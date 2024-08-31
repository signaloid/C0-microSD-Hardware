---
layout: default
parent: "Hardware Overview"
title: "Bootloader Addressing"
nav_order: 3
---

# Bootloader Addressing
Communicating with the C0-microSD is achieved through block read and write operations. The following specification contains the different address offsets you can use to communicate with the device while in **Bootloader** mode.

| Address space                      | Address Start | Size    | Operation | Description                             |
| ---------------------------------- | ------------- | ------- | --------- | --------------------------------------- |
| `CONFIGURATION_ID_OFFSET`          | `0x020000`    | 4 Bytes | R         | Offset for configuration ID             |
| `CONFIGURATION_VERSION_OFFSET`     | `0x020004`    | 4 Bytes | R         | Offset for configuration version        |
| `CONFIGURATION_STATE_OFFSET`       | `0x020008`    | 4 Bytes | R         | Offset for configuration state          |
| `BOOTLOADER_SWITCH_CONFIG_OFFSET`  | `0x040000`    | 4 Bytes | W         | Offset for switching operation modes    |
| `BOOTLOADER_UNLOCK_OFFSET`         | `0x060000`    | 4 Bytes | W         | Offset for locking/unlocking bootloader |
| `BOOTLOADER_BITSTREAM_OFFSET`*     | `0x080000`    | 512 KiB | R/W\*\*   | Bootloader bitstream region             |
| `SIGNALOID_CORE_BITSTREAM_OFFSET`* | `0x100000`    | 512 KiB | R/W\*\*   | Signaloid SoC bitstream region          |
| `USER_BITSTREAM_OFFSET`*           | `0x180000`    | 512 KiB | R/W       | Custom user bitstream region            |
| `USER_DATA_OFFSET`*                | `0x200000`    | 14 MiB  | R/W       | User data space region                  |

<p style="font-size:14px; color:#999">
* Address space corresponds to on-board flash memory data.<br>
** Address space needs unlocking for write operation.
</p>

### `CONFIGURATION_ID_OFFSET`
This 4-byte word stores the ID of the active configuration (in this case the Bootloader). This is used by the toolkit to identify the active mode of operation of the C0-microSD.

### `CONFIGURATION_VERSION_OFFSET`
This 4-byte word stores the current version of the active configuration (in this case the Bootloader). Specifically:

| Active Configuration |  Word   |
| :------------------: | :-----: |
|      Bootloader      | b"SBLD" |
|    Signaloid SoC    | b"SSOC" |


### `CONFIGURATION_STATE_OFFSET`
This 4-byte word stores the current state of the active configuration (in this case the Bootloader). Currently, this is used by the toolkit to verify whether the C0-microSD is in `SWITCHING` state.

### `BOOTLOADER_SWITCH_CONFIG_OFFSET`
This offset is used for switching between operation modes. To achieve this, you can write the 4-byte word `SBLD` (ASCII encoded) to this offset.

### `BOOTLOADER_UNLOCK_OFFSET`
Address spaces `BOOTLOADER_BITSTREAM_OFFSET` and `SIGNALOID_CORE_BITSTREAM_OFFSET` are locked by default. This is to prevent accidental overriding of the Bootloader or Signaloid SoC bitstreams, which could render the device inoperable. To flash these address spaces, you must first write a special 4-byte word (ASCII encoded `UBLD`) to this offset. You can re-lock the bootloader by writing anything else to the same offset.

### `BOOTLOADER_BITSTREAM_OFFSET`
In this address space, the Bootloader bitstream is stored. You first need to unlock the bootloader to write to this address space.

### `SIGNALOID_CORE_BITSTREAM_OFFSET`
In this address space, the Signaloid SoC bitstream is stored. You first need to unlock the bootloader to write to this address space.

### `USER_BITSTREAM_OFFSET`
In this address space, the custom user bitstream is stored.

### `USER_DATA_OFFSET`
This 14 MiB address space can be used to store data, or binary files to be used either by the custom user bitstream, or the Signaloid SoC configuration. Specifically, the Signaloid SoC initializes its memory by copying the first 128 KiB section of this address space, before starting its execution.

## Important notes
The SD interface mandates the support of read and write operations for the entire available address space. This is in contrast to the supported operation in each address space as described above. For that reason, the following rules apply:

- **R**: Reading from this address space will return valid data. Writing to this address space will succeed, but will have no effect.
- **W**: Reading from this address will succeed, but will return invalid data. Writing data to this address space will succeed, and will have an effect on the device. 
- **R/W**: Reading from this address space will return valid data. Writing data to this address space will succeed, and will have an effect on the device.

- **N/A**: Reading from this address will succeed, but will return invalid data. Writing to this address space will succeed, but will have no effect.

Address spaces that are not mentioned in the table above can be considered as **N/A**.
