from array import array

class MemoryController:
    def __init__(self, capacity):
        self.M = array('B', (0 for x in range(0, capacity-1)) )
        self.devices = []

    def map_device(self, device, addrs_range):
        device.map(self, addrs_range)
        self.devices.append(device)


    def read(self, addrs):
        for device in self.devices:
            if addrs in device.addrs_range:
                device.read(addrs)

        return self.M[addrs]

    def write(self, addrs, data):
        self.M[addrs] = data

        for device in self.devices:
            if addrs in device.addrs_range:
                device.write(addrs, data)

class IODevice:
    REQUIRED_MEM_SIZE = 1

    def __init__(self):
        self.addrs_range = range(0,0)
        self.mem = None

    def map(self, mem, addrs_range):
        self.mem = mem
        self.addrs_range = addrs_range
        

    def read(self, addrs):
        print("IODevice::Generic read at '{0}'".format(hex(addrs)))
        pass

    def write(self, addrs, data):
        print("IODevice::Generic write '{0}' at '{1}'".format(hex(data), hex(addrs)))
        pass


if __name__ == '__main__':
    mem = MemoryController(2**24)
    mem.write(0xAABBCC, 0xFE)
    print(mem.read(0xAABBCC))

    mem.map_device(IODevice(), range(0xAABBCC, 0xAABBCE))
    mem.write(0xAABBCD, 0xAA)
    print(mem.read(0xAABBCE))




