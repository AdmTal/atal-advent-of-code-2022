import numpy as np

# FOR PART 2 - We need to discount air pockets.
# I guess we could just fill the airpockets with blocks - and re-run same ALG from part 1.
# So .... we only need to identify the COORDs of an Air Pocket.
# A air Pocket is any cube that can trace an unblocked path from the edge of the graph

# input_items = open('./example-input.txt').read().split('\n')
input_items = open('./input.txt').read().split('\n')

MAXES = [float('-inf'), float('-inf'), float('-inf')]


def ts(x, y, z):
    return f'{x}|{y}|{z}'


import sys
sys.setrecursionlimit(5000)


def coord_is_air_pocket(x, y, z, visited_str=''):
    global memo
    if memo[x][y][z] is not None:
        return memo[x][y][z]

    # Return FALSE if this COORD touches any edge
    if any([
        x <= 0, y <= 0, z <= 0,
        x >= MAXES[0], y >= MAXES[1], z >= MAXES[2],
    ]):
        return False

    visited = {k: True for k in visited_str.split(',')}

    # Return False if all neighbors not AIR POCKETS
    for dx, dy, dz in [
        [x, y, z - 1],
        [x, y, z + 1],
        [x, y - 1, z],
        [x, y + 1, z],
        [x - 1, y, z],
        [x + 1, y, z],
    ]:
        # Don't re-visit anything
        if ts(dx, dy, dz) in visited:
            continue
        # Is the neighbor a WALL
        if input_cube_lookup[dx][dy][dz]:
            continue
        visited[ts(dx, dy, dz)] = True
        if not coord_is_air_pocket(dx, dy, dz, ','.join(visited.keys())):
            memo[x][y][z] = False
            return False

    memo[x][y][z] = True
    return True


class Cube(object):
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
        self._neighbors = {}

    @property
    def coords(self):
        return self._x, self._y, self._z

    @property
    def id(self):
        return ','.join(list(map(str, [self._x, self._y, self._z])))

    def __str__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def get_neighbors(self):
        resp = ''
        for n in self._neighbors.values():
            resp += f'({n.id}),'
        return resp

    def add_neighbor_if_connected(self, other_cube):

        # 2 same, 1 diff, off by one
        same = 0
        diff = 0
        for a, b in zip(self.coords, other_cube.coords):
            if a == b:
                same += 1
                continue
            diff = abs(a - b)

        if same != 2 or diff != 1:
            return

        self._neighbors[other_cube.id] = other_cube

    def get_sides_exposed(self):
        return 6 - len(self._neighbors)


cubes = []
for line in input_items:
    x, y, z = list(map(int, line.split(',')))
    MAXES[0] = max(MAXES[0], x)
    MAXES[1] = max(MAXES[1], y)
    MAXES[2] = max(MAXES[2], z)

    new_cube = Cube(x, y, z)
    for other_cube in cubes:
        other_cube.add_neighbor_if_connected(new_cube)
        new_cube.add_neighbor_if_connected(other_cube)

    cubes.append(new_cube)

memo = input_cube_lookup = np.random.choice([None], size=(MAXES[0] + 1, MAXES[1] + 1, MAXES[2] + 1))
input_cube_lookup = np.random.choice([0], size=(MAXES[0] + 1, MAXES[1] + 1, MAXES[2] + 1))
for cube in cubes:
    x, y, z = cube.coords
    input_cube_lookup[x][y][z] = 1
print('x max = ', MAXES[0])
print('y max = ', MAXES[1])
print('z max = ', MAXES[2])
print(f'search space = {MAXES[0] * MAXES[1] * MAXES[2]}')
# FILL IN THE AIR POCKETS BY ADDING MORE CUBES TO THE INPUT
for x in reversed(range(MAXES[0])):
    for y in reversed(range(MAXES[1])):
        for z in reversed(range(MAXES[2])):
            item = f'{x},{y},{z}'
            # Skip any cubes that are on the input list
            if input_cube_lookup[x][y][z]:
                continue
            v = ts(x, y, z)
            if coord_is_air_pocket(x, y, z, v):
                input_items.append(item)
                print(f'\tFilling air bubble -> {input_items[-1]}')

cubes = []

for line in input_items:
    x, y, z = list(map(int, line.split(',')))

    new_cube = Cube(x, y, z)
    for other_cube in cubes:
        other_cube.add_neighbor_if_connected(new_cube)
        new_cube.add_neighbor_if_connected(other_cube)

    cubes.append(new_cube)

answer = 0
for cube in cubes:
    answer += cube.get_sides_exposed()

print(f'Answer = {answer}')
