import heapq

elf_calorie_inventory_items = open('./input.txt').read().split('\n')

current_elf_calories = 0
elf_calorie_totals_max_heap = []
for elf_calorie_inventory_item in elf_calorie_inventory_items:

    if not elf_calorie_inventory_item:
        heapq.heappush(elf_calorie_totals_max_heap, -current_elf_calories)
        current_elf_calories = 0
        continue

    current_elf_calories += int(elf_calorie_inventory_item)

# Get sum of calories for top 3 elves
sum_top_three_elf_calories = sum([
    -heapq.heappop(elf_calorie_totals_max_heap),
    -heapq.heappop(elf_calorie_totals_max_heap),
    -heapq.heappop(elf_calorie_totals_max_heap),
])

print(sum_top_three_elf_calories)
