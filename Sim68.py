from bitstring import *
from MemoryController import *

class Sim68:
    def __init__(self, mem_controler):
        self.D = [bitstring(0,16) for i in range(0,4)]
        self.A = [bitstring(0,24) for i in range(0,4)]
        self.PC = bitstring(0,24)
        self.SR = bitstring(0,5)

        self.IR = bitstring(0,16)
        self.MBR = bitstring(0,32)
        self.MAR = bitstring(0,24)
        
        self.mem = mem_controler


    def _fetch(self):
        self.MAR = self.PC[:]
        self.MBR[7:0]  = bitstring(mem.read(self.MAR), 8)
        self.MBR[16:8] = bitstring(mem.read(self.MAR+1), 8)
        self.IR = self.MBR[:]

    def _decode(self):
        pass

    def _execute(self):
        if self.IR[]



mem = MemoryController(2**24)
proc = Sim68(mem)
