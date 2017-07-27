#!/usr/bin/env python2

import r2pipe
import sys

if len(sys.argv) < 2:
    print("Usage: {} <path to toilet-binary>".format(sys.argv[0]))
    sys.exit(1)

r2p=r2pipe.open(sys.argv[1])
r2p.cmd('oo+')
print("Before patching:")
r2p.cmd('s 0x004024c2')
print(r2p.cmd('pd 13'))

r2p.cmd('s 0x004024e6')
r2p.cmd('wx 0fb7ed') # movzx ebp, bp (rasm2 doesn't support this instr)
r2p.cmd('s 0x004024e9') # /
r2p.cmd('wx 909090909090')

print("\n\nAfter patching:")
r2p.cmd('s 0x004024c2')
print(r2p.cmd('pd 18'))
r2p.quit()
