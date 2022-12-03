rucksack_inventories = open('./input.txt').read().split('\n')


def priority(letter):
    ascii_offset = 38 if letter.isupper() else 96
    return ord(letter) - ascii_offset


priorities_sum = 0

for rucksack_inventory in rucksack_inventories:
    item_count = len(rucksack_inventory)
    middle = int(item_count / 2)
    first_compartment = rucksack_inventory[:middle]
    second_compartment = rucksack_inventory[middle:]

    common_item = set(first_compartment).intersection(set(second_compartment)).pop()

    priorities_sum += priority(common_item)

print(priorities_sum)
