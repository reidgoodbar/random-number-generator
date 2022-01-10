"""
    Generate random array of 0s and 1s of length count using builtin random and pseudo lfsr
    Compare the outputs of the two
"""

import random
from collections import Counter


def normal_random(seed, count):
    """
        Generate random array of 0s and 1s of length count using builtin random
    """
    random.seed(seed)
    n_rn = [random.randrange(0, 2) for _ in range(count)]
    return n_rn


def update_register(register, length, positions):
    """
        Adds bit to end of register using the positions array
    """
    res_bit = 0
    for i in positions:
        res_bit ^= (register >> i) & 1
    if res_bit == 0:
        return register

    register |= 1 << length - 1

    return register


def get_register_length(register):
    """
        Gets the number of bits in a register, where shifting right becomes 0
    """
    temp = register
    length = 0
    while temp != 0:
        temp >>= 1
        length += 1
    return length


def lfsr(seed, count):
    """
        Generate random array of 0s and 1s of length count using a basic LFSR
    """
    settings = seed & int("0xFFFFFF", 16)
    position_0 = settings & int("1", 16)
    position_1 = settings & int("0xF", 16)
    position_2 = settings & int("0xF0", 16)
    position_3 = settings & int("0xF00", 16)
    position_4 = settings & int("0xF000", 16)
    position_5 = settings & int("0xF0000", 16)
    position_6 = settings & int("0xF00000", 16)

    register = seed >> 4 * len("FFFFFF")
    lfsr_rn = []
    length = get_register_length(register)

    # Run LFSR to move past seed
    for _ in range(100000):
        register >>= 1
        register = update_register(
            register,
            length,
            [
                position_0,
                position_1,
                position_2,
                position_3,
                position_4,
                position_5,
                position_6,
            ],
        )

    # Build random list
    for _ in range(count):
        lfsr_rn.append(register & 1)
        register >>= 1
        register = update_register(
            register,
            length,
            [position_1, position_2, position_3, position_4, position_5],
        )

    return lfsr_rn


def get_seed():
    """
        Have user enter really big seed
    """
    seed = 0
    while seed < 1000000000:
        seed = int(input("Please input random seed int > 1000000: "))
    return seed


def main():
    """
        Main method
    """
    seed = get_seed()
    count = 10000
    n_rn = normal_random(seed, count)
    lfsr_rn = lfsr(seed, count)

    print("Classic RNG Difference Between 1s and 0s:")
    print(abs(Counter(n_rn)[1] - Counter(n_rn)[0]))
    print("Pseudo LFSR RNG Difference Between 1s and 0s:")
    print(abs(Counter(lfsr_rn)[1] - Counter(lfsr_rn)[0]))


if __name__ == "__main__":
    main()
