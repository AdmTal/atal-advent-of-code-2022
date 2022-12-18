import numpy as np
import matplotlib.pyplot as plt

input_items = open('./example-input.txt').read().split('\n')
# input_items = open('./input.txt').read().split('\n')


MAXES = [float('-inf'), float('-inf'), float('-inf')]


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

        # Touching == 2 same, 1 off by one
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

answer = 0
for cube in cubes:
    print(f'{cube.id} -> {cube.get_sides_exposed()} :: {cube.get_neighbors()}')

    answer += cube.get_sides_exposed()

print(f'Answer = {answer}')

# Set the figure size
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

data = np.random.choice([0], size=(MAXES[0] + 1, MAXES[1] + 1, MAXES[2] + 1))

for cube in cubes:
    x, y, z = cube.coords
    data[x][y][z] = 1

# Create a new figure
fig = plt.figure()

# Axis with 3D projection
ax = fig.add_subplot(projection='3d')

# Plot the voxels
ax.voxels(data, edgecolor="k", facecolors='green')

# Display the plot
plt.show()
