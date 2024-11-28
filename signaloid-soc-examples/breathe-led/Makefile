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

#
#	You will want to change the following to suit your setup:
#
TOOLCHAIN		= /opt/riscv32i

TARGET			= riscv
TARGET-ARCH		= riscv32-unknown-elf
TARGET-ARCH-FLAGS	= -DM32

COMMON			= ../common
TOOLKIT_INCLUDE		= ../../submodules/C0-microSD-utilities/src/c/include
TOOLKIT			= python3 ../../submodules/C0-microSD-utilities/C0_microSD_toolkit.py
DEVICE			= /dev/disk4

TOOLCC			= gcc
TOOLCXX			= g++

#
#	You likely do not need to change the items below:
#

TOOLSBIN	= $(TOOLCHAIN)/bin
TOOLSLIB	= $(TOOLCHAIN)/$(TARGET-ARCH)/lib
TOOLSLIBGCC	= $(lastword $(sort $(wildcard $(TOOLCHAIN)/lib/gcc/riscv32-unknown-elf/*/)))
 
CC		= $(TOOLSBIN)/$(TARGET-ARCH)-gcc
CXX		= $(TOOLSBIN)/$(TARGET-ARCH)-g++
LD		= $(TOOLSBIN)/$(TARGET-ARCH)-ld
AR		= $(TOOLSBIN)/$(TARGET-ARCH)-ar
OBJCOPY		= $(TOOLSBIN)/$(TARGET-ARCH)-objcopy
OBJDUMP		= $(TOOLSBIN)/$(TARGET-ARCH)-objdump
AS		= $(TOOLSBIN)/$(TARGET-ARCH)-as
SIZE		= $(TOOLSBIN)/$(TARGET-ARCH)-size
STRIP		= $(TOOLSBIN)/$(TARGET-ARCH)-strip
RANLIB		= $(TOOLSBIN)/$(TARGET-ARCH)-ranlib
MAKE		= make
RM		= rm -rf
DEL		= rm -rf


PROGRAM		= main

INIT_S		= $(COMMON)/init.S
INIT		= init

TOOL_INCL_DIR	= $(TOOLCHAIN)/include
OPTFLAGS	= -Os -g
CFLAGS		= -march=rv32i -mabi=ilp32 $(TARGET-ARCH-FLAGS) -Wall
ASFLAGS		= --march=rv32i --mabi=ilp32
INCLUDES	= -I$(TOOL_INCL_DIR) -I$(TOOLKIT_INCLUDE)
LD_SCRIPT	= $(COMMON)/C0-microSD.ld
LDFLAGS		= -T$(LD_SCRIPT) -L$(TOOLSLIB) -L$(TOOLSLIBGCC) -Map $(PROGRAM).map

OBJS		= $(INIT).o $(PROGRAM).o

all:	$(PROGRAM) $(PROGRAM).bin

$(INIT).o: $(INIT_S)
	$(AS) $(ASFLAGS) $(INIT_S) -o $(INIT).o

$(PROGRAM).o: $(PROGRAM).c
	$(CC) $(CFLAGS) $(OPTFLAGS) $(INCLUDES) -c $(PROGRAM).c

$(PROGRAM): $(OBJS)
	$(LD) $(LDFLAGS) $(OBJS) -o $@ -lm -lc -lnosys -lgcc

$(PROGRAM).bin: $(OBJS)
	$(OBJCOPY) -O binary $(PROGRAM) $@

disassemble:
	$(OBJDUMP) -dSl $(PROGRAM) > $(PROGRAM).dis.S

flash: $(PROGRAM).bin
	sudo $(TOOLKIT) -t $(DEVICE) -b $(PROGRAM).bin -u -p 128K

switch:
	sudo $(TOOLKIT) -t $(DEVICE) -s

clean:
	$(RM) init.i *.o $(PROGRAM) $(PROGRAM).sr $(PROGRAM).map $(PROGRAM).dis.S $(PROGRAM).bin
