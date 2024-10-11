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

#include <stdint.h>
#include <stdbool.h>
#include "C0microSDConstants.h"

enum
{
	kCalculateNoCommand			= 0,
	kCalculateAddition			= 1,
	kCalculateSubtraction			= 2,
	kCalculateMultiplication		= 3,
	kCalculateDivision			= 4,
};

int
main(void)
{
	volatile SignaloidSoCStatus *	mmioStatus = (SignaloidSoCStatus *) kSignaloidSoCDeviceConstantsStatusAddress;
	volatile uint32_t *		mmioCommand = (uint32_t *) kSignaloidSoCDeviceConstantsCommandAddress;
	volatile float *		mmioWriteBuf = (float *) kSignaloidSoCDeviceConstantsMISOBufferAddress;
	volatile float *		mmioReadBuf = (float *) kSignaloidSoCDeviceConstantsMOSIBufferAddress;
	float				sourceValueA = 0.0f;
	float				sourceValueB = 0.0f;
	float				calculatedValue = 0.0f;

	while (1)
	{
		/*
		 *	Set status to
		 */
		*mmioStatus = kSignaloidSoCStatusWaitingForCommand;
		/*
		 *	Block until command is issued
		 */
		while (*mmioCommand == kCalculateNoCommand) {}
		/*
		 *	Set status to inform host that calculation will start
		 */
		*mmioStatus = kSignaloidSoCStatusCalculating;

		switch (*mmioCommand)
		{
			case kCalculateAddition:
				/* 
				 *	Get source data from source buffer
				 */
				sourceValueA = mmioReadBuf[0];
				sourceValueB = mmioReadBuf[1];
				/* 
				 *	Calculate addition of source values
				 */
				calculatedValue = sourceValueA + sourceValueB;
				mmioWriteBuf[0] = calculatedValue;
				/* 
				 *	Inform host about successful calculation
				 */
				*mmioStatus = kSignaloidSoCStatusDone;
				break;
			case kCalculateSubtraction:
				/* 
				 *	Get source data from source buffer
				 */
				sourceValueA = mmioReadBuf[0];
				sourceValueB = mmioReadBuf[1];
				/* 
				 *	Calculate subtraction of source values
				 */
				calculatedValue = sourceValueA - sourceValueB;
				mmioWriteBuf[0] = calculatedValue;
				/* 
				 *	Inform host about successful calculation
				 */
				*mmioStatus = kSignaloidSoCStatusDone;
				break;
			case kCalculateMultiplication:
				/* 
				 *	Get source data from source buffer
				 */
				sourceValueA = mmioReadBuf[0];
				sourceValueB = mmioReadBuf[1];
				/* 
				 *	Calculate multiplication of source values
				 */
				calculatedValue = sourceValueA * sourceValueB;
				mmioWriteBuf[0] = calculatedValue;
				/* 
				 *	Inform host about successful calculation
				 */
				*mmioStatus = kSignaloidSoCStatusDone;
				break;
			case kCalculateDivision:
				sourceValueA = mmioReadBuf[0];
				sourceValueB = mmioReadBuf[1];
				
				/* 
				 *	Calculate division of source values
				 */
				calculatedValue = sourceValueA / sourceValueB;
				mmioWriteBuf[0] = calculatedValue;
				/* 
				 *	Inform host about successful calculation
				 */
				*mmioStatus = kSignaloidSoCStatusDone;
				break;
			default:
				*mmioStatus = kSignaloidSoCStatusInvalidCommand;
				break;
		}

		/*
		 *	Block until command is cleared
		 */
		while (*mmioCommand != kCalculateNoCommand)
		{
			;
		}
	}
}
