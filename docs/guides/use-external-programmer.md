---
layout: default
parent: "Guides"
title: "Use External Programmer"
nav_order: 4
---

# Flash the C0-microSD Using an External Programmer
You can flash the C0-microSD on-board SPI flash chip using an external programmer, and the `iceprog` toolkit, which is part of the [Icestorm](https://github.com/YosysHQ/icestorm) suite. This example uses the [Tigard](https://github.com/tigard-tools/tigard) board, which can interface with SPI ports that operate at `1.8V` and is compatible with the `iceprog` toolkit.

{: .warning }
> Do not attempt to manually flash the C0-microSD using an external programmer unless you know what you are doing. Overriding the Bootloader bitstream, the Signaloid SoC bitstream, or the first 512 KiB of the non-volatile memory may disable the bootloader and SD interface of the C0-microSD. Nevertheless, this method can be used to re-flash the Bootloader and Signaloid SoC in case they are corrupted, and bring the device to its initial state. You can find the official C0-microSD configuration bitstreams [here](https://github.com/signaloid/C0-microSD-hardware) 

1. Make sure that the `Tigard` board is configured correctly, with the `Target` switch set to `1.8V` and the `Mode` switch set to `JTAG/SPI` (Figure 1).

2. Connect the C0-microSD to the `Tigard` board as follows (Figure 1):

    | C0-microSD Pin   | SilkScreen | Tigard Board Pin | Notes                                              |
    | ---------------- | ---------- | ---------------- | -------------------------------------------------- |
    | `VDD`            | \-         | \-               | Supply voltage of 3.3V must be externally provided |
    | `VSS`            | \-         | GND              | Ground                                             |
    | `CONFIG_SCLK`    | C          | TCK              | Clock pin of SPI configuration port                |
    | `CONFIG_DONE`    | D          | \-               | Configuration done pin, not connected              |
    | `CONFIG_CRESET_N` | R          | SRST             | FPGA reset pin (active low)                        |
    | `CONFIG_MISO`    | O          | TDO              | MISO pin of SPI configuration port                 |
    | `CONFIG_CS_N`    | S          | TRST             | Chip select of SPI configuration port (active low) |
    | `CONFIG_MOSI`    | I          | TDI              | MOSI pin of SPI configuration port                 |


    {: .note }
    > The form-factor of the C0-microSD requires the use of special tooling for accessing the configuration pins mentioned above. We recommend one of the following methods:
    > - Using a probing system like [PCBite](https://sensepeek.com/) from SensePeek.
    > - Using a data recovery jig like the [iDili](https://www.amazon.com/iDili-Probe-Repair-Flying-Jumper/dp/B0CDGNGVVY) probe, the [PC-3000](https://blog.acelab.eu.com/pc-3000-flash-spider-board-adapter-how-to-use-it.html) spider board, or something similar.
    > - Soldering small wires to the bottom pads. This is a cheap solution but might cause fitment issues if you don't thoroughly clean the pads from any remaining solder after you have completed the flashing process.


3. Connect a power supply of `3.3V` to the C0-microSD, make sure that the ground pins of the power supply and the `Tigard` board are tied together (Figure 1).

    | <img src="/assets/images/diagrams/signaloid-external-illustration-Tigard-connection-diagram-withCR.png"> |
    |:--:|
    | **Figure 1:** Tigard connection diagram using the pads located at the bottom layer of the C0-microSD. |

4. Use the `iceprog` tool from the `IceStorm` suite to flash a new bitstream to the device. Assuming your bitstream is named `c0-microsd.bin` use the following command and wait for the flashing process to finish:

    ```
    iceprog -I -p B c0-microsd.bin

    init..
    cdone: high
    reset..
    cdone: high
    flash ID: 0x1F 0x42 0x18 0x1F 0x42 0x18 0x1F 0x42 0x18 0x1F 0x42 0x18 0x1F 0x42 0x18 0x1F 0x42
    0x18 0x1F 0x42 0x18 0x1F 0x42 0x18 0x1F 0x42 0x18 0x1F 0x42 0x18 0x1F 0x42 0x18 0x1F 0x42
    file size: 104157
    erase 64kB sector at 0x000000..
    erase 64kB sector at 0x010000..
    programming..
    done.
    reading..
    VERIFY OK
    cdone: high
    Bye.
    ```

    A console message stating `VERIFY OK` means that flashing the new bitstream was successful. You need to power cycle the device for the new bitstream to take effect.
