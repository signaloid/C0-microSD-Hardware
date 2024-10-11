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
#include <unistd.h>
#include <stdint.h>
#include <math.h>
#include <stdbool.h>
#include <errno.h>

#include "C0microSDConstants.h"
#include "C0microSDHostUtils.h"

enum
{
	kCalculateNoCommand		= 0,
	kCalculateAddition		= 1,
	kCalculateSubtraction		= 2,
	kCalculateMultiplication	= 3,
	kCalculateDivision		= 4,
};

enum
{
	kReturnSuccess			= 0,
	kReturnError			= 1,	
};

/**
 *	@brief Sends a command to the Signaloid SoC and parses the output buffer.
 *
 *	@param device: Path to C0-microSD.
 *	@param command: Command to execute.
 *	@param readBuffer: Pointer to temp buffer for storing the Signaloid SoC MISO buffer data.
 *	@return The first 4 bytes of the result buffer parsed as float.
 */
float
calculateDataFP(char *  device, uint32_t command, float *  readBuffer)
{
	float			returnValue = NAN;
	SignaloidSoCStatus 	deviceStatus;

	printf("Start calculation of command: %u\n", command);
	/*
	 *	Instruct Signaloid C0-microSD compute module which command to execute
	 */
	hostUtilsSendSignaloidSoCCommand(device, command);

	printf("Waiting for calculation to finish\n");
	while (1)
	{
		/*
		 *	Get status of Signaloid C0-microSD compute module
		 */
		deviceStatus = hostUtilsReadSignaloidSoCStatusRegister(device);

		if (deviceStatus == kSignaloidSoCStatusCalculating)
		{
			/*
			 *	Signaloid C0-microSD compute module is still calculating
			 */
			printf(".\n");
			sleep(1);
		}
		else if (deviceStatus == kSignaloidSoCStatusDone)
		{
			/*
			 *	Signaloid C0-microSD completed calculation
			 *	Read the output of Signaloid C0-microSD calculation
			 */
			hostUtilsReadSignaloidSoCMISOBuffer(device, readBuffer);
			returnValue = readBuffer[0];
			break;
		}
		else if (deviceStatus == kSignaloidSoCStatusInvalidCommand)
		{	
			printf("ERROR: Device returned 'Unknown CMD'\n");
			break;
		}
		else if (deviceStatus != kSignaloidSoCStatusWaitingForCommand)
		{
			printf("ERROR: Device returned 'Unknown CMD'\n");
			break;
		}
	}

	/*
	 *	Send ack to Signaloid C0-microSD compute module
	 */
	while (hostUtilsReadSignaloidSoCStatusRegister(device) != kSignaloidSoCStatusWaitingForCommand)
	{
		hostUtilsSendSignaloidSoCCommand(device, kCalculateNoCommand);
	}

	return returnValue;
}

int
main(int argc, char *  argv[])
{
	C0microSDConfigurationStatus	configurationStatus;
	float				MISOBuffer[kSignaloidSoCCommonConstantsMISOBufferSizeWords];
	float				MOSIBuffer[kSignaloidSoCCommonConstantsMOSIBufferSizeWords];
	float				valueA;
	float				valueB;
	float				calculatedResult = 0.0f;

	if (argc != 4)
	{
		/*
		 *	Ensure exactly three arguments are provided
		 */
		printf("Usage: %s <device path> <float1> <float2>\n", argv[0]);
		return kReturnError;
	}

	char *endptr;

	/*
	 *	Attempt to convert the second argument to a float
	 */
	errno = 0;
	valueA = strtof(argv[2], &endptr);
	if ((errno != 0) || (endptr == argv[2]) || (*endptr != '\0'))
	{
		printf("Error: '%s' is not a valid floating-point number.\n", argv[2]);
		return kReturnError;
	}

	/*
	 *	Attempt to convert the third argument to a float
	 */
	errno = 0;
	valueB = strtof(argv[3], &endptr);
	if ((errno != 0) || (endptr == argv[3]) || (*endptr != '\0'))
	{
		printf("Error: '%s' is not a valid floating-point number.\n", argv[3]);
		return kReturnError;
	}

	printf("Device target: %s\n", argv[1]);
	printf("First float parameter: %f\n", valueA);
	printf("Second float parameter: %f\n", valueB);

	printf("\nReading C0-microSD status\n");
	configurationStatus = hostUtilsReadC0microSDConfigurationStatus(argv[1]);
	hostUtilsAssertSignaloidSoCStatus(configurationStatus);
	hostUtilsPrintC0microSDConfigurationStatus(configurationStatus);

	printf("\nInitializing input floating-point data buffer\n\n");
	MOSIBuffer[0] = valueA;
	MOSIBuffer[1] = valueB;
	hostUtilsWriteSignaloidSoCMOSIBuffer(argv[1], (void *) MOSIBuffer);

	/*
	 *	Calculate addition of valueA and valueB
	 */
	calculatedResult = calculateDataFP(argv[1], kCalculateAddition, MISOBuffer);
	printf("Calculated output of addition: %f\n\n", calculatedResult);

	/*
	 *	Calculate subtraction of valueA and valueB
	 */
	calculatedResult = calculateDataFP(argv[1], kCalculateSubtraction, MISOBuffer);
	printf("Calculated output of subtraction: %f\n\n", calculatedResult);

	/*
	 *	Calculate multiplication of valueA and valueB
	 */
	calculatedResult = calculateDataFP(argv[1], kCalculateMultiplication, MISOBuffer);
	printf("Calculated output of multiplication: %f\n\n", calculatedResult);

	/*
	 *	Calculate division of valueA and valueB
	 */
	calculatedResult = calculateDataFP(argv[1], kCalculateDivision, MISOBuffer);
	printf("Calculated output of division: %f\n\n", calculatedResult);

	printf("Done...\n");
	return kReturnSuccess;
}
