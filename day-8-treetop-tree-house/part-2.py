grid_rows = open('./input.txt').read().split('\n')
grid = [
    [int(col) for col in row] for row in grid_rows
]

NUM_COLS = len(grid)
NUM_ROWS = len(grid[0])


def coord_is_possible(x, y):
    return not any([
        x < 0,
        y < 0,
        x >= NUM_ROWS,
        y >= NUM_ROWS
    ])


def trees_visible_in_direction(x, y, x_dir, y_dir):
    global grid
    trees_visible = 0

    this_tree = grid[x][y]

    while coord_is_possible(x + x_dir, y + y_dir):
        x = x + x_dir
        y = y + y_dir
        next_tree = grid[x][y]
        trees_visible += 1
        if next_tree >= this_tree:
            return trees_visible

    return trees_visible


def get_scenic_score(x, y):
    global grid

    scores = [
        trees_visible_in_direction(x, y, -1, 0),
        trees_visible_in_direction(x, y, 1, 0),
        trees_visible_in_direction(x, y, 0, -1),
        trees_visible_in_direction(x, y, 0, 1),
    ]
    scenic_score = scores[0]
    for score in scores[1:]:
        scenic_score *= score

    return scenic_score


max_scenic_score = float('-inf')
for x in range(NUM_COLS):
    for y in range(NUM_ROWS):
        max_scenic_score = max(max_scenic_score, get_scenic_score(x, y))

print(max_scenic_score)

