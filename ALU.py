from bitstring import *

class ALU:
    def __init__(self):
        self.result = None

        self.carry = None
        self.overflow = None
        self.zero = None
        self.negative = None
    
    
    def __repr__(self):
        return "{0} (C={1} O={2}, Z={3}, N={4})".format(
            self.result, self.carry, self.overflow, self.zero, self.negative
        )

    
    def add(self, a: bitstring, b: bitstring):
        assert(a.width == b.width)
        
        extra_bit = bitstring(a.val(), a.bit_length() + 1)
        extra_bit += b

        res = extra_bit[extra_bit.bit_length()-2 : 0]

        self.carry = extra_bit.msb()
        self.overflow = res.msb() ^ a.msb() if a.msb() == b.msb() else False
        self.zero = res.val() == 0
        self.negative = res.msb()
        
        self.result = res


    def sub(self, a: bitstring, b: bitstring):
        assert(a.bit_length() == b.bit_length())
        self.add(a, b.complement())


if __name__ == '__main__':
    
    alu = ALU()

    print("===Addition Test===") 
    a = bitstring(7,4)
    b = bitstring(-7,4)
    alu.add(a,b)
    print("Test Carry:\t", a, "+", b, "\t=", alu)
    
    a = bitstring(7,4)
    b = bitstring(7,4)
    alu.add(a,b)
    print("Test Overflow:\t", a, "+", b, "\t=", alu)

    print("===Subtraction Test===") 
    a = bitstring(7,4)
    b = bitstring(7,4)
    alu.sub(a,b)
    print("Test Carry:\t", a, "-", b, "\t=", alu)
    
    a = bitstring(7,4)
    b = bitstring(-7,4)
    alu.sub(a,b)
    print("Test Overflow:\t", a, "-", b, "\t=", alu)


