""""
   Copyright 2025 jackkyyang

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

# -------------------------------------------------------------------------
# Description:
#   This file contains the implementation of the Bits class
#   which is a simple bit vector class that supports
#   basic arithmetic operations and slicing.
#   The class is designed to be used in the context of
#   hardware modeling where bit vectors are used to represent
#   signals and registers in a hardware design.
# -------------------------------------------------------------------------

class Bits:
    __slots__ = ["__value", "__width"]
    def __init__(self, value: int | bool, width: int):
        # the bit vec in unsigned integer format
        if value >= 0:
            assert 0 <= value < 2**width , f"Value[{value}] is out of range for width {width}"
            self.__value = value
        else:
            assert -2**(width-1) <= value, f"Value[{value}] is out of range for width {width}"
            self.__value = value & ((1 << width) - 1)
            assert self.__value > 0, f"Value[{value}] is out of range for width {width}"
        self.__width = width

    def __len__(self):
        return self.__width

    @property
    def value(self):
        return self.__value

    def __and__(self, other):
        max_width = max(len(self), len(other))
        return Bits(self.value & other.value , max_width)

    def __or__(self, other):
        max_width = max(len(self), len(other))
        return Bits(self.value | other.value , max_width)

    def __xor__(self, other):
        max_width = max(len(self), len(other))
        return Bits(self.value ^ other.value , max_width)

    def __invert__(self):
        inv_value = ((1 << self.__width) - 1) ^ self.value
        return Bits(inv_value, self.__width)

    def __bool__(self):
        return self.value != 0

    def __rshift__(self, other):
        assert other >= 0, "Shift amount must be non-negative"
        assert isinstance(other, int), "Shift amount must be an integer"
        return Bits(self.value >> other, self.__width)

    def __lshift__(self, other):
        assert other >= 0, "Shift amount must be non-negative"
        assert isinstance(other, int), "Shift amount must be an integer"
        return Bits(self.value << other, self.__width)

    def __add__(self, other):
        max_width = max(len(self), len(other))
        return Bits(self.value + other.value, max_width+1)

    def __sub__(self, other):
        max_width = max(len(self), len(other))
        return Bits(self.value - other.value, max_width+1)

    def __mul__(self, other):
        result_width = len(self) + len(other)
        return Bits(self.value * other.value, result_width)

    def __truediv__(self, other):
        return Bits(self.value // other.value, self.__width)

    def __floordiv__(self, other):
        return Bits(self.value // other.value, self.__width)

    def __mod__(self, other):
        return Bits(self.value % other.value, other.__width)

    def __eq__(self, other) -> "Bits": # type: ignore
        return Bits(self.value == other.value, 1)

    def __ne__(self, other) -> "Bits": # type: ignore
        return Bits(self.value != other.value, 1)

    def __lt__(self, other):
        return Bits(self.value < other.value, 1)

    def __le__(self, other):
        return Bits(self.value <= other.value, 1)

    def __gt__(self, other):
        return Bits(self.value > other.value, 1)

    def __ge__(self, other):
        return Bits(self.value >= other.value, 1)

    def __getitem__(self, key):
        if isinstance(key, int):
            if key >= self.__width:
                raise ValueError(f"Index: [{key}] out of range of width: {self.__width}")
            return Bits((self.value >> key) & 1, 1)
        elif isinstance(key, slice):
            if key.step is not None:
                raise ValueError("Slice step is not supported")
            start = key.start if key.start is not None else self.__width-1
            stop = key.stop if key.stop is not None else 0
            if start == stop and start is not None:
                if start >= self.__width:
                    raise ValueError(f"Index: [{start}:{stop}] out of range of width: {self.__width}")
                return Bits((self.value >> start) & 1, 1)
            if start < stop:
                lsb, msb = start, stop
            else:
                lsb, msb = stop, start
            if msb >= self.__width:
                raise ValueError(f"Index: [{msb}] out of range of width: {self.__width}")
            if lsb < 0:
                raise ValueError(f"Index: [{lsb}] out of range")

            result_width = msb - lsb + 1
            result_value = (self.value >> lsb) & ((1 << result_width) - 1)
            if start > stop:
                return Bits(result_value, result_width)
            else:
                bin_str = bin(result_value)[2:].zfill(result_width)
                reversed_str = bin_str[::-1]
                reversed_value = int(reversed_str, 2)
                return Bits(reversed_value, result_width)
        else:
            raise TypeError("Invalid argument type for indexing")

    def __iter__(self):
        for i in range(self.__width):
            yield self[i]

    def __bin_str(self):
        bin_str = bin(self.value)[2:].zfill(self.__width)
        grouped = [bin_str[max(i - 4, 0):i] for i in range(len(bin_str), 0, -4)]
        return "_".join(reversed(grouped))

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
        return (f"bin: {self.__bin_str()}, "
                f"hex: {self.__hex_str()}, "
                f"uint: {self.as_uint_value()}, "
                f"sint: {self.as_sint_value()}")




# Example usage:
if __name__ == "__main__":
    # Bits example
    v_a = Bits(0b1010, 4)
    v_b = Bits(0b1100, 4)
    print(v_a & v_b)  # Bits: bin: 1000, hex: 8, uint: 8, sint: 8
    print(v_a | v_b)  # Bits: bin: 1110, hex: e, uint: 14, sint: 14
    print(v_a ^ v_b)  # Bits: bin: 110, hex: 6, uint: 6, sint: 6
    print(~v_a)       # Bits: bin: 1101, hex: d, uint: 13, sint: -3

    # singed example
    v_a = Bits(-3, 4)
    try:
        v_b = Bits(-5, 3)
    except AssertionError as e:
        print(e)
    v_c = Bits(-1, 1)
    v_d = Bits(1, 1)
    v_e = Bits(-4, 3)
    print(v_a)
    print(v_b)
    print(v_c)
    print(v_d)
    print(v_e)

    # Bits example more than 64 bits
    v_a = Bits(0b1010, 65)
    v_b = Bits(0b1100, 67)
    print(v_a & v_b)  # Bits: bin: 1000, hex: 8, uint: 8, sint: 8
    print(v_a | v_b)  # Bits: bin: 1110, hex: e, uint: 14, sint: 14
    print(v_a ^ v_b)  # Bits: bin: 1110, hex: e, uint: 14, sint: 14
    print(~v_a)       # Bits: bin: 11110101, hex: f5, uint: 245, sint: -11

    v_a = Bits(2**64+1, 65)
    v_b = Bits(2**64, 67)
    print("v_a: ", v_a)
    print("v_b: ", v_b)
    print(v_a & v_b)  # Bits: bin: 1000, hex: 8, uint: 8, sint: 8
    print(v_a | v_b)  # Bits: bin: 1110, hex: e, uint: 14, sint: 14
    print(v_a ^ v_b)  # Bits: bin: 1110, hex: e, uint: 14, sint: 14
    print(~v_a)

    # Bits arithmetic operations example
    v_a = Bits(0b1010, 7)
    v_b = Bits(0b1100, 8)
    print("v_a: ", v_a)
    print("v_b: ", v_b)
    print(v_a + v_b)  # Bits: bin: 0_0001_0110, hex: 016, uint: 22, sint: 22
    print(v_a - v_b)  # Bits: bin: 1_1111_1110, hex: 1fe, uint: 62, sint: -2
    print(v_a * v_b)  # Bits: 000_0000_0111_1000, hex: 0078, uint: 120, sint: 120
    print(v_a >> 3)   # Bits: bin: 000_0001, hex: 01, uint: 1, sint: 1
    print(v_b << 2)   # Bits: bin: 0011_0000, hex: 30, uint: 48, sint: 48
    print(v_a + v_b + v_a - v_b * v_a)  # Bits: bin: 1111_1111_1010_1000, hex: ffa8, uint: 65448, sint: -88

    # Bits slice example
    v_a = Bits(0b1010, 7)
    print(v_a[0])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
    print(v_a[1])  # Bits: bin: 1, hex: 1, uint: 1, sint: 1
    print(v_a[2])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
    print(v_a[3])  # Bits: bin: 1, hex: 1, uint: 1, sint: 1
    print(v_a[4])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
    print(v_a[5])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
    print(v_a[6])  # Bits: bin: 1, hex: 1, uint: 1, sint: 1
    try:
        print(v_a[7])  # error
    except ValueError as e:
        print(e)
    print(v_a[0:3])  # Bits: bin: 0101, hex: 5, uint: 5, sint: 5
    print(v_a[3:0])  # Bits: bin: 1010, hex: a, uint: 10, sint: 10
    print(v_a[3:0][0])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
    print(v_a[3:0][1])  # Bits: bin: 1, hex: 1, uint: 1, sint: 1
    print(v_a[3:0][2])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
    print(v_a[3:0][3])  # Bits: bin: 1, hex: 1, uint: 1, sint: 1
    try:
        print(v_a[3:0][4])  # error
    except ValueError as e:
        print(e)
    print(v_a[0:6]) # Bits: bin: 010_1000, hex: 28, uint: 40, sint: 40
    print(v_a[6:0]) # Bits: bin: 000_1010, hex: 0a, uint: 10, sint: 10

    for bit in v_a:
        print(bit)