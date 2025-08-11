#
#	Icestorm toolchain
#
PACKED_BITSTREAM	= pack.bin
ICEMULTI		= icemulti
ICEMULTI_ARGS		= -p0 -A 19 -v -o $(PACKED_BITSTREAM)
ICEPROG			= iceprog
ICEPROG_ARGS		= -I B -p

#
#	Bootloader toolchain
#
DFU_UTIL		= python3 ../submodules/C0-microSD-utilities/C0_microSD_toolkit.py
DFU_DEVICE		= /dev/disk4

#
#	Configuration bitstreams
#
BOOTLOADER 		= bootloader.bin
SIGNALOID_SOC		= signaloid-soc.bin
CUSTOM_USER_BITSTREAM	= blink.bin

#
#	We are packing Bootloader - Signaloid SoC - Empty Design - User Design. This is so that the 
#	User Design is outside the Software Security Region of the SPI Flash
#
$(PACKED_BITSTREAM): $(BOOTLOADER) $(SIGNALOID_SOC) $(CUSTOM_USER_BITSTREAM)
	dd if=/dev/zero bs=1 count=32768 | tr '\000' '\377' > empty.bin
	$(ICEMULTI) $(ICEMULTI_ARGS) $(BOOTLOADER) $(SIGNALOID_SOC) empty.bin $(CUSTOM_USER_BITSTREAM)
	rm empty.bin

flash: $(PACKED_BITSTREAM)
	$(ICEPROG) $(ICEPROG_ARGS) $(PACKED_BITSTREAM)

flash-dfu-bootloader:
	sudo $(DFU_UTIL) -t $(DFU_DEVICE) -b $(BOOTLOADER) -q

flash-dfu-soc:
	sudo $(DFU_UTIL) -t $(DFU_DEVICE) -b $(SIGNALOID_SOC) -w

flash-dfu-blink:
	sudo $(DFU_UTIL) -t $(DFU_DEVICE) -b $(CUSTOM_USER_BITSTREAM)

switch:
	sudo $(DFU_UTIL) -t $(DFU_DEVICE) -s

clean:
	rm -f $(PACKED_BITSTREAM)
