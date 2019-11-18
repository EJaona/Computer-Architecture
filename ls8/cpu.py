"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

SP = 7

EQUAL = 0b0
LESS = 0b0
GREATER = 0b0

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.halted = False
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0
        

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value


    def load(self, program):
        """Load a program into memory."""
        # print(f'Program start: {program}')
        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(program) as f:
            for instructions in f:
                # print(instructions)
                instructions = instructions.split("#")[0].strip()
                # print(f'second: {instructions}')

                if instructions == "":
                    continue
                value = int(instructions, 2)## Turn to base 2
                print(instructions)
                self.ram[address] = value

                address += 1
                


    


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                EQUAL = 1
                LESS = 0
                GREATER = 0
            if self.reg[reg_a] < self.reg[reg_b]:
                EQUAL = 0
                LESS = 1
                GREATER = 0
            if self.reg[reg_a] > self.reg[reg_b]:
                EQUAL = 0
                LESS = 0
                GREATER = 1



        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        


        self.trace()

        self.pc = 0
        while not self.halted:
            # print(self.ram)
            self.ir = self.ram[self.pc]
            location = self.ram[self.pc + 1]
            value = self.ram[self.pc + 2]
            # HLT Halt
            if self.ir == HLT:
                self.halted = True
                self.pc += 1
            # LDI Store value in register  reg, val
            elif self.ir == LDI:
                self.reg[location] = value
                self.pc += 3
                print(f'LDI to reg:{location}, value: {value}')
            # PRN Print
            elif self.ir == PRN:
                print(f'PRN:{self.reg[location]}')
                self.pc += 2
            # MUL multiply
            elif self.ir == PUSH:

                self.reg[SP] -= 1 # dec stack pointer
                reg_value = self.reg[location]
                self.ram[self.reg[SP]] = reg_value # Copying the register value into me at stack pointer index

                self.pc += 2

            elif self.ir == POP:

                value = self.ram[self.reg[SP]]
                reg_num = self.ram[location]
                
                self.reg[reg_num] = value
                
                self.pc += 2

            elif self.ir == CALL:

                return_address = self.pc + 2

                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = return_address

                self.pc += 2

            elif self.ir == RET:
                # pop the return address off the stack
                # store it in the pc
                self.pc = self.ram[SP]
                self.reg[SP] += 1

            elif self.ir == CMP:
                
                self.alu('CMP', location, value)

                self.pc += 3

            elif self.ir == JMP:
                
                self.pc = self.reg[self.ram[self.pc + 1]]

            elif self.ir == JEQ:
                
                if EQUAL == 1:
                    self.pc = self.reg[location]
                else:
                    self.pc += 2

            elif self.ir == JNE:
                
                if EQUAL == 0:
                    self.pc = self.reg[location]
                else:
                    self.pc += 2

            elif self.ir == MUL:
                self.alu("MUL", location, value)
                self.pc += 3
            else:
                self.pc += 1
