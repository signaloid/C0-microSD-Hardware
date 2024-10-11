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
#

from src.python.sddev.sddev import SDDevController
import argparse

APP_VERSION = "0.1"  # Application version


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"Signaloid SD_Dev_toolkit. Version {APP_VERSION}",
        add_help=False
    )

    parser.add_argument(
        '-h', '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='Show this help message and exit.'
    )

    parser.add_argument(
        "-p", "--power-cycle",
        dest="power_cycle",
        action="store_true",
        help="Power-cycle the onboard full-size SD and microSD cards.",
    )

    args = parser.parse_args()
    controller = SDDevController()

    full_size_sd_detect, micro_sd_detect = controller.detect_cards()
    print("Detected full-size SD card: " + str(full_size_sd_detect))
    print("Detected microSD card: " + str(micro_sd_detect))

    if args.power_cycle:
        "Power cycling SD cards..."
        controller.refresh_sd_cards()
