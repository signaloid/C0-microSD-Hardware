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
import struct

from utilities.src.python.c0microsd.interface \
    import C0microSDSignaloidSoCInterface


kSignaloidC0StatusWaitingForCommand = 0
kSignaloidC0StatusCalculating = 1
kSignaloidC0StatusDone = 2
kSignaloidC0StatusInvalidCommand = 3

kCalculateNoCommand = 0
kCalculateAddition = 1
kCalculateSubtraction = 2
kCalculateMultiplication = 3
kCalculateDivision = 4


# Function to pack floats into a byte buffer
def pack_floats(floats: list, size: int) -> bytes:
    """
    Pack a list of floats to a zero-padded bytes buffer of length size

    :param floats: List of floats to be packed
    :param size: Size of target buffer

    :return: The padded bytes buffer
    """
    buffer = struct.pack(f"{len(floats)}f", *floats)

    # Pad the buffer with zeros
    if len(buffer) < size:
        buffer += bytes(size - len(buffer))
    elif len(buffer) > size:
        raise ValueError(
            f"Buffer length exceeds {size} bytes after packing floats."
        )
    return buffer


def unpack_floats(byte_buffer: bytes, count: int) -> list[int]:
    """
    This function unpacks 'count' number of single-precision floating-point
    numbers from the given byte buffer. It checks if the buffer has enough
    data to unpack.

    Parameters:
        byte_buffer: A bytes object containing the binary data.
        count: The number of single-precision floats to unpack.

    Returns:
        A list of unpacked floating-point values.
    """

    # Each float is 4 bytes
    float_size = 4

    # Check if the buffer has enough bytes to unpack the requested
    # number of floats
    expected_size = float_size * count
    if len(byte_buffer) < expected_size:
        raise ValueError(
            f"Buffer too small: expected at least {expected_size} bytes, \
                got {len(byte_buffer)} bytes.")

    # Unpack the 'count' number of floats ('d' format for float in struct)
    format_string = f'{count}f'
    floats = struct.unpack(format_string, byte_buffer[:expected_size])

    return list(floats)


def parse_arguments():
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        description='Host application for C0-microSD \
            basic demo'
    )

    parser.add_argument(
        'device_path',
        type=str,
        help='Path of C0-microSD',
    )

    parser.add_argument(
        'argument_a',
        type=float,
        help='First argument'
    )

    parser.add_argument(
        'argument_b',
        type=float,
        help='Second argument'
    )

    # Parse the arguments
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    C0_microSD = C0microSDSignaloidSoCInterface(args.device_path)

    try:
        C0_microSD.get_status()
        print(C0_microSD)

        if C0_microSD.configuration != "soc":
            raise RuntimeError(
                "Error: The C0-microSD is not in SoC mode. "
                "Switch to SoC mode and try again."
            )

        print(f"Argument A: {args.argument_a}")
        print(f"Argument B: {args.argument_b}")

        print("Sending parameters to C0-microSD...")
        C0_microSD.write_signaloid_soc_MOSI_buffer(
            pack_floats(
                [args.argument_a, args.argument_b],
                C0_microSD.MOSI_BUFFER_SIZE_BYTES,
            )
        )

        # Calculate addition
        print("Calculating addition...")
        result_buffer = C0_microSD.calculate_command(
            kCalculateAddition)
        result = unpack_floats(result_buffer, 1)[0]
        print(f'Result: {result}')

        # Calculate subtraction
        print("Calculating subtraction...")
        result_buffer = C0_microSD.calculate_command(
            kCalculateSubtraction)
        result = unpack_floats(result_buffer, 1)[0]
        print(f'Result: {result}')

        # Calculate multiplication
        print("Calculating multiplication...")
        result_buffer = C0_microSD.calculate_command(
            kCalculateMultiplication)
        result = unpack_floats(result_buffer, 1)[0]
        print(f'Result: {result}')

        # Calculate division
        print("Calculating division...")
        result_buffer = C0_microSD.calculate_command(
            kCalculateDivision)
        result = unpack_floats(result_buffer, 1)[0]
        print(f'Result: {result}')

    except Exception as e:
        print(
            f"An error occurred while calculating: \n{e} \nAborting.",
            file=sys.stderr
        )
