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
	kMaxBrightnessLevel	= 255
};

/**
 *	@brief 	Turn on the on-board status LED of the Signaloid SoC using PWM
 * 
 *	@param brightness:	uint8_t brightness value (0 - 255)
 *	@param iterate:		Iterate same PWM package multiple times.
 */
void static ledPWM(uint8_t brightness, uint32_t iterate)
{
	volatile uint32_t *	mmioSoCControl = (uint32_t *) kSignaloidSoCDeviceConstantsSoCControlAddress;
	for (uint32_t i = 0; i < iterate; i++)
	{
		for (int j = 0; j < kMaxBrightnessLevel; j++)
		{
			if (j < brightness)
			{
				*mmioSoCControl = 0x00000001;
			}
			else
			{
				*mmioSoCControl = 0x00000000;
			}
		}
	}
}

int
main(void)
{
	uint8_t brightness;
	while (1)
	{		
		/*
		 *	Fade in LED
		 */
		for (brightness = 0; brightness < kMaxBrightnessLevel; brightness++)
		{
			ledPWM(brightness, 4);
		}

		/*
		 *	Fade out LED
		 */
		for (brightness = kMaxBrightnessLevel; brightness > 0; brightness--)
		{
			ledPWM(brightness, 4);
		}
	}
}
