import os
from time import sleep
from collections import defaultdict

# input_items = open('./example-input.txt').read().split('\n')
# input_items = open('./example-5-elves.txt').read().split('\n')
input_items = open('./input.txt').read().split('\n')


elves = []
for y in range(len(input_items)):
    row = input_items[y]
    for x in range(len(row)):
        if input_items[y][x] == '#':
            elves.append([x, y])

round_number = 1


def _grid_size_from_elves_positions(ep):
    MIN_X = float('inf')
    MIN_Y = float('inf')
    MAX_X = float('-inf')
    MAX_Y = float('-inf')
    for x, y in ep:
        MIN_X = min(x, MIN_X)
        MIN_Y = min(y, MIN_Y)
        MAX_X = max(x, MAX_X)
        MAX_Y = max(y, MAX_Y)

    WIDTH = MAX_X - MIN_X
    HEIGHT = MAX_Y - MIN_Y

    return WIDTH + 1, HEIGHT + 1


def _grid_from_elves_positions(ep):
    WIDTH, HEIGHT = _grid_size_from_elves_positions(ep)
    grid = [['.' for col in range(WIDTH)] for row in range(HEIGHT)]
    for x, y in ep:
        grid[y][x] = '#'

    return grid


def _print_grid(ep):
    grid = _grid_from_elves_positions(ep)
    for row in grid:
        print(''.join(row))


def _generate_elf_lookup(ep):
    elf_lookup = defaultdict(lambda: defaultdict(bool))
    for x, y in ep:
        elf_lookup[y][x] = True
    return elf_lookup


N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)
NE = tuple(sum(x) for x in zip(N, E))
NW = tuple(sum(x) for x in zip(N, W))
SE = tuple(sum(x) for x in zip(S, E))
SE = tuple(sum(x) for x in zip(S, E))
SW = tuple(sum(x) for x in zip(S, W))

DIRS = [NW, N, NE, W, E, SW, S, SE]

# Rules are a list of DIRS to look, and a direction to move if all are empty
RULES = [
    [[N, NE, NW], N],
    [[S, SE, SW], S],
    [[W, NW, SW], W],
    [[E, NE, SE], E],
]

print(f'Starting Grid')
_print_grid(elves)

while round_number <= 10:
    final_elf_positions = []
    elves_who_will_move = []

    elf_lookup = _generate_elf_lookup(elves)

    # Every elf checks the 8 DIR around them
    for x, y in elves:

        elf_found = False

        for dx, dy in DIRS:
            if elf_lookup[y + dy][x + dx]:
                elf_found = True
                break

        # If no elf is around, this elf does not move
        if not elf_found:
            final_elf_positions.append([x, y])
            continue

        elves_who_will_move.append([x, y])

    # Elves are considering the rules, and deciding their next potential destination
    proposed_destinations = defaultdict(lambda: defaultdict(list))
    for idx, coord in enumerate(elves_who_will_move):
        x, y = coord
        # Elf checks all rules until one hits
        destination_was_proposed = False
        for rule in RULES:
            dirs_to_check, dir_to_move_if_all_empty = rule
            elf_found = False
            for dx, dy in dirs_to_check:
                if elf_lookup[y + dy][x + dx]:
                    elf_found = True
                    break
            # If no elf is found in those DIRs, then a move will be proposed
            if not elf_found:
                dx, dy = dir_to_move_if_all_empty
                proposed_destinations[y + dy][x + dx].append(idx)
                destination_was_proposed = True
                break  # Done checking rules

        # If this elf does not move, mark its position as final
        if not destination_was_proposed:
            final_elf_positions.append([x, y])

    # Move the elves who should be moved
    for y in proposed_destinations.keys():
        for x in proposed_destinations[y].keys():
            elves_who_proposed_this_destination = proposed_destinations[y][x]
            if len(elves_who_proposed_this_destination) == 1:
                final_elf_positions.append([x, y])
            else:
                # Otherwise, find the elves who will stay still
                for idx in elves_who_proposed_this_destination:
                    final_elf_positions.append(elves_who_will_move[idx])

    # Final - rotate the rules
    RULES.append(RULES.pop(0))

    elves = final_elf_positions
    # os.system('clear')
    # _print_grid(elves)
    # sleep(.5)

    round_number += 1

grid = _grid_from_elves_positions(elves)

num_space = 0
for row in grid:
    for col in row:
        if col == '.':
            num_space += 1

print(f'Answer: {num_space}')
