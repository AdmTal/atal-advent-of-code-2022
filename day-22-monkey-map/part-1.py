import re

# input_items = open('./example-input.txt').read().split('\n')
input_items = open('./input.txt').read().split('\n')

grid = [[col for col in row] for row in input_items[:-2]]
HEIGHT = len(grid)
WIDTH = len(grid[0])
steps = [i if i.isalpha() else int(i) for i in re.findall('(\d+|[RL])', input_items[-1])]

# FILL MISSING SPOTS
for row in grid:
    row += [' '] * (WIDTH - len(row))

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3


def find_start(grid):
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if grid[row][col] == '.':
                return row, col


import os
import time


def dir_char(d):
    if d == LEFT:
        return '<'
    if d == RIGHT:
        return '>'
    if d == UP:
        return '^'
    return 'V'


def print_grid(row, col, d):
    return
    global grid
    _g = [r.copy() for r in grid]
    _g[row][col] = dir_char(d)
    time.sleep(.1)
    os.system('clear')
    for row in _g:
        print(''.join(row))


def pprint(message):
    print(message)
    pass


def get_next_step(row, col, direction):
    global grid
    pprint(f'\t\t\t\t{row}, {col}, {direction}')
    drow, dcol = None, None
    if direction == RIGHT:
        drow, dcol = row, col + 1
    elif direction == LEFT:
        drow, dcol = row, col - 1
    elif direction == UP:
        drow, dcol = row - 1, col
    elif direction == DOWN:
        drow, dcol = row + 1, col

    over_the_top = drow < 0
    over_the_left = dcol < 0
    over_the_right = dcol >= WIDTH
    over_the_bottom = drow >= HEIGHT

    if not any([
        over_the_top,
        over_the_left,
        over_the_right,
        over_the_bottom,
    ]):
        curr_space_not_walkable = grid[drow][dcol] == ' '
        over_the_top = curr_space_not_walkable and direction == UP
        over_the_left = curr_space_not_walkable and direction == LEFT
        over_the_right = curr_space_not_walkable and direction == RIGHT
        over_the_bottom = curr_space_not_walkable and direction == DOWN

    if over_the_top:
        drow = HEIGHT - 1  # jump to bottom
        pprint(f'\t\t\t\tjump bottom')
        while grid[drow][dcol] not in ('.', '#'):
            drow -= 1
    elif over_the_bottom:
        drow = 0  # jump to top
        pprint(f'\t\t\t\tjump top')
        while grid[drow][dcol] not in ('.', '#'):
            drow += 1
    elif over_the_left:
        pprint(f'\t\t\t\tjump right')
        dcol = WIDTH - 1  # jump to RIGHT
        while grid[drow][dcol] not in ('.', '#'):
            dcol -= 1
    elif over_the_right:
        pprint(f'\t\t\t\tjump left')
        dcol = 0  # jump to LEFT
        while grid[drow][dcol] not in ('.', '#'):
            dcol += 1

    # If next space is not walkable, just stop trying
    if grid[drow][dcol] == '#':
        return None

    return drow, dcol


curr_row, curr_col = find_start(grid)

next_step_is_number = True
current_direction = RIGHT

print(' '.join([str(i) for i in steps]))

while steps:

    next_step = steps.pop(0)
    pprint(f'Step is {next_step}')

    if next_step_is_number:
        pprint(f'\tWalk {next_step} to the {dir_char(current_direction)}')
        next_step_is_number = False
        while next_step:
            pprint(f'\t\t{next_step} steps remaining : {curr_row, curr_col}')
            next_step -= 1
            next_step_position = get_next_step(curr_row, curr_col, current_direction)
            if not next_step_position:
                pprint('\t\t\twe are blocked')
                break
            curr_row, curr_col = next_step_position
            print_grid(curr_row, curr_col, current_direction)

    else:
        next_step_is_number = True
        prev_dir = current_direction
        if next_step == 'L':
            if current_direction == LEFT:
                current_direction = DOWN
            elif current_direction == RIGHT:
                current_direction = UP
            elif current_direction == UP:
                current_direction = LEFT
            elif current_direction == DOWN:
                current_direction = RIGHT
        else:
            if current_direction == LEFT:
                current_direction = UP
            elif current_direction == RIGHT:
                current_direction = DOWN
            elif current_direction == UP:
                current_direction = RIGHT
            elif current_direction == DOWN:
                current_direction = LEFT
        pprint(f'Turn {next_step} :: {dir_char(prev_dir)} {dir_char(current_direction)}')
        print_grid(curr_row, curr_col, current_direction)

items = [
    1000 * (curr_row + 1),
    4 * (curr_col + 1),
    current_direction
]
answer = sum(items)

print(f'row={curr_row}; col={curr_col}; dir={current_direction}')
print(items)
print(f'Answer={answer}')
