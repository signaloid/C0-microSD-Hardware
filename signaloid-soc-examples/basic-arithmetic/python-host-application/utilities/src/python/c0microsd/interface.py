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

import sys
import struct
import time

SIGNALOID_SOC_STATUS_WAIT_FOR_COMMAND = 0
SIGNALOID_SOC_STATUS_CALCULATING = 1
SIGNALOID_SOC_STATUS_DONE = 2
SIGNALOID_SOC_STATUS_INVALID_COMMAND = 3

K_CALCULATE_NO_COMMAND = 0


class C0microSDInterface:
    """Communication interface for C0-microSD.

    This class provides basic functionality for interfacing with the
    Signaloid C0-microSD.
    """

    # 128 KiB offset for hardware status
    DEVICE_CONFIGURATION_STATUS_OFFSET = 0x20000

    BOOTLOADER_CHECK_WORD = b"SBLD"
    SOC_CHECK_WORD = b"SSOC"

    def __init__(
            self, target_device: str,
            force_transactions: bool = False
            ) -> None:

        self.target_device = target_device

        self.configuration = None
        self.configuration_version = None
        self.configuration_state = None
        self.configuration_switching = False
        self.force_transactions = force_transactions

    def _read(self, offset, bytes) -> bytes:
        """
        Reads data from the C0-microSD.

        :return: The read buffer
        """
        try:
            with open(self.target_device, "rb") as device:
                device.seek(offset)
                return device.read(bytes)
        except PermissionError:
            raise PermissionError(
                "Permission denied: You do not have the "
                f"necessary permissions to access {self.target_device}. "
                "Try running this application with root privileges."
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Device not found: The device {self.target_device} "
                "does not exist."
            )

    def _write(self, offset, data) -> int:
        """
        Write data to the C0-microSD.

        :param buffer: The data buffer to write.
        :return: Number of bytes written.
        """
        try:
            with open(self.target_device, "wb") as device:
                device.seek(offset)
                return device.write(data)

        except PermissionError:
            raise PermissionError(
                "Permission denied: You do not have the "
                f"necessary permissions to access {self.target_device}. "
                "Try running this application with root privileges."
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Device not found: The device {self.target_device} "
                "does not exist."
            )

    def get_status(self) -> None:
        """
        Reads configuration status from the C0-microSD.
        """
        data = self._read(self.DEVICE_CONFIGURATION_STATUS_OFFSET, 12)

        # Decode configuration id register
        configuration_id = data[0:4]
        if configuration_id == self.BOOTLOADER_CHECK_WORD:
            self.configuration = "bootloader"
        elif configuration_id == self.SOC_CHECK_WORD:
            self.configuration = "soc"
        elif not self.force_transactions:
            raise RuntimeError("Error: Device is not a C0-microSD.")

        # Decode configuration data register
        configuration_version = data[4:8]
        major_version = (
            (configuration_version[0] << 8) | configuration_version[1]
        )
        minor_version = (
            (configuration_version[2] << 8) | configuration_version[3]
        )
        self.configuration_version = (major_version, minor_version)

        # Decode configuration state register
        self.configuration_state = data[8:12]
        self.configuration_switching = bool(
            int.from_bytes(self.configuration_state, byteorder="big") & 1
        )

        if self.configuration_switching and not self.force_transactions:
            print(self)
            raise RuntimeError(
                "Error: Device is in configuration switching mode. "
                "Power-cycle the device and try again."
            )

    def __str__(self) -> str:
        value = "Signaloid C0-microSD"
        if self.configuration == "bootloader":
            value += " | Loaded configuration: Bootloader"
        elif self.configuration == "soc":
            value += " | Loaded configuration: Signaloid SoC"
        else:
            value += " | Loaded configuration: UNKNOWN"

        if self.configuration:
            major_version = self.configuration_version[0]
            minor_version = self.configuration_version[1]
            value += f" | Version: {major_version}.{minor_version}"
        else:
            value += " | Version: N/A"

        if self.configuration_switching:
            value += " | State SWITCHING"
        else:
            value += " | State IDLE"
        return value


