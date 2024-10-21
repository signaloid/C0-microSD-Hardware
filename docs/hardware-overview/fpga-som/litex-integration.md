---
layout: default
grand_parent: "Hardware Overview"
parent: "FPGA System on Module"

title: "LiteX Integration on Signaloid C0-microSD"
nav_order: 4
---

# LiteX Framework and Signaloid C0-microSD Integration
By following this guide, you should be able to build, flash, and run the LiteX-based SoC on your Signaloid C0-microSD. Feel free to explore and modify the design to suit your specific needs!

## What is LiteX?
[LiteX](https://github.com/enjoy-digital/litex) is an open-source digital hardware design framework that simplifies the creation of complex digital systems, particularly System-on-Chip (SoC) designs. It's built on top of [Migen](https://m-labs.hk/migen/), a Python-based hardware description language and provides a high-level abstraction for designing digital circuits.  

LiteX offers numerous benefits, including rapid prototyping with pre-built components and high-level abstractions, flexibility in customization and extension, portability across FPGA platforms, easy integration of IP cores and peripherals, community support, and serves as an excellent learning tool for software engineers transitioning to hardware design.

Key features of LiteX include:
- Python-based design flow
- Modular architecture
- Support for various CPU cores (including RISC-V)
- Built-in peripherals and interfaces
- Vendor-agnostic approach (supports multiple FPGA families)

## Using the Signaloid C0-microSD LiteX Integration Example
The [Signaloid C0-microSD-litex-integration](https://github.com/signaloid/Signaloid-C0-microSD-litex-integration) repository provides an example RISC-V SoC implementation for the Signaloid C0-microSD using LiteX. It includes Makefiles for building and flashing both the FPGA bitstream and firmware binary.

### Prerequisites
Before you begin, ensure you have the following tools installed:
1. [Yosys](https://github.com/YosysHQ/yosys)
2. [nextpnr](https://github.com/YosysHQ/nextpnr)
3. [IceStorm](https://github.com/YosysHQ/icestorm)
4. [RISC-V GNU Toolchain](https://github.com/riscv/riscv-gnu-toolchain) with support for the `RV32IM` instruction set

We recommend using the [OSS CAD Suite](https://github.com/YosysHQ/oss-cad-suite-build) to install `Yosys`, `nextpnr`, and `IceStorm`.

### Getting Started
1. Clone the repository:
	```
	git clone --recursive git@github.com:signaloid/Signaloid-C0-microSD-litex-integration
	```

2. Navigate to the project root directory:
	```
	cd Signaloid-C0-microSD-litex-integration
	```

3. Configure the build environment:
	- Open the `config.mk` file.
	- Set the `CROSS_COMPILE_PATH` variable to your RISC-V GNU Toolchain installation path.
	- Set the `DEVICE` variable to the correct device path for your Signaloid C0-microSD (follow the [Identify the Signaloid C0-microSD](/guides/identify-c0-microsd) guide).

4. Build and flash both gateware and firmware:
	```
	make flash
	```

### Gateware Details
For this example, we use the default Signaloid C0-microSD target design from [litex-boards](https://github.com/litex-hub/litex-boards/blob/master/litex_boards/targets/signaloid_c0_microsd.py), featuring:
- VexRISC-V-Lite SoC with IM support
- UART interface for serial communication
- 12MHz default system clock
- 128KB SRAM
- 14MB binary & files storage on SPI Flash

### Firmware Details
The example firmware implements:
- LED blinking (red and green) every 250ms.
- Printing the active LED identifier ('r' for red, 'g' for green) to the UART serial port.
- UART echo functionality (tx to rx).

### Serial Communication
You can interact with the SoC via the UART serial interface.
1. Connect your Signaloid C0-microSD UART serial port to your computer using a compatible 3.3V USB-to-serial adapter, such as the [FTDI FT232RL](https://ftdichip.com/products/ttl-232r-3v3/), or the [Tigard board](https://github.com/tigard-tools/tigard).  
UART port pins:
	- TX: `SD_CMD` (`A4`)
	- RX: `SD_CLK` (`B3`)
1. Configure your serial terminal with a baud rate of 115200.  
	Example using `screen` on Linux:
	```
	screen /dev/ttyACM0 115200
	```

## Customizing the Design
To modify the SoC design:

1. Edit the `signaloid_c0_microsd.py` file in the `gateware/` directory.
2. Rebuild the gateware using `make gateware`.

To modify the firmware:

1. Edit the source files in the `firmware/src/` directory.
2. Rebuild the firmware using `make firmware`.

## Troubleshooting
If you encounter issues:

1. Ensure all prerequisites are correctly installed.
2. Ensure that the [Signaloid-C0-microSD-litex-integration](https://github.com/signaloid/Signaloid-C0-microSD-litex-integration) repository was cloned recursively.
3. Verify that `CROSS_COMPILE_PATH` and `DEVICE` in `config.mk` are set correctly.
4. Check the console output for specific error messages.
5. If flashing fails, ensure you have the necessary permissions to access the device.

For further assistance, please contact Signaloid Developer Support at: developer-support@signaloid.com.

## Further Resources
We also provide a more advanced LiteX SoC design that uses the Lattice iCE40 hard I2C IP to communicate with peripherals. You can find that in the [Signaloid-C0-microSD-litex-I2C-demo](https://github.com/signaloid/Signaloid-C0-microSD-litex-I2C-demo) repository. You can also read more in the official [LiteX](https://github.com/enjoy-digital/litex/wiki) and [Migen](https://m-labs.hk/migen/) documentation pages.
