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

    # this condition is the kind of thing I have to figure out on paper every time...
    # 100% I'll forget what this means in a couple of min
    if c <= b <= d or d >= a and c <= b:
        num_fully_covered_ranges += 1

print(num_fully_covered_ranges)
