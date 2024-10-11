.globl _start
.align	4

.section .text.unlikely

_start:
.option push
.option norelax
	li	sp, 0x0020000	# 128K
	la	gp, __global_pointer$
.option pop
	call	main

errnoValue:	.word 0

__errno:
	la	a0, errnoValue
	ret
