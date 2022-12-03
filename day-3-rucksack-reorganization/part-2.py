rucksack_inventories = open('./input.txt').read().split('\n')


def groups(array, group_size=3):
    for i in range(0, len(array), group_size):
        yield [set(x) for x in array[i:i + group_size]]


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
