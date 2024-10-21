![](https://github.com/signaloid/C0-microSD-Hardware/actions/workflows/jekyll.yml/badge.svg)


# Signaloid C0-microSD Hot-Pluggable Hardware Module
The **Signaloid C0-microSD** has two main use cases: You can either **(1) use it as a hot-pluggable co-processor module** (it implements a subset of Signaloid's C0 processor), or you can **(2) use it as a hot-pluggable FPGA module**. The Signaloid C0-microSD contains a bootloader that exposes the hardware module's functionality as a SD mass storage device, making it easy to configure new applications in either of the two use cases by performing I/O to the module when it is plugged into a host system. 


![C0-microSD pinout](docs/assets/images/C0-microSD-pinout-horizontal.png)


## Repository Submodules
A companion repository for the hardware module's [bootloader utilities](https://github.com/signaloid/C0-microSD-utilities/), included as a submodule, contains utilities for interacting with the bootloader, and libraries for building your own applications for the built-in Signaloid Soc.

## Repository Structure
- The `examples/` folder contains example applications that run on the built Signaloid Soc of the device.
- The `bin/` folder contains the latest `Bootloader` and `Signaloid Soc` bitstreams for your C0-microSD, as well as a pre-synthesized blink example.
- The `docs/` folder contains the documentation of the C0-microSD.

## Cloning the Repository 
The correct way to clone this repository is:
```
git clone --recursive git@github.com:signaloid/C0-microSD-hardware.git
```
To update all submodules
```
git pull --recurse-submodules
git submodule update --remote --recursive
```
If you forgot to clone with `--recursive`, and end up with empty submodule directories, you can remedy this with
```
git submodule update --init --recursive
```

## Documentation
You can find the latest documentation for the Signaloid C0-microSD [here](https://c0-microsd-docs.signaloid.io/).

## Compatibility
For host controllers and adapters known to be compatible with the Signaloid C0-microSD SoM, please see [the compatibility section](https://c0-microsd-docs.signaloid.io/hardware-overview/compatibility.html) of the documentation.

