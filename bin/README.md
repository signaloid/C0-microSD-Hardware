# Synthesized FPGA configuration bitstreams:
`bootloader.bin`: Bootloader bitstream
`signaloid-soc.bin`: Signaloid Core bitstream
`blink.bin`: Simple design that alternatively blinks the onboard LEDs

## Using the Makefile:

### Flash the packed bitstreams using external tool.
To flash the device using an external tool like the Tigard board, run `make` to pack the bitstreams and `make flash` to flash the final bitstream to the nonvolatile memory using `iceprog`. You can find more details [here](https://c0-microsd-docs.signaloid.io/guides/use-external-programmer).

### Flash bitstreams using the built-in bootloader
1. Connect the device to your computer and make sure it is on bootloader mode (red LED).
2. Find the device path using `fdisk` or `diskutil`. For this example we assume `/dev/disk4`
3. Flash the bitstream that you want:
   1. For overriding the bootloader do: `make flash-dfu-bootloader DFU_DEVICE=/dev/disk4`
   2. For overriding the SoC do: `make flash-dfu-soc DFU_DEVICE=/dev/disk4`
   3. For flashing the blink example bitstream do: `make flash-dfu-blink DFU_DEVICE=/dev/disk4`
4. Make sure to power-cycle the device for the new bitstreams to take effect.
