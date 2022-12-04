elf_pair_assignments = [
    [
        [
            int(k) for k in j.split('-')
        ]
        for j in i.split(',')
    ] for i in open('./input.txt').read().split('\n')
]

num_fully_covered_ranges = 0
for elf_a_assignments, elf_b_assignments in elf_pair_assignments:
    a, b = elf_a_assignments
    c, d = elf_b_assignments

    if c >= a and d <= b or a >= c and b <= d:
        num_fully_covered_ranges += 1

print(num_fully_covered_ranges)
