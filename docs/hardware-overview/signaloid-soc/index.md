---
layout: default
title: "Signaloid SoC"
parent: "Hardware Overview"
has_children: true
nav_order: 5
---

# Using the Signaloid C0-microSD as a Hot-Pluggable Co-processor Module
The Signaloid C0-microSD comes with a built-in version of Signaloid’s C0 RISC-V processor, which you can use to run your applications. In this mode of operation, host computers can use the SD protocol to exchange data with applications running on the Signaloid C0-microSD, either by creating custom applications that run on the host platform and which access the SD storage device, or using Unix tools such as `dd`. Applications running on the Signaloid’s C0 processor in the Signaloid C0-microSD, can take advantage of a subset of Signaloid’s [uncertainty-tracking technology](https://signaloid.com/technology) to quantify how uncertainties in data affect their outputs.

<!-- | ![Signaloid SoC on C0-microSD illustration](/assets/images/ortho-renders/C0-microSD-signaloid-core/C0-microSD-with-signaloid-core.png) | ![Signaloid SoC on Macbook](/assets/images/macbook-animations/inserted-green-led.png) |
| :-------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------: |
|                                        **Figure 1:** Signaloid SoC on C0-microSD illustration.                                         |        **Figure 2:** C0-microSD on Signaloid SoC mode used as a co-processor.         | -->

<div style="max-width: 420px; margin-left: auto; margin-right: auto; margin-top: 16px">
    <table style = "text-align: center;">
    <tr>
        <td><img src="/assets/images/macbook-animations/signaloid-external-illustration-C0-microSD-inserted-Signaloid-SoC-mode-withCR.png" alt="Signaloid SoC in Macbook"/></td>
    </tr>
    <tr>
        <td><b>Figure 1:</b> C0-microSD on Signaloid SoC mode used as a co-processor.</td>
    </tr>
    </table>
</div>

## Signaloid SoC specifications:
The Signaloid SoC is based on the open-source [PicoRV32](https://github.com/YosysHQ/picorv32) project, which we have extended to support a subset of Signaloid’s uncertainty-tracking technology, as well as communication with the host device over the SD interface.

|  ISA  | Operating Frequency | Available Memory |
| :---: | :-----------------: | :--------------: |
| RV32I |        12MHz        |      128KiB      |

## Developing applications for the Signaloid SoC
The Signaloid SoC can run custom user code (device application), and work in conjunction with an application that runs on the host machine (host application). The host application is responsible for communicating with the device application over the SD interface, via block read and write operations. You can find more details on the Signaloid SoC communication scheme [here](/hardware-overview/signaloid-soc/communication-scheme.html).

You can use the [official RISC-V GNU toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain) to compile and run your applications on the Signaloid SoC. We provide example C applications that use the Signaloid SoC, along with host applications and instructions on how to compile them [here](https://github.com/signaloid/C0-microSD-Hardware).

The toolchain for compiling applications that can take advantage of the uncertainty-tracking functionality will eventually be available through the [Signaloid Cloud Developer Platform](https://get.signaloid.io) (SCDP). You can find pre-compiled example applications with uncertainty-tracking capabilities that run on the C0-microSD [here](https://github.com/signaloid?q=Signaloid-C0-microSD-Demo).
