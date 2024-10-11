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

/**
 *	@brief	Read data from the Signaloid C0-microSD device. This is the entry
 *		function for all read transactions.
 *
 *	@param	device		device path of C0-microSD.
 *	@param	destBuffer	destination buffer for data to be stored.
 *	@param	bufferSize	number of bytes to be read.
 *	@param	offset		offset address.
 *
 *	@return			number of bytes read, -1 if error occurred.
 */
ssize_t hostUtilsReadFromC0microSD(char *  device, void *  destBuffer, size_t bufferSize, off_t offset);

/**
 *	@brief	Write data tp the Signaloid C0-microSD device. This is the entry
 *		function for all write transactions.
 *
 *	@param	device		device path of C0-microSD.
 *	@param	destBuffer	source buffer of data.
 *	@param	bufferSize	number of bytes to be written.
 *	@param	offset		offset address.
 *
 *	@return			number of bytes written, -1 if error occurred.
 */
ssize_t hostUtilsWriteToC0microSD(char *  device, void *  sourceBuffer, size_t bufferSize, off_t offset);

/**
 *	@brief	Read status of active configuration. Configuration status includes
 *		Configuration ID, Configuration Version, and Configuration State.
 *
 *	@param	device				device path of C0-microSD
 *	@return	C0microSDConfigurationStatus	configuration status struct
 */
C0microSDConfigurationStatus hostUtilsReadC0microSDConfigurationStatus(char *  device);

/**
 *	@brief	Print active configuration status on stdout.
 *
 *	@param	status		configuration status struct
 */
void hostUtilsPrintC0microSDConfigurationStatus(C0microSDConfigurationStatus status);

/**
 *	@brief	Assert that the target device is a C0-microSD, and that the active
 *		configuration is the Signaloid SoC in IDLE state. If any of the
 *		above fails, the function exits the process with EXIT_FAILURE code.
 *
 *	@param	status		C0microSDConfigurationStatus containing decoded configuration status
 *				of C0-microSD
 */
void hostUtilsAssertSignaloidSoCStatus(C0microSDConfigurationStatus status);

/**
 *	@brief	Write data to Signaloid C0-microSD MOSI buffer
 *
 *	@param	device		device path of C0-microSD
 *	@param	srcBuffer	source buffer, this must be at least kSignaloidSoCCommonConstantsMOSIBufferSizeBytes bytes long
 */
void hostUtilsWriteSignaloidSoCMOSIBuffer(char *  device, void *  srcBuffer);

/**
 *	@brief	Read data from Signaloid C0-microSD MISO buffer
 *
 *	@param	device		device path of C0-microSD
 *	@param	destBuffer	destination buffer, this must be at least kSignaloidSoCCommonConstantsMISOBufferSizeBytes bytes long
 */
void hostUtilsReadSignaloidSoCMISOBuffer(char *  device, void *  destBuffer);

/**
 *	@brief	Read status register of Signaloid C0-microSD
 *
 *	@param	device			device path of C0-microSD
 *	@return	SignaloidSoCStatus	Status code of Signaloid SoC
 */
SignaloidSoCStatus hostUtilsReadSignaloidSoCStatusRegister(char *  device);


/**
 *	@brief	Read SoCControl register of Signaloid C0-microSD
 *
 *	@param	device		device path of C0-microSD
 *	@return	uint32_t	Signaloid C0-microSD SoCControl register value
 */
uint32_t hostUtilsReadSignaloidSoCSoCControlRegister(char *  device);

/**
 *	@brief	Send command to Signaloid C0-microSD
 *
 *	@param	device		device path of C0-microSD
 *	@param	command		command code
 */
void hostUtilsSendSignaloidSoCCommand(char *  device, uint32_t command);
