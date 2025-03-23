class Bit:
    def __init__(self, value: bool):
        self.__value: bool = value

    @property
    def value(self):
        return self.__value

    def __and__(self, other):
        return Bit(self.value and other.value)

    def __or__(self, other):
        return Bit(self.value or other.value)

    def __xor__(self, other):
        return Bit(self.value != other.value)

    def __invert__(self):
        return Bit(not self.value)

    def __bool__(self):
        return self.value

    def __repr__(self):
        return f"Bit({int(self.__value)})"

    def __len__(self):
        return 1


class BitVector:
    def __init__(self, value: int, width: int):
        # the bit vec in unsigned integer format
        if value > 0:
            assert 0 <= value < 2**width , f"Value {value} is out of range for width {width}"
            self.__value = value
        else:
            assert -2**(width-1) <= value, f"Value {value} is out of range for width {width}"
            self.__value = value & ((1 << width) - 1)
            assert self.__value > 0, f"Value {value} is out of range for width {width}"
        self.__width = width

    def __len__(self):
        return self.__width

    @property
    def value(self):
        return self.__value

    def __and__(self, other):
        max_width = max(len(self), len(other))
        return BitVector(self.value & other.value , max_width)

    def __or__(self, other):
        max_width = max(len(self), len(other))
        return BitVector(self.value | other.value , max_width)

    def __xor__(self, other):
        max_width = max(len(self), len(other))
        return BitVector(self.value ^ other.value , max_width)

    def __invert__(self):
        inv_value = ((1 << self.__width) - 1) ^ self.value
        return BitVector(inv_value, self.__width)

    def __bool__(self):
        return self.value != 0

    def __bin_str(self):
        return bin(self.value)[2:].zfill(self.__width)

    def __hex_str(self):
        return hex(self.value)[2:].zfill((self.__width + 3) // 4)

    def as_uint_value(self):
        return self.value

    def as_sint_value(self):
        if self.value >= 2**(self.__width - 1):
            return self.value - 2**self.__width
        else:
            return self.value

    def __repr__(self):
        return ("BitVector, "
                f"bin: {self.__bin_str()}, "
                f"hex: {self.__hex_str()}, "
                f"uint: {self.as_uint_value()}, "
                f"sint: {self.as_sint_value()}")





# Example usage:
if __name__ == "__main__":
    a = Bit(True)
    b = Bit(False)
    print(a & b)  # Bit(False)
    print(a | b)  # Bit(True)
    print(a ^ b)  # Bit(True)
    print(~a)     # Bit(False)

    # BitVector example
    v_a = BitVector(0b1010, 4)
    v_b = BitVector(0b1100, 4)
    print(v_a & v_b)  # BitVector: bin: 1000, hex: 8, uint: 8, sint: 8
    print(v_a | v_b)  # BitVector: bin: 1110, hex: e, uint: 14, sint: 14
    print(v_a ^ v_b)  # BitVector: bin: 110, hex: 6, uint: 6, sint: 6
    print(~v_a)       # BitVector: bin: 1101, hex: d, uint: 13, sint: -3

    # singed example
    v_a = BitVector(-3, 4)
    v_b = BitVector(-5, 3) # error
    print(v_a)
    print(v_b)

    # # BitVector example more than 64 bits
    # v_a = BitVector(0b1010, 65)
    # v_b = BitVector(0b1100, 67)
    # print(v_a & v_b)  # BitVector: bin: 1000, hex: 8, uint: 8, sint: 8
    # print(v_a | v_b)  # BitVector: bin: 1110, hex: e, uint: 14, sint: 14
    # print(v_a ^ v_b)  # BitVector: bin: 1110, hex: e, uint: 14, sint: 14
    # print(~v_a)       # BitVector: bin: 11110101, hex: f5, uint: 245, sint: -11
