---
layout: default
parent: "Guides"
title: "Switch Operation Mode"
nav_order: 2
---

# Switch between Operation Modes
You can use the `C0_microSD_toolkit.py`, which you can find [here](https://github.com/signaloid/C0-microSD-utilities), to switch between modes of operation.

1. Insert the C0-microSD into your computer.

2. Identify the C0-microSD device path. For this example, we assume the device path is `/dev/disk4`. You can find more details on how to identify your C0-microSD [here](/guides/identify-c0-microsd.html).

3. Verify the active mode. 
    - A solid red LED means that the C0-microSD is in Bootloader mode (Figure 1).
    - A solid green LED means that the C0-microSD is in Signaloid Soc mode (Figure 2).

    | ![inserted C0-microSD with red led on](/assets/images/macbook-animations/inserted-red-led.png) | ![inserted C0-microSD with green led on](/assets/images/macbook-animations/inserted-green-led.png) |
    | :--------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------: |
    |                    **Figure 1:** C0-microSD is in **Signaloid Soc** mode.                     |                        **Figure 2:** C0-microSD is in **Bootloader** mode.                         |

4. Run `sudo python3 ./C0_microSD_toolkit.py -t /dev/disk4 -s` to switch operation mode. If this is successful, the opposite LED of the one that is solid should start blinking (Figures 3 and 4).

    | ![inserted C0-microSD switching from Bootloader to Signaloid SoC](/assets/images/macbook-animations/switching-from-bootloader-to-signaloid-core.gif) | ![inserted C0-microSD switching from Signaloid SoC to Bootloader](/assets/images/macbook-animations/switching-from-signaloid-core-to-bootloader.gif) |
    | :---------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: |
    |                                 **Figure 3:** C0-microSD in **Bootloader** mode switching to **Signaloid Soc** mode.                                 |                                 **Figure 4:** C0-microSD in **Signaloid Soc** mode switching to **Bootloader** mode.                                 |

    Following is an example output of switching the operation mode of a C0-microSD from **Signaloid Soc** mode to **Bootloader** mode:

    ```
    % sudo python3 C0_microSD_toolkit.py -t /dev/disk4 -s

    Signaloid C0-microSD | Loaded configuration: Signaloid Soc | Version: 1.0 | State IDLE
    Switching device boot mode from Signaloid Soc to Bootloader...
    Device configured successfully. Power cycle the device to boot in new mode.
    Done.
    ```

5. Power-cycle the C0-microSD to load new configuration mode. This means that the LED that was previously flashing, should now be constantly on (Figures 5 and 6).

    | ![power cycling from Bootloader to Signaloid SoC](/assets/images/macbook-animations/switch-from-bootloader-to-signaloid-core.gif) | ![power cycling from Signaloid SoC to Bootloader](/assets/images/macbook-animations/switch-from-signaloid-core-to-bootloader.gif) |
    | :--------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------: |
    |                          **Figure 5:** Power cycling the C0-microSD to switch to **Signaloid Soc** mode.                          |                            **Figure 6:** Power cycling the C0-microSD to switch to **Bootloader** mode.                            |

{: .note }
> In the visualizations above, the C0-microSD has been inserted into a common off-the-shelf microSD to SD adapter.

## Loading your custom user bitstream.
To use the Signaloid C0-microSD in **Custom User Bitstream** mode, you must first switch the device to **Bootloader** mode following the procedure above. After doing that, power it on without an SD-protocol host present. You can achieve that by powering it using a microSD breakout board, or by connecting it to the Signaloid SD-Dev and powering it from the PWR USB-C port.
