# Basic arithmetic example for Signaloid SoC
This is a simple [Signaloid SoC](https://c0-microsd-docs.signaloid.io/hardware-overview/signaloid-soc/) example that executes basic arithmetics (addition, subtraction, multiplication, and division) on two floating-point values. The application running on the Signaloid SoC is designed to work in conjunction with a "master" host application that sends parameters and issues commands. The host application communicates with the Signaloid SoC via the SD interface by issuing block reads/writes to a set of pre-determined [addresses](https://c0-microsd-docs.signaloid.io/hardware-overview/signaloid-soc/communication-scheme.html). For this example, we provide two implementations for the host application, written in C and Python.

Directories:
- `signaloid-soc-application/` contains the source code for the Signaloid SoC application.
- `host-application/` contains a C-based application that runs on the host machine and communicates with the Signaloid SoC.
- `python-host-application/` contains a Python based application that runs on the host machine and communicates with the Signaloid SoC.

# How to use:
## Build and flash the Signaloid SoC application
1. Make sure the C0-microSD is in `Bootloader` mode and connected.
2. Navigate to the `signaloid-soc-application/` directory.
3. Modify the `Makefile` to point to your `RV32I` toolchain[^1].
4. Run `make` to build the application.
5. Run `make flash DEVICE=/dev/diskx`, where `/dev/diskX` is the C0-microSD device path[^2], to flash the application.
6. Run `make switch DEVICE=/dev/diskx`, where `/dev/diskX` is the C0-microSD device path, to switch to the Signaloid SoC (the green LED should blink).
7. Power cycle the C0-microSD. The green LED should light up[^3].

## Build and run the C based host application
1. Navigate to the `host-application` directory.
2. Run `make` to build the application.
3. Run `sudo ./host-application /dev/diskX` where `/dev/diskX` is the C0-microSD device path.

## Run the Python based host application
1. Navigate to the `python-host-application` directory.
2. Run `sudo python3 host_application.py /dev/diskX A B` where `/dev/diskX` is the C0-microSD device path, and `A` and `B` are floating point values.

[^1]: You will need to install the [riscv-gnu-toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain) on your system. Make sure the toolchain supports `RV32I`.
[^2]: Guide: [Identify the Signaloid C0-microSD](https://c0-microsd-docs.signaloid.io/guides/identify-c0-microsd.html).
[^3]: Guide: [Switch between Operation Modes](https://c0-microsd-docs.signaloid.io/guides/switch-c0-microsd-mode.html)
