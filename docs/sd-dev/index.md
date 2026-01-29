---
layout: default
title: "Signaloid SD-Dev"
has_children: false
nav_order: 4
---

# The SD-Dev carrier board
The Signaloid SD-Dev is a compact carrier board and development system designed for testing and characterizing the Signaloid C0-microSD.

| ![SD-Dev port](/assets/images/signaloid-external-illustration-SD-Dev-port-diagram-withCR.png) |
|:--:|
| **Figure 1:** SD-Dev port diagram. |

## Peripheral mode
When you connect the Signaloid SD-Dev to a host computer via USB, it acts as a generic USB-to-SD adapter, exposing one microSD and one full-size SD slot to the host. 

{: .note }
> When using the SD-Dev without an onboard Raspberry Pi compute module, you must connect it to your host computer via the `PWR+D` port.

## Standalone mode
You can attach a Raspberry Pi CM4 or CM5 to the carrier board, **producing a compact single-board computer** (SBC) with hot-swappable FPGA modules in a standalone configuration. In this mode, the carrier board provides power measurement capabilities for the on-board FPGA modules and allows you to power cycle them programmatically.

{: .note }
> When using the SD-Dev with an onboard Raspberry Pi compute module, power it via the `PWR` port so that you can use the `P0` and `P1` ports to connect peripherals to the Raspberry Pi compute module.

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

## Raspberry Pi compute module as a USB Serial gadget
When using the SD-Dev in standalone mode, with a Raspberry Pi compute module attached, you can configure the Raspberry Pi to act as a USB serial gadget, i.e. access it through its USB serial port. Optionally, you can also attach a console to that serial port.

To do that:  
1. Edit the `/boot/firmware/config.txt` file:
	- Comment out the line `otg_mode=1`.
	- Add this `dtoverlay=dwc2,dr_mode=peripheral` at the end of the file.
2. Create the `/etc/modules-load.d/otg.conf` file with the following content:
	```
	dwc2
	g_serial
	```
3. Reboot
4. Connect your SD-Dev to your host machine using the `PWR+D` USB-C port.
5. Access the serial port from your host machine using tools like `screen` on Linux/Mac, or `minicom` on Windows.

At this point your Raspberry Pi will create a `/dev/ttyGS0` serial port, which you can read from and write to from both the Raspberry Pi and the host machine.

To attach a console to `ttyGS0`, so that you can have access to a full Raspberry Pi terminal from your host machine:
1. Symlink the `getty` service:
	```sh
	sudo ln -s /lib/systemd/system/getty@.service /etc/systemd/system/getty.target.wants/getty@ttyGS0.service
	```
2. Enable and start the service:
	```sh
	sudo systemctl enable --now getty@ttyGS0.service
	```

## Raspberry Pi compute module as a USB Ethernet gadget
When using the SD-Dev in standalone mode, with a Raspberry Pi compute module attached, you can configure the Raspberry Pi to act as a USB Ethernet gadget, i.e. attach it to a host machine using USB-C and access it via SSH.

To do that:  
1. Edit the `/boot/firmware/config.txt` file:
	- Comment out the line `otg_mode=1`.
	- Add this `dtoverlay=dwc2,dr_mode=peripheral` at the end of the file.
2. Create the `/etc/modules-load.d/otg.conf` file with the following content:
	```
	dwc2
	g_ether
	```
3. Reboot
4. Connect your SD-Dev to your host machine using the `PWR+D` USB-C port.
5. Add an ethernet connection:
	```sh
	sudo nmcli con add type ethernet con-name usb-otg ifname usb0
	```
6. Activate the connection:
	```sh
	sudo nmcli con up usb-otg
	```
7. Identify your Raspberry Pi IP address:
	```sh
	ip addr show dev usb0
	```
8. Connect to your Raspberry Pi from your host machine via SSH using the IP from the previous step.

If everything works correctly, you can automate the connection activation by creating a `systemd` service:
1. Create the `/lib/systemd/system/usb_otg.service` file with the following content:
	```
	[Unit]
	Description=USB Ethernet gadget
	After=NetworkManager.service
	Wants=NetworkManager.service
	
	[Service]
	Type=oneshot
	RemainAfterExit=yes
	ExecStart=/bin/sh -c 'nmcli con up usb-otg'
	
	[Install]
	WantedBy=sysinit.target
	```
2. Enable and start the service:
	```sh
	sudo systemctl enable --now usb_otg.service
	```