class C0microSDSignaloidSoCInterface(C0microSDInterface):
    """Communication interface for C0-microSD Signaloid SoC configuration.

    This class extends the C0microSDInterface class to include constants and
    routines for interfacing with the Signaloid C0-microSD when the Signaloid
    SoC is loaded. You can use this class to read and write to/from the
    MISO/MOSI buffers, issue commands, and probe the status of the SoC.
    """

    MOSI_BUFFER_SIZE_BYTES = 4096
    MISO_BUFFER_SIZE_BYTES = 4096

    STATUS_REGISTER_OFFSET = 0x00000
    SOC_CONTROL_REGISTER_OFFSET = 0x00004
    COMMAND_REGISTER_OFFSET = 0x10000

    MOSI_BUFFER_OFFSET = 0x50000
    MISO_BUFFER_OFFSET = 0x60000

    def write_signaloid_soc_MOSI_buffer(self, buffer: bytes) -> None:
        """
        Writes data to the C0-microSD MOSI buffer.

        :param buffer: The data buffer to write.
        """
        if len(buffer) > self.MOSI_BUFFER_SIZE_BYTES:
            raise ValueError(
                "Buffer size exceeds maximum allowed "
                f"size of {self.MOSI_BUFFER_SIZE_BYTES} bytes."
            )

        self._write(self.MOSI_BUFFER_OFFSET, buffer)

    def read_signaloid_soc_MISO_buffer(self) -> bytes:
        """
        Reads data from the C0-microSD MISO buffer.

        :return: The read buffer
        """
        return self._read(
            self.MISO_BUFFER_OFFSET,
            self.MISO_BUFFER_SIZE_BYTES
        )

    def send_signaloid_soc_command(self, value: int) -> None:
        """
        Sends a command to the C0-microSD device.

        :param value: The uint32_t value to write
        """
        # Pack the uint32_t value into a 4-byte buffer and send it
        self._write(self.COMMAND_REGISTER_OFFSET, struct.pack("I", value))

    def get_signaloid_soc_status(self) -> int:
        """
        Reads the C0-microSD status register.

        :return: The read uint32_t value
        """
        buffer = self._read(self.STATUS_REGISTER_OFFSET, 4)
        return struct.unpack("I", buffer)[
            0
        ]  # Unpack the buffer to get the uint32_t value

    def calculate_command(
            self,
            command: int,
            idle_command: int = K_CALCULATE_NO_COMMAND
    ) -> bytes:
        """
        Basic command calculation routine. This function sends a command to
        the C0-microSD, polls the device until it reports that the calculation
        has finished, and finally returns the MISO buffer data.

        :param command:         The C0-microSD command.
        :param idle_command:    This is the command that will be sent after the
                                calculation is complete. The default is
                                K_CALCULATE_NO_COMMAND

        :return: The MISO buffer contents after the command has finished.
        """
        data_buffer = None

        self.send_signaloid_soc_command(command)
        sys.stdout.write("Waiting for calculation to finish.")
        sys.stdout.flush()

        while True:
            # Get status of Signaloid C0-microSD compute module
            soc_status = self.get_signaloid_soc_status()

            if soc_status == SIGNALOID_SOC_STATUS_CALCULATING:
                # Signaloid C0-microSD compute module is still calculating
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(0.5)
            elif soc_status == SIGNALOID_SOC_STATUS_DONE:
                # Signaloid C0-microSD completed calculation
                print("\nRead data content...")
                data_buffer = self.read_signaloid_soc_MISO_buffer()
                break
            elif soc_status == SIGNALOID_SOC_STATUS_INVALID_COMMAND:
                print("\nERROR: Device returned 'Unknown CMD'\n")
                break
            elif soc_status != SIGNALOID_SOC_STATUS_WAIT_FOR_COMMAND:
                print("\nERROR: Device returned 'Unknown CMD'\n")
                break

        while (self.get_signaloid_soc_status()
               != SIGNALOID_SOC_STATUS_WAIT_FOR_COMMAND):
            self.send_signaloid_soc_command(idle_command)

        return data_buffer
