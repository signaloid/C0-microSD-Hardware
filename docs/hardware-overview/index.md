---
layout: default
title: "Hardware Overview"
has_children: true
nav_order: 2
---

# Hardware Overview
The Signaloid C0-microSD is based on the iCE40 FPGA from Lattice Semiconductor. In addition to the iCE40 FPGA, the Signaloid C0-microSD SOM contains 128Mbit of serial NOR flash for storing bitstreams, firmware, and user data.

## Features
- [ICE40UP5K](https://www.latticesemi.com/en/Products/FPGAandCPLD/iCE40UltraPlus) FPGA
  - 5280 logic cells
  - 128 Kbit (16 KB) dual-port Block RAM
  - 1 Mbit (128 KB) Single-Port RAM
  - One PLL, two SPI, and two I2C hard IPs
  - Two internal oscillators (10 kHz and 48 MHz)
  - 8 DSPs (16x16 multiply + 32-bit accumulate)
  - Hard IP PWM (for the on-board LEDs)
- [AT25QL128A](https://www.renesas.com/us/en/products/memory-logic/non-volatile-memory/spi-nor-flash/at25ql128a-128mbit-17v-minimum-spi-serial-flash-memory-dual-io-quad-io-and-qpi-support) SPI Flash
  - 128 Mbit (16 MB) non-volatile memory
  - 50 MHz typical operating frequency
  - 133 MHz maximum operating frequency (fast read)
  - Low power dissipation
- Programmable I/O pins
  - Two on-board leds (one red and one green), for status indication
  - Six programmable I/O pins by repurposing the microSD pads as I/O accessible from custom designs mapped to the FPGA.
  - Five additional programmable I/O via test pads.
- Built-in Signaloid C0 RISC-V SoC
- Built-in bootloader, allowing you to load new FPGA bitstreams or RISC-V applications via the SD interface
