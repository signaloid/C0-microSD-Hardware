---
layout: default
grand_parent: "Hardware Overview"
parent: "FPGA System on Module"

title: "Using the Open-Source Toolchain"
nav_order: 2
---

# Using the open-source toolchain (OSS)
You can use the open-source toolchain to synthesize custom bitstreams for the C0-microSD. The open-source toolchain includes [Yosys](https://github.com/YosysHQ/yosys), [NextPnR](https://github.com/YosysHQ/nextpnr/tree/master) and [Icestorm](https://github.com/YosysHQ/icestorm). You can install the toolchain by compiling it for your environment, or find pre-compiled binaries [here](https://github.com/YosysHQ/oss-cad-suite-build).

## PCF file reference
In the Place and Route stage of the workflow, `NextPnR` can use a `.pcf` file to describe physical constraints. You can find more information in the [NextPnR documentation](https://github.com/YosysHQ/nextpnr/blob/master/docs/ice40.md).

Following is an example `.pcf` pinout configuration file for the C0-microSD.

```conf
#
#	Copyright (c) 2021 – 2024 Signaloid.
#	All rights reserved.
#

set_io		SD_DAT0			A1	# GPIO pin connected to the SD bus DAT0
set_io		SD_DAT1			A2	# GPIO pin connected to the SD bus DAT1
set_io		SD_DAT2			E5	# GPIO pin connected to the SD bus DAT2
set_io		SD_DAT3			F5	# GPIO pin connected to the SD bus DAT3
set_io		SD_CMD			A4	# GPIO pin connected to the SD bus CMD
set_io		SD_CLK			B3	# GPIO pin connected to the SD bus CLK

set_io		LED_GREEN		A5	# Green status LED
set_io		LED_RED			B5	# Red status LED

set_io		CONFIG_MOSI		F1	# MOSI pin of SPI configuration port
set_io		CONFIG_MISO		E1	# MISO pin of SPI configuration port
set_io		CONFIG_SCLK		D1	# Clock pin of SPI configuration port
set_io		CONFIG_CS_N		C1	# Chip select of SPI configuration port (active low)
set_io		CONFIG_CDONE		D3	# Configuration done pin
```

## Generating and flashing your custom bitstream
You can generate the final bitstream configuration for the C0-microSD using the `icepack` tool, which is part of the `Icestorm` toolkit. You can find details on how to flash your custom bitstream [here](/guides/flash-data-to-c0-microsd.html).
