# Breathe example
This application applies a "breathing" effect on the Signaloid SoC status LED using soft pulse width modulation (PWM). 

# How to use:
1. Make sure the C0-microSD is in `Bootloader` mode and connected.
2. Modify the `Makefile` to point to your `rv32i` toolchain[^1].
3. Run `make` to build the application.
4. Run `make flash DEVICE=/dev/diskx` where `/dev/diskX` is the C0-microSD device path.
5. Run `make switch DEVICE=/dev/diskx` where `/dev/diskX` is the C0-microSD device path (the green LED should blink).
6. Power cycle the C0-microSD. The green LED should light up solid and the red LED should light up with a "breathing" effect.

[^1]: You will need to install the [riscv-gnu-toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain) on your system. Make sure the toolchain supports `RV32I`.
