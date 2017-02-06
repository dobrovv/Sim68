class bitstring:
    def __init__(self, val = 0, width = 32):
        self.width = width
        self._val  = val % 2**width

    def __int__(self):
        return self._val

    def __repr__(self):
        return "{0}:{1}".format(bin(self._val), self.width)

    def __getitem__(self, slicing):
        if type(slicing) is int:
            high_i = low_i = slicing;
        else:
            high_i = slicing.start if slicing.start != None else self.width-1 ;
            low_i  = slicing.stop if slicing.stop != None else 0
        return bitstring( self._val >> low_i, high_i-low_i+1 ) 


    def __setitem__(self, slicing, item):
        if type(slicing) is int:
            high_i = low_i = slicing;
        else:
            high_i = slicing.start if slicing.start != None else self.width-1
            low_i  = slicing.stop if slicing.stop != None else 0
        
        if type(item) is  int:
            bit_length = item.bit_length()
        else:
            bit_length = item.width

        if high_i-low_i + 1 < bit_length:
            raise AttributeError("Can't assign bitstrings wider than the slice itself")
        elif high_i >= self.width or low_i < 0:
            raise AttributeError("Slice is out of the  bound")

        clear_mask = ~( (2**(high_i - low_i + 1)-1) << low_i )
        self._val &= clear_mask
        if type(item) is int:
           val = item % 2**(high_i-low_i+1) 
        else:
            val = item._val
        self._val |= val << low_i
        return self

    def msb(self):
        return self[self.width-1] 
    
    def extend(self, width, signed=False):
        new_width = max(width, self.width)
        if signed == False or self.msb() == bitstring(0,1):
            return bitstring(self._val, new_width)
        else:
            ones_mask = (2**(new_width-self.width)-1) << self.width
            new_value = ones_mask | self._val
            return bitstring(new_value, new_width)

    def __eq__(self, other):
        if type(other) is int:
            return self.width >= other.bit_length() and self._val == other
        return self.width == other.width and self._val == other._val

    def __add__(self, other):
        if type(other) is int:
            return bitstring(self._val + other, self.width)
        width   = max(self.width, other.width);
        val     = self._val + other._val;
        return bitstring(val, width);
    
    def __sub__(self, other):
        if type(other) is int:
            return bitstring(self._val - other, self.width)
        width   = max(self.width, other.width);
        val     = self._val + ~(other._val)+1;
        return bitstring(val, width);

    def __radd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other):
        width   = max(self.width, other.width);
        val     = self._val * other._val;
        return bitstring(val, width);

    def __div__(self, other):
        width   = max(self.width, other.width);
        val     = self._val / other._val;
        return bitstring(val, width);

if __name__ =='__main__':
    a = bitstring(16, 8)
    print(a[4:0] == 16)

