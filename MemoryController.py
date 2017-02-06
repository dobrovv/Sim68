from array import array
from bitstring import *

class MemoryBusError(Exception):
    pass



class MemoryController:
    def __init__(self):
        self.devices = []


    def map_device(self, device, addrs_range):
        device._map(self, addrs_range)
        self.devices.append(device)


    def read(self, addrs):
        for device in self.devices:
            if addrs in device.addrs_range:
                return device.read(addrs) 

        raise MemoryBusError("The address '{0}' isn't mapped to any I/O device".format(hex(addrs))) 


    def write(self, addrs, data):
        for device in self.devices:
            if addrs in device.addrs_range:
                return device.write(addrs, data)
    
        raise MemoryBusError("The address '{0}' isn't mapped to any I/O device".format(hex(addrs))) 


    def read_word(self, addrs):
        if type(addrs) is bitstring:
            addrs = addrs._val
        word = bitstring(0, 16)
        word[15:8] = self.read(addrs) 
        word[7:0]  = self.read(addrs+1)
        return word._val


    def write_word(self, addrs, data):
        if type(addrs) is bitstring:
            addrs = addrs._val

        if type(data) is bitstring:
            word = data
        else:
            word = bitstring(0, 16)
            word[15:0] = data

        self.write(addrs, word[15:8])
        self.write(addrs+1, word[7:0])



class IODevice:
    def __init__(self):
        self.addrs_range = range(0,0)
        self.mem_ctrl = None


    def _map(self, mem_ctrl, addrs_range):
        self.addrs_range = addrs_range
        self.mem_ctrl = mem_ctrl
        

    def read(self, addrs):
        print("IODevice::Generic read at '{0}'".format(hex(addrs)))


    def write(self, addrs, data):
        print("IODevice::Generic write '{0}' at '{1}'".format(hex(data), hex(addrs)))



class Memory(IODevice):
    def __init__(self, capacity):
        self.M = array('B', [0]*capacity)

    
    def read(self, addrs):
        offset = addrs - self.addrs_range[0]
        return self.M[offset]


    def write(self, addrs, data):
        offset = addrs - self.addrs_range[0]
        self.M[offset] = data



if __name__ == '__main__':
    mem_ctrl = MemoryController()
    mem_ctrl.map_device(Memory(2**16), range(0, 2**16))

    mem_ctrl.write_word(0xAA, 256)
    print ( mem_ctrl.read(0xAA))
