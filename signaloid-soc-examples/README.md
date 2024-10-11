# Example applications for the Signaloid SoC
This directory contains example applications for running on the Signaloid SoC. Specifically:
- `breathe-led/` contains an small that applies a "breathing" effect on the Signaloid SoC status LED using soft PWM. This example does not involve a host application.
- `basic-arithmetic/` contains a basic example that executes arithmetics (addition, subtraction, multiplication, and division) on two floating-point values. For this example, we provide two implementations for the host application, written in C and Python.
- `common/` contains the required linker script and initialization script for compiling applications for the Signaloid SoC.

## Getting Started 
### Install the RISC-V GNU toolchain
These examples require the open-source RISC-V GNU toolchain, that you can find [here](https://github.com/riscv-collab/riscv-gnu-toolchain), for targeting the Signaloid SoC. You can either build the toolchain from source, or install one of the pre-compiled binaries that you can find in the [releases](https://github.com/riscv-collab/riscv-gnu-toolchain/releases) section of the repository. You can find more details in the Signaloid C0-microSD [documentation page](https://c0-microsd-docs.signaloid.io/hardware-overview/signaloid-soc/compiling-applications).

### Python requirements
Additionally, the `C0_microSD_toolkit.py` Python script, which is necessary for flashing new binaries to the device, and switching between `Bootloader` and `Signaloid SoC` modes requires `Python3.8` and above.
