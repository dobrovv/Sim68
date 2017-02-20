from bitstring import *
from MemoryController import *
from ALU import *

class Sim68:
    def __init__(self, mem_controller):
        self.D = [bitstring(0,32) for i in range(0,4)]
        self.A = [bitstring(0,32) for i in range(0,4)]
        
        self.PC = bitstring(0,32)
        self.SR = bitstring(0,16)

        self.IR = bitstring(0,16)
        self.MBR = bitstring(0,16)
        self.MAR = bitstring(0,32)
        
        self.mem_ctrl = mem_controller
        self.alu = ALU()

    def set_statusbits(
        self, carry=None, overflow=None, zero=None, negative=None, extend=None
    ):
        self.SR[0] = carry     if carry    is not None else self.SR[0]
        self.SR[1] = overflow if overflow is not None else self.SR[1]
        self.SR[2] = zero      if zero     is not None else self.SR[2]
        self.SR[3] = negative  if negative is not None else self.SR[3]
        self.SR[4] = extend    if extend   is not None else self.SR[4]
 

    def _get_alu_result(self):
        self.set_statusbits(
            carry=self.alu.carry, overflow=self.alu.overflow, 
            zero=self.alu.zero, negative=self.alu.negative
        )

        return self.alu.result

        
    def _fetch(self):
        self.MAR[:] = self.PC
        self.MBR[:] = mem_ctrl.read_word(self.MAR)
        self.IR[:]  = self.MBR

    def _decode(self):
        pass

    def _execute(self):
        
        op_code = self.IR[15:12]
        op_mode = self.IR[8:3]
        src_n = self.IR[2:0].val()
        dst_n = self.IR[11:9].val()


        if op_code  == 0b1101:              # Add Instruction
            if op_mode == 0b001000:         # Add dDn, sDn
                self.alu.add(self.D[src_n][15:0], self.D[dst_n][15:0])
                self.D[dst_n][15:0] = self._get_alu_result()

mem_ctrl = MemoryController()
proc = Sim68(mem_ctrl)


mem_ctrl.map_device(Memory(2**16), range(0, 2**16))
mem_ctrl.write_word(0, 0b1101000001000001)

proc.D[0][:] = 3
proc.D[1][:] = 10

print(proc.D[0])

proc._fetch()
proc._decode()
proc._execute()

print(proc.D[0])
