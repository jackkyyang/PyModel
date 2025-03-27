from pymodel import Bits


def full_adder(a: Bits, b: Bits, cin: Bits) -> tuple[Bits, Bits]:
    """
    Full adder function that takes three bits (a, b, cin) and returns the sum and carry out.
    :param a: First bit
    :param b: Second bit
    :param cin: Carry in bit
    :return: Tuple of sum and carry out bits
    """
    assert len(a) == len(b) == len(cin), "All inputs must have the same width"

    # Calculate sum and carry out
    sum_ = a ^ b ^ cin
    cout = (a & b) | (cin & a) | (cin & b)

    return sum_, cout


if __name__ == "__main__":
    # Example usage
    b0 = Bits(0, 1)
    b1 = Bits(1, 1)

    sum_, cout = full_adder(b0, b1, b1)
    print(f"Sum: {sum_.value}, Carry out: {cout.value}")

    sum_, cout = full_adder(b1, b1, b1)
    print(f"Sum: {sum_.value}, Carry out: {cout.value}")

    sum_, cout = full_adder(b0, b0, b1)
    print(f"Sum: {sum_.value}, Carry out: {cout.value}")

    sum_, cout = full_adder(b0, b0, b0)
    print(f"Sum: {sum_.value}, Carry out: {cout.value}")
