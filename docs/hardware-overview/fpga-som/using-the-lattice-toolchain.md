---
layout: default
grand_parent: "Hardware Overview"
parent: "FPGA System on Module"

title: "Using the Proprietary Toolchain"
nav_order: 3
---

# Using the proprietary toolchain
Lattice Semiconductor provides a free license for Lattice Radiant, their latest CAD suite that supports the iCE40 FPGA. You can find more details in the official Lattice Radiant [product page](https://www.latticesemi.com/latticeradiant).

## PDC file reference
Similar to the OSS toolchain, Lattice Radiant uses post-synthesis constraint files to map the design's pinout to the physical chip. Following is an example `.pdc` pinout configuration file for the C0-microSD. You can create a new post-synthesis constraint file in your project by navigating to `File -> New -> File`, and selecting `Post-Synthesis Constraint Files` in the pop-up window.


```conf
#
#	Copyright (c) 2021 – 2024 Signaloid.
#	All rights reserved.
#

ldc_set_location -site {A1} [get_ports SD_DAT0]		# GPIO pin connected to the SD bus DAT0
ldc_set_location -site {A2} [get_ports SD_DAT1]		# GPIO pin connected to the SD bus DAT1
ldc_set_location -site {E5} [get_ports SD_DAT2]		# GPIO pin connected to the SD bus DAT2
ldc_set_location -site {F5} [get_ports SD_DAT3]		# GPIO pin connected to the SD bus DAT3
ldc_set_location -site {A4} [get_ports SD_CMD]		# GPIO pin connected to the SD bus CMD
ldc_set_location -site {B3} [get_ports SD_CLK]		# GPIO pin connected to the SD bus CLK

ldc_set_location -site {A5} [get_ports LED_GREEN]	# Green status LED
ldc_set_location -site {B5} [get_ports LED_RED]		# Red status LED

ldc_set_location -site {F1} [get_ports CONFIG_MOSI]	# MOSI pin of SPI configuration port
ldc_set_location -site {E1} [get_ports CONFIG_MISO]	# MISO pin of SPI configuration port
ldc_set_location -site {D1} [get_ports CONFIG_SCK]	# Clock pin of SPI configuration port
ldc_set_location -site {C1} [get_ports CONFIG_CS_N]	# Chip select of SPI configuration port (active low)
ldc_set_location -site {D3} [get_ports CONFIG_CDONE]	# Configuration done pin
```

## Generating and flashing your custom bitstream
To generate the correct format of bitstream for your C0-microSD, select and edit your active strategy, navigate to the `Bitstream` section, and make sure that the `Output Format` option is set to `Bit File (Binary)`. You can find details on how to flash your custom bitstream [here](/guides/flash-data-to-c0-microsd.html).
