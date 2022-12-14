from pprint import pprint

input_items = open('./example-input.txt').read().split('\n')
# input_items = open('./input.txt').read().split('\n')

lines = []
MIN_X = float('inf')
MAX_X = float('-inf')
MAX_Y = float('-inf')

# Let's crop the image on the X axis - like it was in the example images
# First loop figures out the size
for line in input_items:
    for points in line.split(' -> '):
        x, y = map(int, points.split(','))
        MIN_X = min(MIN_X, x)
        MAX_X = max(MAX_X, x)
        MAX_Y = max(MAX_Y, y)

WIDTH = MAX_X - MIN_X
HEIGHT = MAX_Y

# Read input, and adjust it for the above mentioned cropping, and 0-index offset
for line in input_items:
    lines.append([])
    for points in line.split(' -> '):
        x, y = map(int, points.split(','))
        lines[-1].append((x - MIN_X - 1, y - 1))

grid = []
for rows in range(WIDTH):
    grid.append(['.' for col in range(HEIGHT)])

for line in lines:
    # Draw first rock
    x_start, y_start = line[0]
    grid[y_start][x_start] = '#'
    # Draw rest of rocks
    for x_end, y_end in line[1:]:
        for x_mid in range(x_start, x_end + 1):
            for y_mid in range(y_start, y_end + 1):
                grid[y_mid][x_mid] = '#'

pprint(grid)
