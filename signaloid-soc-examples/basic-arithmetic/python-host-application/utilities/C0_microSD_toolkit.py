#!/usr/bin/env python3

# Copyright (c) 2024, Signaloid.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import argparse
import sys
import os
import json
import binascii

from src.python.c0microsd.interface import C0microSDInterface

APP_VERSION = "1.2"  # Application version
MAX_FLASH_ATTEMPTS = 5  # Maximum flashing attempts


class C0microSDToolkit(C0microSDInterface):
    # 256 KiB offset for switch config
    BOOTLOADER_SWITCH_CONFIG_OFFSET = 0x40000
    # 384 KiB offset for unlocking bootloader
    BOOTLOADER_UNLOCK_OFFSET = 0x60000
    # 512 KiB offset for bootloader bitstream
    BOOTLOADER_BITSTREAM_OFFSET = 0x80000
    # 1.0 MiB offset for Signaloid SoC bitstream
    SOC_BITSTREAM_OFFSET = 0x100000
    # 1.5 MiB offset for application bitstream
    USER_BITSTREAM_OFFSET = 0x180000
    # 2.0 MiB offset for userspace
    USER_DATA_OFFSET = 0x200000

    SERIAL_NUMBER_OFFSET = 0x22040
    SERIAL_NUMBER_SIZE = 0x40

    UUID_OFFSET = 0x22080
    UUID_SIZE = 0x40

    BOOTLOADER_UNLOCK_WORD = b"UBLD"

    def _strip_trailing_bytes(
            self, byte_array: bytearray, byte: int
            ) -> bytearray:
        """
        Strip the trailing bytes of a bytearray

        :param byte_array (iterable of bytes): Array of bytes to strip.
        :param byte (int): The byte to remove.
        :return (bytearray): Stripped array of bytes
        """
        end = len(byte_array)
        while end > 0 and byte_array[end - 1] == byte:
            end -= 1
        return byte_array[:end]

    def switch_boot_config(self) -> None:
        """
        Switches the boot configuration of C0-microSD.
        """
        self.get_status()

        if (self.configuration) == "bootloader":
            print(
                "Switching device boot mode from "
                "Bootloader to Signaloid SoC..."
            )
        elif (self.configuration) == "soc":
            print(
                "Switching device boot mode from "
                "Signaloid SoC to Bootloader..."
            )
        elif self.force_transactions:
            print("Switching device boot mode...")

        self._write(self.BOOTLOADER_SWITCH_CONFIG_OFFSET, bytes([0] * 512))

        print(
            "Device configured successfully. "
            "Power cycle the device to boot in new mode."
        )

        if (self.configuration == "bootloader"):
            print(
                "To use the Signaloid C0-microSD in Custom User Bitstream mode"
                ", power it on without an SD-protocol host present."
            )

    def unlock_bootloader(self) -> None:
        """
        Unlocks the bootloader. Used to flash new bootloader or Signaloid SoC.
        """
        self.get_status()
        print("Unlocking bootloader...")
        self._write(self.BOOTLOADER_UNLOCK_OFFSET, self.BOOTLOADER_UNLOCK_WORD)

    def lock_bootloader(self) -> None:
        """
        Locks the bootloader and Signaloid SoC sections.
        """
        self.get_status()
        print("Locking bootloader...")
        self._write(self.BOOTLOADER_UNLOCK_OFFSET, bytes([0] * 32))

    def flash_and_verify(
        self, file_data: bytes, flash_offset: int, max_attempts: int
    ) -> bool:
        """
        Flashes data to the C0-microSD and verifies that the flashing
        process was successful.

        :param file_data: A byte buffer with the data to be written
        :param flash_offset: Device offset (in bytes) for the data
                             to be written
        :param max_attempts: Maximum failed attempts before aborting operation
        """
        self.get_status()

        if self.configuration != "bootloader" and not self.force_transactions:
            raise RuntimeError(
                "Error: device is not in Bootloader mode. "
                "Switch to Bootloader mode and try again"
            )

        input_file_bytes = len(file_data)
        for i in range(1, max_attempts + 1):
            print(
                f"Attempt {i} of {max_attempts}: Flashing... ",
                end="",
                flush=True
            )
            self._write(flash_offset, file_data)
            print("Verifying...")
            data_to_verify = self._read(flash_offset, input_file_bytes)
            if data_to_verify == file_data:
                print("Success: The data matches.")
                return True
            else:
                print("Error: The data do not match.")
        return False

    def get_bitstream_prefix(self, bitstream_offset: int) -> bytes:
        """
        Reads the prefix section of a bitstream

        :param offset: Offset of bitstream in flash memory
        """

        # We assume that the prefix is never going to be larger than 4K
        self.get_status()
        prefix_chunk = self._read(bitstream_offset, 4096)

        prefix_start_word = b'\xFF\x00'
        prefix_end_word = b'\x00\xFF'

        prefix_start = prefix_chunk.find(prefix_start_word)
        prefix_end = prefix_chunk.find(prefix_end_word, prefix_start)

        if prefix_start == -1 or prefix_end == -1:
            raise ValueError("Could not find bitstream prefix section.")

        prefix_end += len(prefix_end_word)

        prefix_data = prefix_chunk[
            prefix_start + len(prefix_start_word):
            prefix_end - len(prefix_end_word)
        ]

        return prefix_data

    def verify_bitstream_crc(
            self,
            bitstream_offset: int,
            bitstream_crc: int,
            bitstream_prefix_size: int,
            bitstream_size: int
    ) -> bool:
        """
        Verifies a the crc32 checksum of a bitstream

        :param bitstream_offset: Offset of bitstream in flash memory
        :param bitstream_crc: Expected crc of bitstream
        :param bitstream_size: Expected size of bitstream in bytes
        """

        bitstream = self._read(
            bitstream_offset, bitstream_prefix_size + bitstream_size
        )

        bitstream_data = bitstream[bitstream_prefix_size:]
        actual_crc = binascii.crc32(bitstream_data) & 0xFFFFFFFF

        return actual_crc == bitstream_crc

    def print_bitstream_information(self, offset) -> None:
        """
        Reads and prints bitstream prefix from a specific offset in the
        device. Also runs crc verification if prefix is in json format and
        includes `bitstream_crc` and `bitstream_size` attributes

        :param bitstream_offset: Offset of bitstream in flash memory
        :param bitstream_crc: Expected crc of bitstream
        :param bitstream_size: Expected size of bitstream in bytes
        """
        bitstream_prefix_data = self.get_bitstream_prefix(offset)

        bitstream_prefix_string = bitstream_prefix_data.decode('utf-8')

        print(f"    Bitstream prefix section: {bitstream_prefix_string}")

        try:
            prefix_json = json.loads(bitstream_prefix_string)
            bitstream_crc = prefix_json["bitstream_crc"]
            bitstream_size = prefix_json["bitstream_size"]
            crc_pass = self.verify_bitstream_crc(
                offset,
                bitstream_crc,
                len(bitstream_prefix_data) + 4,
                bitstream_size
            )

            if crc_pass:
                print("    Bitstream CRC verification: PASS")
            else:
                print("    Bitstream CRC verification: FAIL")
        except ValueError or KeyError:
            print("    Unable to parse prefix for CRC verification")

    def verify_warmboot_section(self) -> bool:
        warmboot_section = self._read(0, 5*32).hex()
        warmboot_section_template = str(
            "7eaa997e92000044030800008200000108000000000000000000000000000000"
            "7eaa997e92000044030800008200000108000000000000000000000000000000"
            "7eaa997e92000044031000008200000108000000000000000000000000000000"
            "7eaa997e92000044031800008200000108000000000000000000000000000000"
            "7eaa997e92000044030800008200000108000000000000000000000000000000"
        )

        return warmboot_section == warmboot_section_template

    def get_serial_number(self) -> str:
        serial_number_section = self._read(
            self.SERIAL_NUMBER_OFFSET, self.SERIAL_NUMBER_SIZE
        )
        serial_number_section = self._strip_trailing_bytes(
            serial_number_section, 0xFF
        )

        serial_number_section = ''.join(
            to_printable(byte) for byte in serial_number_section
        )
        return serial_number_section

    def get_uuid(self) -> str:
        uuid_section = self._read(
            self.UUID_OFFSET, self.UUID_SIZE
        )
        uuid_section = self._strip_trailing_bytes(
            uuid_section, 0xFF
        )

        uuid_section = ''.join(
            to_printable(byte) for byte in uuid_section
        )
        return uuid_section


