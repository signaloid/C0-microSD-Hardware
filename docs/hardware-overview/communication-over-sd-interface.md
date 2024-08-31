---
layout: default
parent: "Hardware Overview"
title: "Communication over the SD Interface"
nav_order: 2
---

# Communication over the SD Interface
The C0-microSD is designed to communicate with host devices over the SD interface. When connected to a host computer, the device presents itself as a 20.2 MB (19.3 MiB) unformatted block storage device. All communication is achieved with block read and write operations which the host initiates. This is true both when the device is in **Bootloader** mode, or in **Signaloid SoC** mode.

{: .note }
> The communication over the SD interface is done using block read and write operations, and not an [SDIO extension](https://www.sdcard.org/developers/sd-standard-overview/sdio-isdio/) of the SD interface.

## Bootloader communication example
In this example, the C0-microSD is in **Bootloader** mode, and connected to a host computer that runs macOS. To flash a new bitstream to the Custom User Bitstream section of the device you can use the `dd` command. Here, we assume that the device is located in `/dev/disk4/`, and that the bitstream file is `bitstream.bin`.

```console
% sudo dd if=bitstream.bin of=/dev/disk4 seek=3072 bs=512

203+1 records in
203+1 records out
104090 bytes transferred in 1.904253 secs (54662 bytes/sec)
```

In the example above, the `seek` argument is calculated by taking the decimal representation of the `USER_BITSTREAM_OFFSET` (see /hardware-overview/bootloader-addresssing.html), and dividing it by the block size (`bs = 512`). For all the bootloader operations you can use the `C0_microSD_toolkit.py` script that you can find [here](https://github.com/signaloid/C0-microSD-utilities).

## Signaloid SoC communication example
In this example, the C0-microSD is in **Signaloid SoC** mode, and connected to a host computer that runs macOS. We assume that the device is located in `/dev/disk4/`. Here, we communicate with the C0-microSD using a C host application to set the `command` register to `0x00000001`.

```c
#include <stdio.h>
#include <errno.h>
#include <stdint.h>

main(void)
{
	char*		devicePath = "/dev/disk4";
	uint32_t	command = 0x00000001;
	uint32_t	commandRegisterOffset = 0x00010000;
	
	/*
	 *	Open the C0-microSD device
	 */
	fd = open(devicePath, O_WRONLY | O_SYNC | O_DSYNC);
	if (fd == -1)
	{
		perror("Error opening device");
		return -1;
	}

	/*
	 *	Seek to offset for command register
	 */
	seek_offset = lseek(fd, commandRegisterOffset, SEEK_SET);
	if (seek_offset == (off_t)-1)
	{
		perror("Error seeking to target offset");
		close(fd);
		return -1;
	}

	/*
	 *	Write command register data
	 */
	result = write(fd, &command, sizeof(uint32_t));
	if (result != bufferSize)
	{
		perror("Error writing data to the device");
	}
	
	/*
	 *	Close the C0-microSD device
	 */
	close(fd);
}
```

The `commandRegisterOffset` is determined based on the Signaloid SoC [communication scheme](/hardware-overview/signaloid-core/communication-scheme.html) specifications. You can find header files and helper functions for building your own C and Python based host applications [here](https://github.com/signaloid/C0-microSD-utilities?tab=readme-ov-file#using-the-c0_microsd_toolkitpy-tool).
