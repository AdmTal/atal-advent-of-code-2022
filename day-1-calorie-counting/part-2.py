

elf_calorie_inventory_items = open('./input.txt').read().split('\n')

highest_calories_held_by_a_single_elf = float('-inf')

current_elf_calories = 0
for elf_calorie_inventory_item in elf_calorie_inventory_items:

    if not elf_calorie_inventory_item:
        highest_calories_held_by_a_single_elf = max(current_elf_calories, highest_calories_held_by_a_single_elf)
        current_elf_calories = 0
        continue

    current_elf_calories += int(elf_calorie_inventory_item)

print(highest_calories_held_by_a_single_elf)
