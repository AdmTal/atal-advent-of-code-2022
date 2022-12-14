from pprint import pprint

input_items = open('./example-input.txt').read().split('\n')
# input_items = open('./input.txt').read().split('\n')

lines = []
MIN_X = float('inf')
MAX_X = float('-inf')
MIN_Y = float('inf')
MAX_Y = float('-inf')
for line in input_items:
    lines.append([])
    for points in line.split(' -> '):
        x, y = map(int, points.split(','))
        lines[-1].append((x, y))
        MIN_X = min(MIN_X, x)
        MAX_X = max(MAX_X, x)
        MIN_Y = min(MIN_Y, y)
        MAX_Y = max(MAX_Y, y)

print([
    MIN_X,
    MIN_Y,
    MAX_X,
    MAX_Y,
])

WIDTH = MAX_X - MIN_X
HEIGHT = MAX_Y - MIN_Y

print([WIDTH, HEIGHT])

grid = []
for rows in range(WIDTH):
    grid.append(['.' for col in range(HEIGHT)])

for line in lines:
    x, y = line[0]
    print(f'({x - MIN_X}, {y - MIN_Y})')
    # grid[y - MIN_Y][x - MIN_X] = 'A'
    # for x, y in line[1:]:
    #     print(f'\t({x - MIN_X}, {y - MIN_Y})')
    # Draw first rock
    # Draw rest of rocks
    pass

pprint(grid)
