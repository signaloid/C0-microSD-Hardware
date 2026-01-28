---
layout: default
parent: "Hardware Overview"
title: "Modes of Operation"
nav_order: 1
---

# Modes of Operation
The C0-microSD has three distinct modes of operation (also referred to as **active configurations**):
1. **Bootloader mode**: In this mode, you can flash new custom bitstreams, update the firmware of the C0-microSD, and flash new user data to the non-volatile memory.
2. **Signaloid SoC mode**: In this mode, the Signaloid C0 Core is loaded into the device.
3. **Custom user bitstream mode**: In this mode, the latest custom user bitstream is loaded into the device.

Modes **1** and **2** are intended to be used in conjunction with a host device, which can communicate with the C0-microSD via the SD interface.

Mode **3** is intended for using the C0-microSD as a standalone FPGA module.

## How the Signaloid C0-microSD's bootloader works
The Signaloid C0-microSD detects whether it has been plugged in an SD host, and if so, presents itself as an unformatted block storage device. You can then write your custom bitstream to a specific offset (using tools such as `dd`) and its built-in bootloader will setup your bitstream so that it is the design that is configured into the FPGA after the system is power cycled.

This behavior is achieved using the iCE40 _warmboot_ capability. The built-in **Bootloader** is always the first configuration to be loaded. Following the logic shown in Figure 1, the **Bootloader** will either stay in its current configuration, switch to the the built-in **Signaloid SoC** configuration, or load the **Custom User Bitstream**.

| <img src="/docs/assets/images/diagrams/signaloid-external-illustration-c0-microSD-boot-order-logic-updated-withCR.png"> |
|:--:|
| **Figure 1:** Boot order logic. |

## Identifying the active mode
You can distinguish between the three modes of operation based on the following ruleset:
- If the C0-microSD is powered on and connected to a host machine:
  - If the C0-microSD is in **Bootloader mode**, the red LED should be constantly on (Figure 2).
  - If the C0-microSD is in **Signaloid SoC mode**, the green LED should be constantly on (Figure 3).
- If the C0-microSD is powered on without a host present, it will switch to **Custom User Bitstream Mode**. In this mode, the behavior of the on-board LEDs is entirely dictated by the custom user bitstream configuration.

| <img style=" width: 300px" src="/docs/assets/images/ortho-renders/normal_size/signaloid-external-illustration-C0-microSD-in-Bootloader-mode-withCR.png"> | <img style=" width: 300px" src="/docs/assets/images/ortho-renders/normal_size/signaloid-external-illustration-C0-microSD-in-Signaloid-SoC-mode-withCR.png"> |
|:--:| :--:| 
| **Figure 2:** C0-microSD in **Bootloader mode**. | **Figure 3:** C0-microSD in **Signaloid SoC mode**. |

## Switching between modes
Switching between modes **1** and **2** requires writing to a pre-defined offset to the C0-microSD via the SD interface. Once this is done the C0-microSD will store the new setting to its on-board SPI flash memory and go into `SWITCHING` state. You need to power-cycle the device for the changes to take effect. You can use the `C0_microSD_toolkit.py`, which you can find [here](https://github.com/signaloid/C0-microSD-utilities), to switch between modes of operation. Once the C0-microSD goes into `SWITCHING` state, the LED which was not constantly on will start blinking. This indicates that the next time the C0-microSD powers up, it will be in a different operation mode (Figures 4 and 5).

| <img style=" width: 300px" loop=infinite src="/assets/images/ortho-renders/small_size/animations/red-solid-green-blink-animation.gif"> | <img style=" width: 300px" loop=infinite src="/assets/images/ortho-renders/small_size/animations/green-solid-red-blink-animation.gif"> |
|:--:| :--:| 
| **Figure 4:** C0-microSD in **Bootloader mode**, switching to **Signaloid SoC mode**. | **Figure 5:** C0-microSD in **Signaloid SoC mode**,switching to **Bootloader mode**. |

You can find a complete guide on how to switch the operation mode of your C0-microSD [here](/guides/switch-c0-microsd-mode.html).
