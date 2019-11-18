#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()



if len(sys.argv) != 2:
    print(f"usage: ls8.py {sys.argv[1]}")
    sys.exit(1)
program = sys.argv[1]
address = 0


cpu.load(program)
cpu.run()