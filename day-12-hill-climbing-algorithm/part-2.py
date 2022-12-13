from functools import cache
from queue import PriorityQueue

# input_rows = open('./example-input.txt').read().split('\n')
input_rows = open('./input.txt').read().split('\n')

X = 0
Y = 1
grid = []
START = None
END = None
ORD_A_POS = 96
A = 'a'
Z = 'z'
S = 'S'
E = 'E'
possible_starting_locations = []
for x, row in enumerate(input_rows):
    new_row = []
    for y, col in enumerate(row):

        item = ord(col) - ORD_A_POS
        if col == S:
            START = (x, y)
            item = ord(A) - ORD_A_POS
        elif col == E:
            END = (x, y)
            item = ord(Z) - ORD_A_POS

        if item == ord(A) - ORD_A_POS:
            possible_starting_locations.append((x, y))

        new_row.append(item)

    grid.append(new_row)

NUM_ROWS = len(grid)
NUM_COLS = len(grid[0])


def _coord_in_list(x, y, path):
    for px, py in path:
        if x == px and y == py:
            return True
    return False


class Node:
    def __init__(self, name):
        self._name = name
        self._edges = []

    @property
    def name(self):
        return self._name

    @property
    def edges(self):
        return self._edges

    def add_edge(self, node, weight):
        self._edges.append((weight, node))


@cache
def coord_is_possible(x, y):
    return not any([
        x < 0,
        y < 0,
        x >= NUM_ROWS,
        y >= NUM_COLS
    ])


def name_node(x, y):
    return f'{x},{y}'


POSSIBLE_DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def copy_graph():
    input_graph = {}
    for x in range(NUM_ROWS):
        for y in range(NUM_COLS):
            node_name = name_node(x, y)
            input_graph[node_name] = Node(node_name)

    for x in range(NUM_ROWS):
        for y in range(NUM_COLS):
            node_name = name_node(x, y)

            for dx, dy in POSSIBLE_DIRECTIONS:
                next_x = x + dx
                next_y = y + dy

                # Skip impossible COORDs
                if not coord_is_possible(next_x, next_y):
                    continue

                # Skip unclimbable COORDS
                current_height = grid[x][y]
                next_height = grid[next_x][next_y]
                if next_height > current_height and next_height != current_height + 1:
                    continue

                next_node_name = name_node(next_x, next_y)
                current_node = input_graph[node_name]
                next_node = input_graph[next_node_name]
                current_node.add_edge(next_node, 1)
    return input_graph


def dijkstra_shortest_path(graph, start, end) -> int:
    Q = PriorityQueue()
    distance = {}
    visited = {}
    previous = {k: None for k, v in graph.items()}

    for name, _ in graph.items():
        weight = float('inf')
        if name == start:
            weight = 0

        distance[name] = weight
        Q.put((weight, name))

    while not Q.empty():
        distance_to_current, current = Q.get()
        visited[current] = True

        for edge, child in graph[current].edges:

            if child.name in visited:
                continue

            distance_to_child = edge + distance_to_current

            if distance_to_child < distance[child.name]:
                distance[child.name] = distance_to_child
                previous[child.name] = current
                Q.put((distance_to_child, child.name))

    return distance[end]


end = name_node(END[X], END[Y])
shortest_path_so_far = float('inf')
i = 0
for start_x, start_y in possible_starting_locations:
    start = name_node(start_x, start_y)
    new_graph = copy_graph()
    shortest_path = dijkstra_shortest_path(new_graph, start, end)
    print(f'{i} -- starting from {start_x}, {start_y}: {shortest_path_so_far}')
    i += 1
    if shortest_path < shortest_path_so_far:
        shortest_path_so_far = shortest_path
print(shortest_path_so_far)
