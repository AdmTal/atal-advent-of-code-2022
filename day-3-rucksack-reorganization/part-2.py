rucksack_inventories = open('./input.txt').read().split('\n')

GROUP_SIZE = 3


def groups(array, chunk_size=GROUP_SIZE):
    for i in range(0, len(array), chunk_size):
        yield [set(x) for x in array[i:i + chunk_size]]


def priority(letter):
    ascii_offset = 38 if letter.isupper() else 96
    return ord(letter) - ascii_offset


priorities_sum = 0

for first, second, third in groups(rucksack_inventories):
    common_item = first \
        .intersection(second) \
        .intersection(third) \
        .pop()

    priorities_sum += priority(common_item)

print(priorities_sum)
