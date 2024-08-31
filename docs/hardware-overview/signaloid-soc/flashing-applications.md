---
layout: default
grand_parent: "Hardware Overview"
parent: "Signaloid SoC"

title: "Flashing Applications"
nav_order: 2
---

# Flashing Applications to the C0-microSD
You can use the `C0_microSD_toolkit.py`, which you can find [here](https://github.com/signaloid/C0-microSD-utilities), to flash custom binary applications to the C0-microSD, and run them using the built-in Signaloid SoC. This requires switching between **Bootloader** mode for flashing your custom binary, and **Signaloid SoC** mode for executing it:

1. Plug in and identify your C0-microSD. For more details on how to identify your C0-microSD see [here](/guides/identify-c0-microsd.html)
2. Make sure that the C0-microSD is in **Bootloader** mode (red LED). If not, switch to **Bootloader** mode and power-cycle the device. For more details on how to switch the C0-microSD operation mode see [here](/guides/switch-c0-microsd-mode.html). 
3. Flash your custom binary using the `C0_microSD_toolkit.py`. For more details on how to use the toolkit see [here](/guides/flash-data-to-c0-microsd.html). The Signaloid SoC initializes its memory using the first 128 KiB of the `USER_DATA` section, so you need to use the `-u` option.
4. Switch the device to **Signaloid SoC** mode and power-cycle it.
