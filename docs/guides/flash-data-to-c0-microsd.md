---
layout: default
parent: "Guides"
title: "Flash the C0-microSD"
nav_order: 3
---

# Flash the C0-microSD
You can use the `C0_microSD_toolkit.py`, which you can find [here](https://github.com/signaloid/C0-microSD-utilities), to flash new bitstreams, firmware, and data to the C0-microSD. 

1. Insert the C0-microSD into your computer.
2. Identify the C0-microSD device path. For this example, we assume the device path is `/dev/disk4`. You can find more details on how to identify your C0-microSD [here](/guides/identify-c0-microsd.html).
3. Verify that the C0-microSD is in **Bootloader** mode (solid red LED). If not, switch to **Bootloader** mode and power-cycle the device. You can find more details on how to switch the operation mode of your C0-microSD [here](/guides/identify-c0-microsd.html).
4. Flash new firmware/data to the device using the `C0_microSD_toolkit.py` python script. While the flashing operation takes place, you should see the green LED of the C0-microSD blink rapidly.


## Using the `C0_microSD_toolkit.py` tool
You can use the `C0_microSD_toolkit.py` Python script to configure the C0-microSD and flash new
firmware. The script is written and tested in Python 3.11 on macOS 14.5 and does not use any
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

{: .note }
> All options except of `-s` require the C0-microSD to be in **Bootloader** mode. 

### Examples:
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

Print target C0-microSD information and verify loaded bitstreams:
```sh
sudo python3 ./C0_microSD_toolkit.py -t /dev/sda -i
```
