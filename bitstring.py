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
        if high_i-low_i + 1 < item.width or high_i >= self.width:
            raise AttributeError("Can't assign bitstrings wider than the slice itself")
        clear_mask = ~( (2**(high_i - low_i + 1)-1) << low_i )
        self._val &= clear_mask
        self._val |= item._val << low_i
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
    a = bitstring(0xAA, 8)
    print(a, (1+a) )
