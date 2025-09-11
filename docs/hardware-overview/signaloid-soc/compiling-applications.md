---
layout: default
grand_parent: "Hardware Overview"
parent: "Signaloid SoC"

title: "Compiling Applications"
nav_order: 2
---

# Compiling Applications for the Signaloid SoC

## Install the RISC-V GNU cross-compilation toolchain
To compile applications for the built-in Signaloid SoC, you will require the open-source RISC-V GNU cross-compilation toolchain, that you can find [here](https://github.com/riscv-collab/riscv-gnu-toolchain). You can build the cross-compilation toolchain from source, make sure to install it for the `RV32I` instruction set.

>[!Note]
>At the time of writing, pre-built binaries that you can find in the [releases](https://github.com/riscv-collab/riscv-gnu-toolchain/releases) section of the cross-compilation toolchain [repository](https://github.com/riscv-collab/riscv-gnu-toolchain), **do not contain** the standard C libraries compiled for the `rv32i`/`ilp32` configuration needed for the Signaloid SoC on the C0-microSD, which, if used, will result in compilation fatal errors. Please use the build guide below to build it from source.


### Building from source.
You can find general installation instructions in the top-level `README.md` file of the cross-compilation toolchain [repository](https://github.com/riscv-collab/riscv-gnu-toolchain) to install it in your system. For targeting the Signaloid SoC, you must specify the target architecture to be RV32I. To do that, you must follow these steps:

#### Step A: Clone RISC-V GNU cross-compilation toolchain.
```sh
git clone --recursive https://github.com/riscv-collab/riscv-gnu-toolchain.git
```

#### Step B: Install gcc (macOS 14+ only)
This is a necessary step for macOS 14+ with Apple clang version 15.0.0 (clang-1500.3.9.4). Ignore this step in older macOS versions and Linux.

Install `gcc-mp-13` and `g++-mp-13` using:
```sh
sudo port install gcc13
```

Set `CC` and `CXX` environment variables so that the following configure picks them up:
```sh
export CXX=g++-mp-13 CC=gcc-mp-13
```

#### Step C: Configure the cross-compilation toolchain installation
Configure the Makefiles to build for the RISC-V R32I ISA with the `ilp32` application binary interface (ABI). Note that the `--prefix` flag sets where you wish the cross-compilation toolchain to be installed. You need to modify `/path/to/installation/dir` accordingly. The `disable-gdb` disables the build of `gdb`. You can remove it if you wish to build `gdb`.
```bash
./configure --prefix=/path/to/installation/dir --with-arch=rv32i --with-abi=ilp32 --disable-gdb
```

#### Step D: Build
You can start the build by executing:
```sh
make
```
You can optionally instruct `make` to parallelize the build process using the `-j` flag. For example, to use four parallel workers you need to execute:
```sh
make -j4
```

The build process takes some minutes. If it is successful, you should see the cross-compilation toolchain in the installation directory that you specified using the prefix argument in the configuration step.

## Compile your application
You can find Makefile examples for compiling applications for the Signaloid SoC in the `signaloid-soc-examples/` directory of the official C0-microSD [repository](https://github.com/signaloid/C0-microSD-hardware). When compiling the examples, make sure to modify each Makefile to correctly point to your toolchain installation path.
