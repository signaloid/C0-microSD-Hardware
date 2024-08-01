#
#	Copyright (c) 2024, Signaloid.
#
#	Permission is hereby granted, free of charge, to any person obtaining a copy
#	of this software and associated documentation files (the "Software"), to deal
#	in the Software without restriction, including without limitation the rights
#	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#	copies of the Software, and to permit persons to whom the Software is
#	furnished to do so, subject to the following conditions:
#
#	The above copyright notice and this permission notice shall be included in all
#	copies or substantial portions of the Software.
#
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#	SOFTWARE.
#

TOOLKIT				= python3 ../../submodules/C0-microSD-utilities/C0_microSD_toolkit.py
DEVICE				= /dev/disk4

DESIGN				= top
DESIGN_SOURCE_FILES		= debounce.v

PCF				= pinout.pcf

ICE40_VARIANT			= up5k
ICE40_PACKAGE			= uwg30

ICEPROG_SRAM_FLAGS		= -I B -S
ICEPROG_FLASH_FLAGS		= -I B
NEXTPNR_DEVICE_FLAGS		= --up5k
NEXTPNR_PACKAGE_FLAGS		= --package $(ICE40_PACKAGE) 
TARGET_FREQ_MHZ			= 24

default: $(DESIGN) 

$(DESIGN): $(DESIGN).v $(DESIGN_SOURCE_FILES)
	yosys -p "synth_ice40 -blif $(DESIGN).blif; write_json $(DESIGN).json; opt" $(DESIGN_SOURCE_FILES) $(DESIGN).v 
	nextpnr-ice40 --freq $(TARGET_FREQ_MHZ) $(NEXTPNR_DEVICE_FLAGS) $(NEXTPNR_PACKAGE_FLAGS) --json $(DESIGN).json --pcf $(PCF) --asc $(DESIGN).asc
	icepack $(DESIGN).asc $(DESIGN).bin
	icetime -m -d $(ICE40_VARIANT) -P $(ICE40_PACKAGE)  -p $(PCF) $(DESIGN).asc

flash:
	sudo $(TOOLKIT) -t $(DEVICE) -b $(DESIGN).bin

switch:
	sudo $(TOOLKIT) -t $(DEVICE) -s

clean:
	rm -f $(DESIGN).blif $(DESIGN).json $(DESIGN).bin $(DESIGN).asc $(DESIGN).vcd dfu
