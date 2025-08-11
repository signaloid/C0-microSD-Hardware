---
layout: default
grand_parent: "Hardware Overview"
parent: "Signaloid SoC"

title: "Communication Scheme"
nav_order: 1
---

# Signaloid SoC Communication Scheme
Communication between the device application that runs on the Signaloid SoC, and the host application that runs on the host device, is achieved over the SD interface via block read and write commands. Specifically, the Signaloid SoC supports control and status registers, as well as data buffers, for communication with the host device, which are exposed in the Signaloid SoC as memory-mapped I/O (MMIO). Following are the memory addresses used by the device application to access them:

## MMIO Communication registers

| Register      | Memory Address | Size    | Device Operation |
| ------------- | -------------- | ------- | ---------------- |
| `status`      | `0x40000000`   | 4 Bytes | W                |
| `SoC Control` | `0x40000004`   | 4 Bytes | W                |
| `command`     | `0x40000008`   | 4 Bytes | R                |


### `status` register
This register is set by the device application and can be used to declare the current status of the application.

### `SoC Control` register
This register is set by the device application to control SoC peripherals, and can be read by the host via the SD interface.

| Register Bit | Usage                 |
| ------------ | --------------------- |
| 31:2         | Reserved              |
| 1            | Set `CONFIG_DONE` pin |
| 0            | Set onboard red LED   |

### `command` register
This register can be set by the host application, and read by the device application. It is used for sending commands to the Signaloid SoC.

{: .note }
> The specific values of the `command` and `status` registers for communication between the host and the device are application dependent.

## MMIO Data buffers
Additionally, the core offers data buffers for extended I/O

| Register              | Memory Address | Size  | Device Operation |
| --------------------- | -------------- | ----- | ---------------- |
| `MISO_BUFFER_ADDRESS` | `0x40010000`   | 4 KiB | W                |
| `MOSI_BUFFER_ADDRESS` | `0x40020000`   | 4 KiB | R                |


### `MOSI_BUFFER`
This is the MOSI (Master Out Slave In) data buffer for sending data from the host application to the device application.

### `MISO_BUFFER`
This is the MISO (Master In Slave Out) data buffer for sending data from the device application to the host application.

## Device application example
In a C based device application, you can store the value `0x00000002` to the `status` register in the following way:

```c
#include <stdint.h>

enum {
	kSignaloidCoreDeviceConstantsStatusAddress = 0x40000000
}

main(void)
{
	volatile uint32_t *	mmioStatus = (uint32_t *) kSignaloidCoreDeviceConstantsStatusAddress;
	...

	*mmioStatus = 0x00000002;
}

```

## SD interface addressing
The table below shows the address offsets for communication with the C0-microSD over the SD interface while in **Signaloid SoC** mode. Note that the addressing scheme for reading and writing to the MMIO buffers and registers from the SD host differs from the addressing scheme from the SoC itself. For example, when you want to write to the `command` register from your host application, the block device offset is `0x10000`, but to read the same register from your SoC application you need to access the `0x40000008` memory address.

| Address space                 | Address Start | Size    | Host Operation | Description                       |
| ----------------------------- | ------------- | ------- | -------------- | --------------------------------- |
| `STATUS_REGISTER_OFFSET`      | `0x000000`    | 4 Bytes | R              | Offset for `status` register      |
| `SOC_CONTROL_REGISTER_OFFSET` | `0x000004`    | 4 Bytes | R              | Offset for `SoC control` register |
| `COMMAND_REGISTER_OFFSET`     | `0x10000`     | 4 Bytes | W              | Offset for `command` register     |
| `MOSI_BUFFER_OFFSET`          | `0x50000`     | 4 KiB   | W              | Offset for `MOSI` buffer          |
| `MISO_BUFFER_OFFSET`          | `0x60000`     | 4 KiB   | R              | Offset for `MISO` buffer          |

Additionally, the following address offsets allow the host device to verify the current active configuration, as well as switch back to the **Bootloader** mode:

| Address space                     | Address Start | Size    | Host Operation | Description                          |
| --------------------------------- | ------------- | ------- | -------------- | ------------------------------------ |
| `CONFIGURATION_ID_OFFSET`         | `0x020000`    | 4 Bytes | R              | Offset for configuration ID          |
| `CONFIGURATION_VERSION_OFFSET`    | `0x020004`    | 4 Bytes | R              | Offset for configuration version     |
| `CONFIGURATION_STATE_OFFSET`      | `0x020008`    | 4 Bytes | R              | Offset for configuration state       |
| `BOOTLOADER_SWITCH_CONFIG_OFFSET` | `0x040000`    | 4 Bytes | W              | Offset for switching operation modes |


### `CONFIGURATION_ID_OFFSET`
This 4-byte word stores the ID of the active configuration (in this case the Signaloid SoC). The toolkit uses the ID to identify the active mode of operation of the C0-microSD.

### `CONFIGURATION_VERSION_OFFSET`
This 4-byte word stores the current version of the active configuration (in this case the Signaloid SoC). 

### `CONFIGURATION_STATE_OFFSET`
This 4-byte word stores the current state of the active configuration (in this case the Signaloid SoC). Currently, the toolkit uses this value to verify whether the C0-microSD is in `SWITCHING` state.

### `BOOTLOADER_SWITCH_CONFIG_OFFSET`
This offset is used for switching between operation modes. To achieve this, you can write the 4-byte word `SBLD` (ASCII Encoded) to this offset.
