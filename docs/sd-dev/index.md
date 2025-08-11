---
layout: default
title: "Signaloid SD-Dev"
has_children: false
nav_order: 4
---

# The SD-Dev carrier board
The Signaloid SD-Dev is a compact carrier board and development system designed for testing and characterizing the Signaloid C0-microSD.

| ![SD-Dev port](/assets/images/sd-dev-pinout.jpg) |
|:--:|
| **Figure 1:** SD-Dev port diagram. |

When you connect the Signaloid SD-Dev to a host computer via USB, it acts as a generic USB-to-SD adapter, exposing one microSD and one full-size SD slot to the host (peripheral mode). Alternatively, you can attach a Raspberry Pi CM4 or CM5 to the carrier board, **producing a compact single-board computer** (SBC) with hot-swappable FPGA modules in a standalone configuration. In this mode, the carrier board provides power measurement capabilities for the on-board FPGA modules and allows you to power cycle them programmatically.

{: .note }
> When using the SD-Dev without an onboard Raspberry Pi compute module (peripheral mode), you must connect it to your host computer via the `PWR+D` port. When using it with a compute module (standalone mode), power it via the PWR port so that you can use the `P0` and `P1` ports to connect peripherals to the Raspberry Pi compute module.

## Getting started with the Signaloid SD-Dev
To get started with the SD-Dev, view the [SD-Dev quickstart guide](https://github.com/signaloid/C0-microSD-Hardware/blob/main/sd-dev-quickstart.pdf).

## Carrier-Board Specifications
- Compact design with the following I/O:
  - 2 USB Type-C downstream ports
  - 1 USB Type-C upstream port
  - 1 USB Type-C upstream power-only port
  - 1 Micro HDMI port
  - JST connectors for SPI and I²C peripherals
- One full-size SD slot and one microSD slot for Signaloid C0-microSD boards or regular storage cards
  - SD card detection
  - Programmable power cycling
  - Power measurement
  - Open-top microSD socket allows you to probe the Signaloid C0-microSD debug pads
- Dual function (peripheral and standalone modes)
- Board outline of 57 x 57 mm

## Flashing the eMMC of a Raspberry Pi compute module.
To flash the onboard eMMC of your Compute Module using the Signaloid SD-Dev board, please refer to the [official Raspberry Pi documentation](https://www.raspberrypi.com/documentation/computers/compute-module.html). Note that the SD-Dev board does not include a `disable eMMC Boot` jumper. Instead, prior to connecting the SD-Dev to the host computer, press and hold the onboard push button and continue with the flashing process.
