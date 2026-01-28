---
layout: default
grand_parent: "Hardware Overview"
parent: "Signaloid SoC"

title: "Memory Map"
nav_order: 0
---

# Signaloid SoC Memory Map
The Signaloid SoC features 128KiB of internal memory (SPRAM) which is dedicated for the user application. Upon system reset, the SoC initializes itself by copying the first 128KiB of data that are stored in the _user data_ sector of the onboard non-volatile flash (see `USER_DATA_OFFSET` sector of the [bootloader addressing](/hardware-overview/bootloader-addressing.html) section), before starting its execution from address `0x00`. Following is a detailed diagram of the memory map of the SoC:

| <img src="/docs/assets/images/diagrams/signaloid-external-illustration-Signaloid-C0-microSD-memory-map-updated-withCR.png" style="width:50%"> |
|:--:|
| **Figure 1:** Signaloid SoC memory map. |
