from functools import cache

grid_rows = open('./input.txt').read().split('\n')
grid = [
    [int(col) for col in row] for row in grid_rows
]

NUM_COLS = len(grid)
NUM_ROWS = len(grid[0])


@cache
def highest_tree_from_left(x, y):
    global grid
    if y == 0:
        return grid[x][y]

    return max(grid[x][y], highest_tree_from_left(x, y - 1))


@cache
def highest_tree_from_right(x, y):
    global grid
    if y == NUM_ROWS - 1:
        return grid[x][y]

    return max(grid[x][y], highest_tree_from_right(x, y + 1))


@cache
def highest_tree_from_top(x, y):
    global grid
    if x == 0:
        return grid[x][y]

    return max(grid[x][y], highest_tree_from_top(x - 1, y))


@cache
def highest_tree_from_bottom(x, y):
    global grid
    if x == NUM_COLS - 1:
        return grid[x][y]

    return max(grid[x][y], highest_tree_from_bottom(x + 1, y))


@cache
def is_tree_visible(x, y):
    global grid

    if x == 0 or y == 0 or x == NUM_ROWS - 1 or y == NUM_COLS - 1:
        return True

    current = grid[x][y]

    return any([
        current > highest_tree_from_top(x - 1, y),
        current > highest_tree_from_left(x, y - 1),
        current > highest_tree_from_right(x, y + 1),
        current > highest_tree_from_bottom(x + 1, y),
    ])


num_visible_trees = 0
for x in range(NUM_COLS):
    for y in range(NUM_ROWS):
        num_visible_trees += int(is_tree_visible(x, y))

print(num_visible_trees)
