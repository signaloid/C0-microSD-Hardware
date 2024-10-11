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

from src.python.sddev.sddev import SDDevADCInterface
import sys
import signal
from datetime import datetime
import argparse

APP_VERSION = "0.1"  # Application version


def sigint_handler(signal, frame):
    print("\n\nExiting...")
    sys.exit(0)


if __name__ == "__main__":

    # Register the signal handler for SIGINT
    signal.signal(signal.SIGINT, sigint_handler)

    parser = argparse.ArgumentParser(
        description=f"Signaloid SD_Dev_power_measure. Version {APP_VERSION}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False
    )

    parser.add_argument(
        '-h', '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='Show this help message and exit.'
    )

    parser.add_argument(
        "-s", "--smbus-number",
        dest="smbus_number",
        default=1,
        type=int,
        help="Specify the target smbus number.",
    )

    parser.add_argument(
        "-o", "--output_filename",
        dest="output_filename",
        help="""Filename of output csv file. When set, the application will
        log measurements to this file."""
    )

    parser.add_argument(
        "-c", "--channel",
        dest="channel",
        default=1,
        type=int,
        choices=[0, 1],
        help="""ADC channel. Channel 0 corresponds to the full-size SD card
        socket and channel 1 to the microSD card socket."""
    )

    parser.add_argument(
        "-g", "--gain",
        dest="gain",
        default=4,
        type=int,
        choices=[1, 2, 4, 8],
        help="ADC Programmable Gain Amplifier (PGA) gain."
    )

    parser.add_argument(
        "-r", "--samle-rate-bits",
        dest="sample_rate_bits",
        default=12,
        type=int,
        choices=[12, 14, 16],
        help="Sample bits."
    )

    args = parser.parse_args()

    print("SMBusNumber:\t\t\t" + str(args.smbus_number))
    print("Channel:\t\t\t" + str(args.channel))
    print("ADC PGA gain:\t\t\t" + str(args.gain))
    print("Sample bits:\t\t" + str(args.sample_rate_bits))

    sdDev = SDDevADCInterface(
        int(args.smbus_number),
        channel=args.channel,
        pga_gain=args.gain,
        sample_rate_bits=args.sample_rate_bits,
    )

    resolution = sdDev.current_sense_resolution * 1000
    print(f"Current sense resolution: \t{resolution} mA")
    print(f"Maximum sense current: \t\t{sdDev.max_current_sense * 1000} mA")

    if args.output_filename is not None:
        print("Logging data to: \t\t" + str(args.output_filename))
        fp = open(args.output_filename, "w")
        fp.write(
            "index, timestamp(uS), current(mA), power(mW)\n"
        )
    print()

    measurement_count = 0
    while 1:
        # Multiply by 1000 to convert it to mA
        current = sdDev.read_converted_current_measurement() * 1000
        power = current * sdDev.SDDEV_SD_USD_VOLTAGE
        # Get the current time
        now = datetime.now()

        # Output data to terminal
        print(f'\rCurrent measurement: \t{current:20.10f} mA', end='')
        print(f'\nPower measurement: \t{power:20.10f} mW', end='\033[F')

        if args.output_filename is not None:
            # Calculate the time in microseconds since the start of the day
            timestamp = (
                now.hour * 3600 +
                now.minute * 60 +
                now.second) * 1_000_000 + now.microsecond

            fp.write(
                str(measurement_count) + ", " +
                str(timestamp) + ", " +
                str(current) + ", " +
                str(power) + "\n"
            )

        measurement_count += 1
