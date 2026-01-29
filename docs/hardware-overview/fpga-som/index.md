---
layout: default
title: "FPGA System on Module"
parent: "Hardware Overview"
has_children: true
nav_order: 4
---

# Using the Signaloid C0-microSD as a Hot-Pluggable FPGA System on Module (SoM)
When using the Signaloid C0-microSD as a hot-pluggable FPGA SoM, you can plug it into your computer, flash new FPGA bitstreams, and then either plug it into a breadboard using a microSD breakout board, or integrate it into a legacy (or custom) PCB that has an unused microSD slot. Once powered on, the built-in bootloader will check if the device has been connected to an SD host, and if not, will load the latest custom user bitstream. In this configuration, the C0-microSD offers six configurable I/O pins by repurposing the microSD pads, and five additional I/O pins in the form of test pads.

| ![C0-microSD on breadboard](/assets/images/ortho-renders/breakout-board/signaloid-external-illustration-C0-microSD-populating-a-breadboard-using-a-microSD-breakout-board-withCR.png) | ![C0-microSD on microcontroller](/assets/images/ortho-renders/signaloid-external-illustration-C0-microSD-connected-to-an-existing-microcontroller-platform-withCR.png) |
|:--:| :--:|
| **Figure 1:** C0-microSD populating a breadboard using a microSD breakout board. | **Figure 2:** C0-microSD connected to an existing microcontroller platform. |

You can find example designs that use the on-board LEDs along with instructions on how to synthesize and load them to your device in the `rtl-examples/` directory of the [C0-microSD-Hardware](https://github.com/signaloid/C0-microSD-hardware) repository.

{: .note }
> Using the C0-microSD as a programmable FPGA SoM does not require switching between modes of operation. You only need to set your C0-microSD in **Bootloader** mode.
