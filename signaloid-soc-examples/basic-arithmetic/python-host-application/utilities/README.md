# C0-microSD Utilities
This repository offers a set of common C and Python libraries for building host applications that interact
with the [Signaloid C0-microSD hot-pluggable hardware module](https://github.com/signaloid/C0-microSD-hardware),
as well as the `C0_microSD_toolkit`, which you can use to flash new bitstreams and firmware to the device.

## Interfacing with the Signaloid C0-microSD
When connected to a host computer, the Signaloid C0-microSD presents itself as an unformatted block
storage device. Communication with the device is achieved through block reads and writes to a set of
pre-defined addresses. The C0-microSD can operate in two different modes when connected to a
host: `Bootloader` mode and `Signaloid SoC` mode.

- `Bootloader` mode: This mode allows flashing new bitstreams and firmware to the device.
- `Signaloid SoC` mode: This is the built-in Signaloid C0 SoC, which features a subset of
  Signaloid's uncertainty-tracking technology.

Interfacing with the C0-microSD varies depending on the active mode.

In the `src/` folder, you will find common functions and classes for building C and Python applications
that interact with the C0-microSD when the Signaloid SoC mode is active.

## Using the `C0_microSD_toolkit.py` tool
You can use the `C0_microSD_toolkit.py` Python script to configure the C0-microSD and flash new
firmware. The script is written and tested in Python 3.11 on MacOS 14.5 and does not use any
additional libraries. Following are the program's command-line arguments and usage examples:

```
usage: C0_microSD_toolkit.py [-h] -t TARGET_DEVICE [-b INPUT_FILE] [-u | -q | -w | -s | -i] [-f]

Signaloid C0_microSD_toolkit. Version 1.1

options:
  -h, --help        Show this help message and exit.
  -t TARGET_DEVICE  Specify the target device path.
  -b INPUT_FILE     Specify the input file for flashing (required with -u, -q, or -w).
  -u                Flash user data.
  -q                Flash new Bootloader bitstream.
  -w                Flash new Signaloid SoC bitstream.
  -s                Switch boot mode.
  -i                Print target C0-microSD information, and run data verification.
  -f                Force flash sequence (do not check for bootloader).
```

> [!IMPORTANT]  
> All options except of `-s` require the C0-microSD to be in **Bootloader** mode. 

#### Examples:
The following examples assume that the C0-microSD is located in`/dev/sda`.

Flash new custom user bitstream:
```sh
sudo python3 ./C0_microSD_toolkit.py -t /dev/sda -b user-bitstream.bin
```

Flash new user data:
```sh
sudo python3 ./C0_microSD_toolkit.py -t /dev/sda -b program.bin -u
```

Flash new Bootloader bitstream:
```sh
sudo python3 ./C0_microSD_toolkit.py -t /dev/sda -b bootloader-bitstream.bin -q
```

Flash new Signaloid SoC bitstream:
```sh
sudo python3 ./C0_microSD_toolkit.py -t /dev/sda -b signaloid-soc.bin -w
```

Toggle boot mode of C0-microSD:
```sh
sudo python3 ./C0_microSD_toolkit.py -t /dev/sda -s
```

Print target C0-microSD information and verify loaded bitstreams:
```sh
sudo python3 ./C0_microSD_toolkit.py -t /dev/sda -i
```

> [!NOTE]  
> Using the `-s` option will toggle the active configuration. So, if the device has booted in 
> `Bootloader` mode, this option will switch to `Signaloid Core` mode, and vice versa.

## Using the `SD_Dev_toolkit.py` tool
You can use the `SD_Dev_toolkit.py` to detect and power-cycle the SD cards on-board the SD-Dev.
```
usage: SD_Dev_toolkit.py [-h] [-p]

Signaloid SD_Dev_toolkit. Version 0.1

options:
  -h, --help         Show this help message and exit.
  -p, --power-cycle  Power-cycle the onboard full-size SD and microSD cards.
```

## Using the `SD_Dev_power_measure.py` tool
You can use the `SD_Dev_power_measure.py` to read and log power measurement data using the SD-Dev
on-board current sense circuitry. ADC channel 0 corresponds to the full-size SD card socket and
channel 1 to the microSD card socket. For this functionality to work, you must first enable the
I2C kernel module. If you use one of the official Raspberry-Pi OS images, you can do that using
the `raspi-config` command.
```
usage: SD_Dev_power_measure.py [-h] [-s SMBUS_NUMBER] [-o OUTPUT_FILENAME] [-c {0,1}] [-g {1,2,4,8}] [-r {12,14,16}]

Signaloid SD_Dev_power_measure. Version 0.1

options:
  -h, --help            Show this help message and exit.
  -s SMBUS_NUMBER, --smbus-number SMBUS_NUMBER
                        Specify the target smbus number. (default: 1)
  -o OUTPUT_FILENAME, --output_filename OUTPUT_FILENAME
                        Filename of output csv file. When set, the application will log measurements to this file. (default: None)
  -c {0,1}, --channel {0,1}
                        ADC channel. Channel 0 corresponds to the full-size SD card socket and channel 1 to the microSD card socket. (default: 1)
  -g {1,2,4,8}, --gain {1,2,4,8}
                        ADC Programmable Gain Amplifier (PGA) gain. (default: 4)
  -r {12,14,16}, --samle-rate-bits {12,14,16}
                        Sample bits. (default: 12)
```

[^1]: Implementing a subset of the full capabilities of the Signaloid C0 processor.
