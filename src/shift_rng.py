import random
from collections import Counter

def normal_random(seed, count):
    random.seed(seed)
    n_rn = [random.randrange(0,2) for _ in range(1000000)]
    return n_rn


def update_register(register, length, positions):
    res_bit = 0
    for i in positions:
        res_bit ^= ((register >> i) & 1)
    if res_bit == 0: return register

    register |= (1 << length-1)
    
    return register



def get_register_length(register):
    temp = register
    length = 0
    while temp != 0:
        temp >>= 1
        length += 1
    return length

print(update_register(1, get_register_length(3), [0,1]))

# RNG loosely based on lfsr
def lfsr(seed, count):
    settings = seed & int('0xFFFF', 16)
    position_1 = settings & int('0xF', 16)
    position_2 = settings & int('0xF0', 16)
    position_3 = settings & int('0xF00', 16)
    position_4 = settings & int('0xF000', 16)

    register = seed >> 4*len('FFFF')
    lfsr_rn = []
    length = get_register_length(register)
    for _ in range(count):
        lfsr_rn.append(register & 1)
        register >>= 1
        register = update_register(register, length, [position_1, position_2, position_3, position_4])
    return lfsr_rn


def get_seed():
    seed = 0
    while seed < 1000000:
        seed = input('Please input random seed int > 1000000: ')
    return seed


def main():
    # seed = get_seed()
    seed = 134521345234524342534425647256
    count = 100000000
    n_rn = normal_random(seed, count)
    lfsr_rn = lfsr(seed, count)
    # print(lfsr_rn)
    print(abs(Counter(n_rn)[1]-Counter(n_rn)[0]))
    print(abs(Counter(lfsr_rn)[1]-Counter(lfsr_rn)[0]))

if __name__ == "__main__":
    main()