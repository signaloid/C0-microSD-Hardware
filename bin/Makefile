#
#	Icestorm toolchain
#
PACKED_BITSTREAM	= pack.bin
ICEMULTI		= icemulti
ICEMULTI_ARGS		= -p0 -A 19 -v -o $(PACKED_BITSTREAM)
ICEPROG			= iceprog
ICEPROG_ARGS		= -I B

#
#	Bootloader toolchain
#
DFU_UTIL		= python3 ../submodules/C0-microSD-utilities/C0_microSD_toolkit.py
DFU_DEVICE		= /dev/disk5

#
#	Configuration bitstreams
#
BOOTLOADER 			= bootloader.bin
SIGNALOID_SOC			= signaloid-soc.bin
CUSTOM_USER_CONFIGURATION	= blink.bin

$(PACKED_BITSTREAM):
	$(ICEMULTI) $(ICEMULTI_ARGS) $(BOOTLOADER) $(SIGNALOID_SOC) $(CUSTOM_USER_CONFIGURATION)

flash: $(PACKED_BITSTREAM)
	$(ICEPROG) $(ICEPROG_ARGS) $(PACKED_BITSTREAM)

flash-dfu-bootloader:
	sudo $(DFU_UTIL) -t $(DFU_DEVICE) -b $(BOOTLOADER) -q

flash-dfu-soc:
	sudo $(DFU_UTIL) -t $(DFU_DEVICE) -b $(SIGNALOID_SOC) -w

flash-dfu-blink:
	sudo $(DFU_UTIL) -t $(DFU_DEVICE) -b $(CUSTOM_USER_CONFIGURATION)

switch:
	sudo $(DFU_UTIL) -t $(DFU_DEVICE) -s

clean:
	rm -f $(PACKED_BITSTREAM)