def to_printable(byte: bytearray) -> str:
    """
    Decode byte to character using UTF-8 encoding.
    Decode anything that is not UTF-8 as '.'
    """
    return chr(byte) if 32 <= byte <= 126 else '.'


def confirm_action() -> bool:
    """
    Prompts the user to accept/reject action

    :return: response
    """
    while True:
        # Prompt the user with the warning message
        response = input(
            "WARNING: This action may render the device inoperable. "
            "Proceed? (y/n): "
        ).lower()
        if response == "y":
            return True
        elif response == "n":
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")


def main():
    parser = argparse.ArgumentParser(
        description=f"Signaloid C0-microSD-toolkit. Version {APP_VERSION}",
        add_help=False
    )

    parser.add_argument(
        '-h', '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='Show this help message and exit.'
    )

    parser.add_argument(
        "-t",
        dest="target_device",
        required=True,
        help="Specify the target device path.",
    )
    parser.add_argument(
        "-b",
        dest="input_file",
        help=("Specify the input file for flashing "
              "(required with -u, -q, or -w)."),
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-u",
        dest="flash_user_data",
        action="store_true",
        help="Flash user data."
    )
    group.add_argument(
        "-q",
        dest="flash_bootloader",
        action="store_true",
        help="Flash new Bootloader bitstream."
    )
    group.add_argument(
        "-w",
        dest="flash_signaloid_soc",
        action="store_true",
        help="Flash new Signaloid SoC bitstream."
    )
    group.add_argument(
        "-s",
        dest="switch_boot_mode",
        action="store_true",
        help="Switch boot mode."
    )
    group.add_argument(
        "-i",
        dest="print_information",
        action="store_true",
        help="Print target C0-microSD information, and run data verification."
    )

    parser.add_argument(
        "-f",
        dest="force_flash",
        action="store_true",
        help="Force flash sequence (do not check for bootloader).",
    )

    args = parser.parse_args()

    # Create a new toolkit instance
    try:
        # Create a new toolkit object
        toolkit = C0microSDToolkit(
            args.target_device, force_transactions=args.force_flash
        )

        # Get status of the C0-microSD, also used to verify that communication
        # is correct, and that the C0-microSD is in bootloader mode.
        toolkit.get_status()

        print(toolkit)

        # Print additional information and exit
        if args.print_information:
            if toolkit.configuration != "bootloader":
                print("Device is not in Bootloader mode.")
                print(
                    "To display device Serial Number, device UUID, and verify "
                    "the bitstream and warmboot sections \nof the "
                    "non-volatile memory, switch to Bootloader mode and "
                    "try again."
                )
                print("Done.")
                exit(os.EX_OK)

            print(f"Device Serial Number: {toolkit.get_serial_number()}")
            print(f"Device UUID: {toolkit.get_uuid()}")
            print()
            print("Reading Bootloader bitstream:")
            toolkit.print_bitstream_information(
                toolkit.BOOTLOADER_BITSTREAM_OFFSET)
            print("Reading Signaloid SoC bitstream:")
            toolkit.print_bitstream_information(
                toolkit.SOC_BITSTREAM_OFFSET)
            toolkit.verify_warmboot_section()
            if (toolkit.verify_warmboot_section()):
                print("Warmboot section verification: PASS")
            else:
                print("Warmboot section verification: FAIL")
            print("Done.")
            exit(os.EX_OK)

        # This is the time to switch boot mode if needed.
        if args.switch_boot_mode:
            toolkit.switch_boot_config()
            print("Done.")
            exit(os.EX_OK)

        # All commands after this point need an input file
        if not args.input_file:
            parser.print_help()
            print("\nOption -b is required when flashing data.")
            sys.exit(os.EX_USAGE)

        # Open the input file and store data in memory.
        file_data = None
        try:
            with open(args.input_file, "rb") as src:
                file_data = src.read()
        except PermissionError:
            raise PermissionError(
                "Permission denied: You do not have the "
                f"necessary permissions to access {args.input_file}."
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                f"File not found: The file {args.input_file} does not exist."
            )

        print("Filename: ", args.input_file)
        print("File size: ", len(file_data), "bytes.")

        if args.flash_bootloader:
            if not confirm_action():
                print("Aborting.")
                exit(os.EX_USAGE)
            toolkit.unlock_bootloader()
            print("Flashing bootloader bitstream...")
            toolkit.flash_and_verify(
                file_data, toolkit.BOOTLOADER_BITSTREAM_OFFSET,
                MAX_FLASH_ATTEMPTS
            )
            toolkit.lock_bootloader
        elif args.flash_signaloid_soc:
            if not confirm_action():
                print("Aborting.")
                exit(os.EX_USAGE)
            toolkit.unlock_bootloader()
            print("Flashing Signaloid SoC bitstream...")
            toolkit.flash_and_verify(
                file_data,
                toolkit.SOC_BITSTREAM_OFFSET,
                MAX_FLASH_ATTEMPTS
            )
            toolkit.lock_bootloader
        elif args.flash_user_data:
            print("Flashing user data bitstream...")
            toolkit.flash_and_verify(
                file_data,
                toolkit.USER_DATA_OFFSET,
                MAX_FLASH_ATTEMPTS
            )
        else:
            print("Flashing custom user bitstream...")
            toolkit.flash_and_verify(
                file_data, toolkit.USER_BITSTREAM_OFFSET, MAX_FLASH_ATTEMPTS
            )
        print("Done.")
    except Exception as e:
        print(f"{e}\nAn error occurred, aborting.", file=sys.stderr)
        if isinstance(e, ValueError):
            exit(os.EX_DATAERR)
        elif isinstance(e, FileNotFoundError):
            exit(os.EX_NOINPUT)
        elif isinstance(e, PermissionError):
            exit(os.EX_NOPERM)
        else:
            exit(os.EX_SOFTWARE)


if __name__ == "__main__":
    main()
