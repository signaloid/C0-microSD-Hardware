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

#pragma once

/*
 *	The following constants are used by the host application for communicating with active
 *	configuration of the C0-microSD.
 */
enum C0microSDConstants
{
	kConfigurationStatusOffset		= 0x20000,
	kConfigurationStatusWords		= 3,
	kConfigurationStatusBytes		= 12,
};

/*
 *	Configuration ID. This is used to identify the currently loaded 
 *	configuration on the C0-microSD
 */
typedef enum
{
	kC0microSDConfigurationUnknown		= 0, /* Unknown configuration id */
	kC0microSDConfigurationBootloader	= 1, /* Bootloader configuration id */
	kC0microSDConfigurationSignaloidSoC	= 2, /* Signaloid SoC configuration id */
} C0microSDConfiguration;

enum SignaloidSoCCommonConstants
{
	/*
	 *	MOSI buffer size in number of bytes and words
	 */
	kSignaloidSoCCommonConstantsMOSIBufferSizeBytes	= 4096,
	kSignaloidSoCCommonConstantsMOSIBufferSizeWords	= 1024,
	/*
	 *	MISO buffer size in number of bytes and words
	 */
	kSignaloidSoCCommonConstantsMISOBufferSizeBytes	= 4096,
	kSignaloidSoCCommonConstantsMISOBufferSizeWords	= 1024,
};

/*
 *	The following constants are used by the host application for the Memory Mapped I/O
 *	of the Signaloid SoC. These denote offsets for communicating over the SD interface.
 */
enum SignaloidSoCHostConstants
{
	/*
	 *	Memory-mapped I/0 (MMIO) register offsets
	 */
	kSignaloidSoCHostConstantsStatusOffset		= 0x00000,
	kSignaloidSoCHostConstantsSoCControlOffset	= 0x00004,	
	kSignaloidSoCHostConstantsCommandOffset	= 0x10000,
	/*
	 *	Memory-mapped I/0 (MMIO) MISO and MOSI buffer offsets
	 */
	kSignaloidSoCHostConstantsMOSIBufferOffset	= 0x50000,
	kSignaloidSoCHostConstantsMISOBufferOffset	= 0x60000,
};

/*
 *	The following constants are used by the Signaloid SoC application for the Memory Mapped I/O
 *	of the device. These denote memory addresses in the Signaloid SoC.
 */
enum SignaloidSoCDeviceConstants
{
	/*
	 *	Memory-mapped I/0 (MMIO) register addresses
	 */
	kSignaloidSoCDeviceConstantsStatusAddress	= 0x40000000,
	kSignaloidSoCDeviceConstantsSoCControlAddress	= 0x40000004,	
	kSignaloidSoCDeviceConstantsCommandAddress	= 0x40000008,
	/*
	 *	Memory-mapped I/0 (MMIO) MISO and MOSI buffer addresses
	 */
	kSignaloidSoCDeviceConstantsMISOBufferAddress	= 0x40010000,
	kSignaloidSoCDeviceConstantsMOSIBufferAddress	= 0x40020000,
};

/*
 *	Host-Device communication is achieved using the command and status registers.
 *	Following are a series of common status values. Using these is not mandatory,
 *	you can determine your own status values as you see fit.
 */
typedef enum
{
	kSignaloidSoCStatusWaitingForCommand	= 0, /* Waiting for command from host */
	kSignaloidSoCStatusCalculating		= 1, /* Executing command */
	kSignaloidSoCStatusDone		= 2, /* Execution complete */
	kSignaloidSoCStatusInvalidCommand	= 3, /* Invalid command */
} SignaloidSoCStatus;

/*
 *	Configuration status registers
 */
typedef enum
{
	C0microSDConfigurationStatusRegisterIndexID		= 0,
	C0microSDConfigurationStatusRegisterIndexVersion	= 1,
	C0microSDConfigurationStatusRegisterIndexState		= 2,
} C0microSDConfigurationStatusRegisterIndex;


/*
 *	Configuration status struct
 */
typedef struct C0microSDConfigurationStatus
{
	C0microSDConfiguration	configuration;		/* Configuration id */
	uint16_t		versionMajor;		/* Configuration version (Major) */
	uint16_t		versionMinor;		/* Configuration version (Minor) */
	uint32_t		configurationState;	/* Configuration state */
	bool			configurationSwitching;	/* Configuration state */
} C0microSDConfigurationStatus;
