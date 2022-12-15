# input_items = open('./example-input.txt').read().split('\n')
input_items = open('./input.txt').read().split('\n')

lines = []
MIN_X = float('inf')
MAX_X = float('-inf')
MAX_Y = float('-inf')

ROCK = '#'
SAND = 'o'

# Let's crop the image on the X axis - like it was in the example images
# First loop figures out the size
for line in input_items:
    for points in line.split(' -> '):
        x, y = map(int, points.split(','))
        MIN_X = min(MIN_X, x)
        MAX_X = max(MAX_X, x)
        MAX_Y = max(MAX_Y, y)

MIN_X -= int(MIN_X / 2)
MAX_X += int(MAX_X / 2)

WIDTH = MAX_X - MIN_X
HEIGHT = MAX_Y

# Read input, and adjusted for crop
for line in input_items:
    lines.append([])
    for points in line.split(' -> '):
        x, y = map(int, points.split(','))
        lines[-1].append((x - MIN_X, y))

grid = []
for rows in range(HEIGHT + 1):
    grid.append(['.' for col in range(WIDTH + 1)])

# Add INF flow
grid.append(['.' for col in range(WIDTH + 1)])
grid.append(['#' for col in range(WIDTH + 1)])
HEIGHT += 2

for line in lines:
    # Draw first rock
    x_start, y_start = line[0]
    grid[y_start][x_start] = ROCK

    # Draw rest of the connected rocks
    for x_end, y_end in line[1:]:
        xdir = 1 if x_start < x_end else -1
        for x_mid in range(x_start, x_end + xdir, xdir):
            ydir = 1 if y_start < y_end else -1
            for y_mid in range(y_start, y_end + ydir, ydir):
                grid[y_mid][x_mid] = ROCK

        # Before we draw the next one, mark that we are starting from the end of the current
        x_start = x_end
        y_start = y_end

SAND_START_X = 500 - MIN_X
SAND_START_Y = 0
LOST_SAND_LIMIT = 100
stopped_sand_count = 0
lost_sand_count = 0
ready_for_grain = True


def dir_is_blocked(x, y, dx, dy):
    return grid[y + dy][x + dx] in (ROCK, SAND)


def dir_is_abyss(x, y):
    return any([
        x < 0,
        y < 0,
        y >= HEIGHT,
        x >= WIDTH,
    ])


while lost_sand_count <= LOST_SAND_LIMIT:

    if ready_for_grain:
        ready_for_grain = False
        # Drop 1 new grain of sand
        sx, sy = (SAND_START_X, SAND_START_Y)
        # Check if the sand hole is blocked
        if dir_is_blocked(sx, sy, 0, 0):
            break

    POSSIBLE_DIRECTIONS = [(0, 1), (-1, 1), (1, 1)]
    for dx, dy in POSSIBLE_DIRECTIONS:
        if not dir_is_abyss(sx, sy) and not dir_is_blocked(sx, sy, dx, dy):
            sx += dx
            sy += dy
            break
    else:
        if dir_is_abyss(sx, sy):
            lost_sand_count += 1
        else:
            stopped_sand_count += 1
            ready_for_grain = True
            grid[sy][sx] = SAND

    grid_copy = []
    for row in grid:
        grid_copy.append(row.copy())

    if not dir_is_abyss(sx, sy):
        grid_copy[sy][sx] = SAND

print(stopped_sand_count)
