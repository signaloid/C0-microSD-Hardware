/*
 *	Copyright (c) 2024, Signaloid.
 *
 *	Permission is hereby granted, free of charge, to any person obtaining a copy
 *	of this software and associated documentation files (the "Software"), to deal
 *	in the Software without restriction, including without limitation the rights
 *	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 *	copies of the Software, and to permit persons to whom the Software is
 *	furnished to do so, subject to the following conditions:
 *
 *	The above copyright notice and this permission notice shall be included in all
 *	copies or substantial portions of the Software.
 *
 *	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 *	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 *	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 *	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 *	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 *	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 *	SOFTWARE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <fcntl.h>
#include <stdbool.h>
#include <errno.h>
#include <assert.h>

#include "C0microSDConstants.h"
#include "C0microSDHostUtils.h"

/*
 *	Function to check if a uint32_t word converts to a specific 4-char word
 */
static bool
checkWord(uint32_t word, char *  checkWord)
{
	if (strlen(checkWord) != sizeof(uint32_t))
	{
		fprintf(stderr, "checkWord must be %lu characters long\n", sizeof(uint32_t));
		exit(EXIT_FAILURE);
	}
	char *  wordAddressAsChar = (char *) &word;
	return memcmp(wordAddressAsChar, checkWord, sizeof(uint32_t)) == 0;
}

ssize_t
hostUtilsReadFromC0microSD(char *  device, void *  destBuffer, size_t bufferSize, off_t offset)
{
	int		fd;
	ssize_t		result;
	off_t		seek_offset;

	/*
	 *	Opening and closing the device for each transaction is needed to force flush
	 */
	fd = open(device, O_RDONLY | O_SYNC | O_DSYNC);
	
	if (fd == -1)
	{
		perror("Error opening device");
		return -1;
	}

	seek_offset = lseek(fd, offset, SEEK_SET);
	if (seek_offset == (off_t)-1)
	{
		perror("Error seeking to target offset");
		close(fd);
		return -1;
	}

	result = read(fd, destBuffer, bufferSize);
	if (result != bufferSize)
	{
		perror("Error reading data from the device");
	}

	close(fd);
	return result;
}

ssize_t
hostUtilsWriteToC0microSD(char *  device, void *  sourceBuffer, size_t bufferSize, off_t offset)
{
	int		fd;
	ssize_t		result;
	off_t		seek_offset;

	/*
	 *	Opening and closing the device for each transaction is needed to force flush
	 */
	fd = open(device, O_WRONLY | O_SYNC | O_DSYNC);
	
	if (fd == -1)
	{
		perror("Error opening device");
		return -1;
	}

	seek_offset = lseek(fd, offset, SEEK_SET);
	if (seek_offset == (off_t)-1)
	{
		perror("Error seeking to target offset");
		close(fd);
		return -1;
	}

	result = write(fd, sourceBuffer, bufferSize);
	if (result != bufferSize)
	{
		perror("Error writing data to the device");
	}
	
	close(fd);
	return result;
}

C0microSDConfigurationStatus
hostUtilsReadC0microSDConfigurationStatus(char *  device)
{
	C0microSDConfigurationStatus	status;
	uint32_t			statusBuffer[kConfigurationStatusWords];
	ssize_t 			readResult;

	readResult = hostUtilsReadFromC0microSD(device, statusBuffer, kConfigurationStatusBytes, kConfigurationStatusOffset);
	if (readResult != kConfigurationStatusBytes)
	{
		exit(EXIT_FAILURE);
	}

	/*
	 *	Decode configuration ID word.
	 */
	if(checkWord(statusBuffer[C0microSDConfigurationStatusRegisterIndexID], "SBLD"))
	{
		status.configuration = kC0microSDConfigurationBootloader;
	}
	else if(checkWord(statusBuffer[C0microSDConfigurationStatusRegisterIndexID], "SSOC"))
	{
		status.configuration = kC0microSDConfigurationSignaloidSoC;
	}
	else
	{
		status.configuration = kC0microSDConfigurationUnknown;
	}

	/*
	 *	Decode configuration version
	 */
	status.versionMajor = (uint16_t)(statusBuffer[C0microSDConfigurationStatusRegisterIndexVersion] & 0xFFFF);
	status.versionMajor = (status.versionMajor >> 8) | (status.versionMajor << 8);
	status.versionMinor = (uint16_t)(statusBuffer[C0microSDConfigurationStatusRegisterIndexVersion] >> 16);
	status.versionMinor = (status.versionMinor >> 8) | (status.versionMinor << 8);

	/*
	 *	Decode configuration state register
	 */
	status.configurationState = statusBuffer[C0microSDConfigurationStatusRegisterIndexState];
	status.configurationSwitching = ((status.configurationState & 0x1) != 0);

	return status;
}

