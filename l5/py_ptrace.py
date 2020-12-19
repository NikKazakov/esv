import ctypes
# look file /usr/ include / x86_64 -linux -gnu /sys/ user .h
# struct pt_regs
class user_regs_struct(ctypes.Structure):
    _fields_ = map(lambda x : (x, ctypes.c_ulong),
				['r15', 'r14', 'r13', 'r12', 'rbp',
				 'rbx', 'r11', 'r10', 'r9', 'r8',
				 'rax', 'rcx', 'rdx', 'rsi', 'rdi',
				 'orig_rax', 'rip', 'cs', 'eflags',
				 'rsp', 'ss', 'fs_base', 'gs_base',
				 'ds', 'es', 'fs', 'gs'])

# look file /usr/ include /x86_64 -linux -gnu /sys/ ptrace .h
# enum __ptrace_request
PTRACE_PEEKDATA = 2
PTRACE_POKEDATA = 5
PTRACE_CONT = 7
PTRACE_SINGLESTEP = 9
PTRACE_GETREGS = 12
PTRACE_SETREGS = 13
PTRACE_ATTACH = 16
PTRACE_DETACH = 17
libc = ctypes.CDLL ('/lib/x86_64-linux-gnu/libc.so.6')
libc.ptrace.argtypes = [ctypes.c_uint,
						ctypes.c_uint,
						ctypes.c_void_p,
						ctypes.c_void_p]
libc.ptrace.restype = ctypes.c_long

import sys
import os
import signal
import copy

def alloc_pages(pid, npages=1, data=None):
	libc.ptrace(PTRACE_ATTACH, pid, None, None)
	status = os.waitpid(pid, 0)
	if os.WIFSTOPPED(status[1]) and os.WSTOPSIG(status[1]) == signal.SIGSTOP:
		print 'attached '
	else:
		print 'not attached'
		sys.exit(1)

	# save registers
	old_regs = user_regs_struct()
	libc.ptrace(PTRACE_GETREGS, pid, None, ctypes.byref(old_regs))
	new_regs = copy.copy(old_regs)

	# save next instruction ( extract 8 bytes from rip)
	code = libc.ptrace(PTRACE_PEEKDATA, pid, ctypes.c_void_p(old_regs.rip),	None)

	# set new values of registers
	new_regs.rdi = 0x0
	new_regs.rsi = npages * 4096
	new_regs.rdx = 0x7
	new_regs.r10 = 0x22
	new_regs.r8 = 0x0
	new_regs.r9 = 0x0
	new_regs.rax = 0x9
	libc.ptrace(PTRACE_SETREGS, pid, None, ctypes.byref(new_regs))

	# exec syscall
	libc.ptrace(PTRACE_POKEDATA, pid, ctypes.c_void_p(new_regs.rip), 0x050f)
	libc.ptrace(PTRACE_SINGLESTEP, pid, None, None)

	# wait while instruction is executed
	status = os.waitpid(pid, 0)
	if os.WIFSTOPPED (status[1]) and os.WSTOPSIG(status[1]) == signal.SIGTRAP:
		print 'successful trap'
	else:
		print 'unsuccessful trap'
		sys.exit(1)

	# get return value of mmap (from rax)
	libc.ptrace(PTRACE_GETREGS, pid, None, ctypes.byref(new_regs))
	addr = new_regs.rax

	if data is not None and data != '':
	# write in 8 - byte chunks in reverse order
		l = ['{:02x}'.format(ord(d)) for d in data] + ['00']
	for i in range((len(l) - 1) / 8 + 1):
		a = reversed(l[i * 8:(i + 1) * 8])
		libc.ptrace(PTRACE_POKEDATA, pid, ctypes.c_void_p(addr+i*8), int(''.join(a),16))

	# restore registers and next instruction
	libc.ptrace(PTRACE_POKEDATA, pid, ctypes.c_void_p(old_regs.rip), code)
	libc.ptrace(PTRACE_SETREGS, pid, None, ctypes.byref(old_regs))
	libc.ptrace(PTRACE_CONT, pid, None, None)
	libc.ptrace(PTRACE_DETACH, pid, None, None)
	return addr

def call_execve(pid, addr):
	libc.ptrace(PTRACE_ATTACH, pid, None, None)
	status = os.waitpid(pid, 0)
	if os.WIFSTOPPED(status[1]) and os.WSTOPSIG(status[1]) == signal.SIGSTOP:
		print 'attached'
	else :
		print 'not attached'
		sys.exit(1)

	# get registers
	regs = user_regs_struct()
	libc.ptrace(PTRACE_GETREGS, pid, None, ctypes.byref(regs))

	# set new values of registers
	regs.rdx = 0
	regs.rsi = 0
	regs.rdi = addr
	regs.rax = 0x3b
	libc.ptrace(PTRACE_SETREGS, pid, None, ctypes.byref(regs))

	libc.ptrace(PTRACE_POKEDATA, pid, ctypes.c_void_p(regs.rip), 0x050f)
	libc.ptrace(PTRACE_SINGLESTEP, pid, None, None)

	# wait while instruction is executed
	status = os.waitpid(pid, 0)
	if os.WIFSTOPPED(status[1]) and os.WSTOPSIG(status[1]) == signal.SIGTRAP:
		print 'successful trap'
	else :
		print 'unsuccessful trap'

	libc.ptrace(PTRACE_CONT, pid, None, None)
