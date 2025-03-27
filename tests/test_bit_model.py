import pytest
from pymodel.bit_model import Bits

# # Bits example
# v_a = Bits(0b1010, 4)
# v_b = Bits(0b1100, 4)
# print(v_a & v_b)  # Bits: bin: 1000, hex: 8, uint: 8, sint: 8
# print(v_a | v_b)  # Bits: bin: 1110, hex: e, uint: 14, sint: 14
# print(v_a ^ v_b)  # Bits: bin: 110, hex: 6, uint: 6, sint: 6
# print(~v_a)  # Bits: bin: 1101, hex: d, uint: 13, sint: -3

# # singed example
# v_a = Bits(-3, 4)
# try:
#     v_b = Bits(-5, 3)
# except AssertionError as e:
#     print(e)
# v_c = Bits(-1, 1)
# v_d = Bits(1, 1)
# v_e = Bits(-4, 3)
# print(v_a)
# print(v_b)
# print(v_c)
# print(v_d)
# print(v_e)

# # Bits example more than 64 bits
# v_a = Bits(0b1010, 65)
# v_b = Bits(0b1100, 67)
# print(v_a & v_b)  # Bits: bin: 1000, hex: 8, uint: 8, sint: 8
# print(v_a | v_b)  # Bits: bin: 1110, hex: e, uint: 14, sint: 14
# print(v_a ^ v_b)  # Bits: bin: 1110, hex: e, uint: 14, sint: 14
# print(~v_a)  # Bits: bin: 11110101, hex: f5, uint: 245, sint: -11

# v_a = Bits(2**64 + 1, 65)
# v_b = Bits(2**64, 67)
# print("v_a: ", v_a)
# print("v_b: ", v_b)
# print(v_a & v_b)  # Bits: bin: 1000, hex: 8, uint: 8, sint: 8
# print(v_a | v_b)  # Bits: bin: 1110, hex: e, uint: 14, sint: 14
# print(v_a ^ v_b)  # Bits: bin: 1110, hex: e, uint: 14, sint: 14
# print(~v_a)

# # Bits arithmetic operations example
# v_a = Bits(0b1010, 7)
# v_b = Bits(0b1100, 8)
# print("v_a: ", v_a)
# print("v_b: ", v_b)
# print(v_a + v_b)  # Bits: bin: 0_0001_0110, hex: 016, uint: 22, sint: 22
# print(v_a - v_b)  # Bits: bin: 1_1111_1110, hex: 1fe, uint: 62, sint: -2
# print(v_a * v_b)  # Bits: 000_0000_0111_1000, hex: 0078, uint: 120, sint: 120
# print(v_a >> 3)  # Bits: bin: 000_0001, hex: 01, uint: 1, sint: 1
# print(v_b << 2)  # Bits: bin: 0011_0000, hex: 30, uint: 48, sint: 48
# print(
#     v_a + v_b + v_a - v_b * v_a
# )  # Bits: bin: 1111_1111_1010_1000, hex: ffa8, uint: 65448, sint: -88

# # Bits slice example
# v_a = Bits(0b1010, 7)
# print(v_a[0])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
# print(v_a[1])  # Bits: bin: 1, hex: 1, uint: 1, sint: 1
# print(v_a[2])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
# print(v_a[3])  # Bits: bin: 1, hex: 1, uint: 1, sint: 1
# print(v_a[4])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
# print(v_a[5])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
# print(v_a[6])  # Bits: bin: 1, hex: 1, uint: 1, sint: 1
# try:
#     print(v_a[7])  # error
# except ValueError as e:
#     print(e)
# print(v_a[0:3])  # Bits: bin: 0101, hex: 5, uint: 5, sint: 5
# print(v_a[3:0])  # Bits: bin: 1010, hex: a, uint: 10, sint: 10
# print(v_a[3:0][0])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
# print(v_a[3:0][1])  # Bits: bin: 1, hex: 1, uint: 1, sint: 1
# print(v_a[3:0][2])  # Bits: bin: 0, hex: 0, uint: 0, sint: 0
# print(v_a[3:0][3])  # Bits: bin: 1, hex: 1, uint: 1, sint: 1
# try:
#     print(v_a[3:0][4])  # error
# except ValueError as e:
#     print(e)
# print(v_a[0:6])  # Bits: bin: 010_1000, hex: 28, uint: 40, sint: 40
# print(v_a[6:0])  # Bits: bin: 000_1010, hex: 0a, uint: 10, sint: 10

# for bit in v_a:
#     print(bit)


def test_bitwise_operations():
    v_a = Bits(0b1010, 4)
    v_b = Bits(0b1100, 4)
    assert (v_a & v_b).value == 0b1000
    assert (v_a | v_b).value == 0b1110
    assert (v_a ^ v_b).value == 0b0110
    assert (~v_a).value == 0b0101


def test_signed_values():
    v_a = Bits(-3, 4)
    assert v_a.as_sint_value() == -3
    assert v_a.as_uint_value() == 13

    with pytest.raises(AssertionError):
        Bits(-5, 3)


def test_shift_operations():
    v_a = Bits(0b1010, 4)
    assert (v_a >> 2).value == 0b0010
    assert (v_a << 1).value == 0b0100


def test_arithmetic_operations():
    v_a = Bits(0b1010, 4)
    v_b = Bits(0b1100, 4)
    assert (v_a + v_b).value == 0b10110
    assert (v_a - v_b).as_sint_value() == -2
    assert (v_a * v_b).value == 0b01111000
    assert (v_a // v_b).value == 0
    assert (v_a % v_b).value == 0b1010


def test_comparison_operations():
    v_a = Bits(0b1010, 4)
    v_b = Bits(0b1100, 4)
    assert (v_a == v_b).value == 0
    assert (v_a != v_b).value == 1
    assert (v_a < v_b).value == 1
    assert (v_a <= v_b).value == 1
    assert (v_a > v_b).value == 0
    assert (v_a >= v_b).value == 0


def test_indexing_and_slicing():
    v_a = Bits(0b1010101, 7)
    assert v_a[0].value == 1
    assert v_a[1].value == 0
    assert v_a[2].value == 1
    assert v_a[3:0].value == 0b0101
    assert v_a[0:3].value == 0b1010

    with pytest.raises(ValueError):
        _ = v_a[7]

    with pytest.raises(ValueError):
        _ = v_a[3:0][4]


def test_large_bit_vectors():
    v_a = Bits(2**64 + 1, 65)
    v_b = Bits(2**64, 67)
    assert (v_a & v_b).value == 2**64
    assert (v_a | v_b).value == 2**64 + 1
    assert (v_a ^ v_b).value == 1
    assert (~v_a).value == (2**65 - 1) - (2**64 + 1)


def test_iteration():
    v_a = Bits(0b1010101, 7)
    bits = [bit.value for bit in v_a]
    assert bits == [1, 0, 1, 0, 1, 0, 1]
