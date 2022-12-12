from pprint import pprint
from functools import cache

input_rows = open('./example-input.txt').read().split('\n')
# input_items = open('./input.txt').read().split('\n')

X = 0
Y = 1
grid = []
START = None
END = None
for x, row in enumerate(input_rows):
    new_row = []
    for y, col in enumerate(row):

        item = ord(col) - 96
        if col == 'S':
            START = (x, y)
            item = 0
        elif col == 'E':
            END = (x, y)
            item = 0

        new_row.append(item)

    grid.append(new_row)

pprint(grid)

NUM_ROWS = len(grid)
NUM_COLS = len(grid[0])


@cache
def coord_is_possible(x, y):
    return not any([
        x < 0,
        y < 0,
        x >= NUM_ROWS,
        y >= NUM_ROWS
    ])


POSSIBLE_DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), ]


def get_shortest_path(start_x, start_y, end_x, end_y, path_taken=[]):
    print(f'({start_x},{start_y}) -- {path_taken}')
    global grid
    # If you are already at the end, exit
    if start_x == end_x and start_y == end_y:
        return path_taken

    # Figure out which options are available
    # Then figure out which option leads to a shorter path
    # Return the shortest path
    to_visit = []

    for dx, dy in POSSIBLE_DIRECTIONS:
        next_x = start_x + dx
        next_y = start_y + dy

        # Skip impossible COORDs
        if not coord_is_possible(next_x, next_y):
            continue

        # Skip visited COORDs
        if (x, y) in path_taken:
            continue

        # Skip unclimbable COORDS
        current_height = grid[start_x][start_y]
        next_height = grid[next_x][next_y]
        if current_height > next_height and next_height - current_height > 1:
            continue

        to_visit.append((next_x, next_y))

    # TODO : later ...

    shortest_path_from_here = []
    shortest_path_len_from_here = float('-inf')

    while to_visit:
        next_x, next_y = to_visit.pop(0)
        new_path = get_shortest_path(next_x, next_y, end_x, end_y, path_taken + [(next_x, next_y)])
        if len(new_path) < shortest_path_len_from_here:
            shortest_path_from_here = [(next_x, next_y)] + new_path

    # Figure out
    return path_taken + shortest_path_from_here


path_taken = [(START[X], START[Y])]
print(get_shortest_path(START[X], START[Y], END[X], END[Y], path_taken))