void
hostUtilsPrintC0microSDConfigurationStatus(C0microSDConfigurationStatus status)
{
	printf("Signaloid C0-microSD");

	if (status.configuration == kC0microSDConfigurationBootloader)
	{
		printf(" | Loaded configuration: Bootloader");
	}
	else if (status.configuration == kC0microSDConfigurationSignaloidSoC)
	{
		printf(" | Loaded configuration: Signaloid SoC");
	}
	else
	{
		printf(" | Loaded configuration: UNKNOWN");
	}

	if (status.configuration != kC0microSDConfigurationUnknown)
	{
		printf(" | Version: %d.%d", status.versionMajor, status.versionMinor);
	}
	else
	{
		printf(" | Version: N/A");
	}

	if (status.configurationSwitching)
	{
		printf(" | State SWITCHING");
	}
	else
	{
		printf(" | State IDLE");
	}
	printf("\n");
}

void
hostUtilsAssertSignaloidSoCStatus(C0microSDConfigurationStatus status)
{
	if (status.configuration == kC0microSDConfigurationUnknown)
	{
		fprintf(stderr,"Error: Device is not a C0-microSD.\n");
		exit(EXIT_FAILURE);
		
	}
	else if (status.configuration != kC0microSDConfigurationSignaloidSoC)
	{
		fprintf(stderr, "Error: The device is not in Signaloid SoC mode.");
		fprintf(stderr, "Switch the device to Signaloid SoC mode and try again.\n");
		exit(EXIT_FAILURE);
	}

	if (status.configurationSwitching)
	{
		fprintf(stderr, "Error: Device is in configuration switching mode. ");
		fprintf(stderr, "Power-cycle the device and try again.\n");
		exit(EXIT_FAILURE);
	}	
}

void
hostUtilsWriteSignaloidSoCMOSIBuffer(char *  device, void *  srcBuffer)
{
	ssize_t		res;
	res = hostUtilsWriteToC0microSD(device, srcBuffer, kSignaloidSoCCommonConstantsMOSIBufferSizeBytes, kSignaloidSoCHostConstantsMOSIBufferOffset);
	if (res != kSignaloidSoCCommonConstantsMOSIBufferSizeBytes)
	{	
		exit(EXIT_FAILURE);
	}
}

void
hostUtilsReadSignaloidSoCMISOBuffer(char *  device, void *  destBuffer)
{
	ssize_t		res;
	res = hostUtilsReadFromC0microSD(device, destBuffer, kSignaloidSoCCommonConstantsMISOBufferSizeBytes, kSignaloidSoCHostConstantsMISOBufferOffset);
	if (res != kSignaloidSoCCommonConstantsMISOBufferSizeBytes)
	{	
		exit(EXIT_FAILURE);
	}
}

SignaloidSoCStatus
hostUtilsReadSignaloidSoCStatusRegister(char *  device)
{
	SignaloidSoCStatus	status;
	ssize_t			res;
	res = hostUtilsReadFromC0microSD(device, (void *) &status, sizeof(uint32_t), kSignaloidSoCHostConstantsStatusOffset);
	if (res != sizeof(uint32_t))
	{	
		exit(EXIT_FAILURE);
	}
	return status;
}

uint32_t
hostUtilsReadSignaloidSoCSoCControlRegister(char *  device)
{
	uint32_t	socControl;
	ssize_t		res;
	res = hostUtilsReadFromC0microSD(device, (void *) &socControl, sizeof(uint32_t), kSignaloidSoCHostConstantsSoCControlOffset);
	if (res != sizeof(uint32_t))
	{	
		exit(EXIT_FAILURE);
	}
	return socControl;
}

void
hostUtilsSendSignaloidSoCCommand(char *  device, uint32_t command)
{
	ssize_t res;
	res = hostUtilsWriteToC0microSD(device, (void *) &command, sizeof(uint32_t), kSignaloidSoCHostConstantsCommandOffset);
	if (res != sizeof(uint32_t))
	{	
		exit(EXIT_FAILURE);
	}
}
