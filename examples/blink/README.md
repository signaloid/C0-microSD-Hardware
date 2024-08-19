# Blink example
This design alternatively blinks the red and green LEDs.

### Build and flash the `blink` design:
- Make sure that the open-source CAD toolchain is properly installed.
- Run `make`. 
- After the example builds successfully, insert the Signaloid C0-microSD into your computer.
- Verify the device path at which the Signaloid C0-microSD device shows up in your operating system. In our example, the Signaloid C0-microSD device path is `/dev/disk4`.
- Verify that the device is in `Bootloader` mode (solid red LED).
  - In case the device is not in `Bootloader` mode, you can switch its operation mode by running `make make flash DEVICE=<device-path>` and power-cycling the device.
- Run `make flash DEVICE=<device-path>`. Make sure to replace the `<device-path>` with the correct path of the C0-microSD. For example, if the device path is `/dev/disk4`, you will need to run `make flash DEVICE=/dev/disk4`.


If the bitstream flashed successfully, you should see:
```console
sudo python3 ../../submodules/C0-microSD-utilities/C0_microSD_toolkit.py -t /dev/disk4 -b top.bin
Signaloid C0-microSD | Loaded configuration: Bootloader | Version: 1.0 | State IDLE
Filename:  top.bin
File size:  104090 bytes.
Flashing custom user bitstream...
Attempt 1 of 5: Flashing... Verifying...
Success: The data matches.
Done.
```

You can now unplug the C0-microSD from your computer and power it up using a microSD breakout board. After 3 seconds, you should see the red and green LEDs blinking alternatively.
