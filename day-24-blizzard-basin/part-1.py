import os
from time import sleep
from collections import defaultdict
from queue import PriorityQueue

input_items = open('./medium-example.txt').read().split('\n')
# input_items = open('./example-input.txt').read().split('\n')
# input_items = open('./input.txt').read().split('\n')
# blizzard_cycle_length=3171

# The answer is fewest num MIN - not steps
# So ... penalty for WAITING

# Figure out if the blizzards cycle, is there a MIN where all B return to their starting locations?
# That is an important number - if it exists.  I could see it maybe not existing, but that is not likely

# In a brute force - you could curtail your paths by never stepping back to a "starting" position.
# That would mean - you stand in the same place, at the same point in the blizzard cycle (which requires memory)
# But DFS would never finish if cycles can exist - an a true cycle can only be detected in that way.
# Memory would be (LOCATION,BLIZZ_INDEX)

# The task here is to convert this problem into a DIrect Graph


HEIGHT = len(input_items) - 2
WIDTH = len(input_items[0]) - 2

BLIZ_UP = '^'
BLIZ_DOWN = 'v'
BLIZ_LEFT = '<'
BLIZ_RIGHT = '>'


class Blizz(object):
    def __init__(self, dir, row, col):
        self._dir = dir
        self._row = row
        self._col = col
        self._start_row = row
        self._start_col = col

    @property
    def location(self):
        return self._row, self._col

    @property
    def direction(self):
        return self._dir

    def is_back_at_step_1(self):
        return self._row == self._start_row and self._col == self._start_col

    def move(self, unit=1):
        if self._dir == BLIZ_UP:
            drow, dcol = (-unit, 0)
        elif self._dir == BLIZ_DOWN:
            drow, dcol = (unit, 0)
        elif self._dir == BLIZ_LEFT:
            drow, dcol = (0, -unit)
        else:
            drow, dcol = (0, unit)

        self._row = (self._row + drow) % (HEIGHT + 1)
        self._col = (self._col + dcol) % (WIDTH + 1)


# Parse Input - make the Bliz Objects
blizzards = []
for row in range(1, HEIGHT + 1):
    for col in range(1, WIDTH + 1):
        item = input_items[row][col]
        if item in (BLIZ_UP, BLIZ_DOWN, BLIZ_LEFT, BLIZ_RIGHT):
            blizzards.append(Blizz(item, row, col))


def _generate_blizz_lookup(blizzes):
    bliz_lookup = defaultdict(lambda: defaultdict(list))
    for bliz in blizzes:
        row, col = bliz.location
        bliz_lookup[row][col].append(bliz.direction)

    bliz_grid_lookup = defaultdict(lambda: defaultdict(list))
    for row in bliz_lookup.keys():
        for col in bliz_lookup[row].keys():
            blizz_at_this_location = bliz_lookup[row][col]
            bliz_grid_lookup[row][col] = blizz_at_this_location[0] if len(blizz_at_this_location) == 1 else str(
                len(blizz_at_this_location))

    return bliz_grid_lookup


def print_grid(blizzards):
    grid = [['' for col in range(WIDTH + 2)] for row in range(HEIGHT + 2)]

    bliz_lookup = _generate_blizz_lookup(blizzards)

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if row == 0 or col == 0 or row == HEIGHT + 1 or col == WIDTH + 1:
                grid[row][col] = '#'

            elif bliz_lookup[row][col]:
                grid[row][col] = bliz_lookup[row][col]
            else:
                grid[row][col] = '.'

    for row in grid:
        print(''.join(row))


# Figure out how many steps it takes the Blizzards to repeat themselves
blizdex_oracle = defaultdict(lambda: defaultdict(lambda: defaultdict(bool)))
blizzard_cycle_length = 0
while True:
    for bliz in blizzards:
        row, col = bliz.location
        blizdex_oracle[blizzard_cycle_length][row][col] = True

    for bliz in blizzards:
        bliz.move()
    blizzard_cycle_length += 1
    # os.system('clear')
    # print_grid(blizzards)
    # sleep(.1)
    num_back_at_1 = 0
    for bliz in blizzards:
        if bliz.is_back_at_step_1():
            num_back_at_1 += 1

    if num_back_at_1 == len(blizzards):
        break

print(f'Blizzard Cycle Length is {blizzard_cycle_length}')


# Now ... Use the cycle length to build a crazy large directed graph :)

def name_node(blizdex, row, col):
    return f'{blizdex}:({row},{col})'


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


START_ROW = 0
START_COL = 1
END_ROW = HEIGHT + 1
END_COL = WIDTH

print(f'Building Graph Nodes: {(blizzard_cycle_length - 1) * HEIGHT * WIDTH}')
blizzard_cycle_length -= 1
input_graph = {}
for blizdex in range(blizzard_cycle_length):

    # We need to inject START, STOP -- for all BLIZDEX
    s = name_node(blizdex, START_ROW, START_COL)
    input_graph[s] = Node(s)
    e = name_node(blizdex, END_ROW, END_COL)
    input_graph[e] = Node(e)

    for row in range(1, HEIGHT + 1):
        for col in range(1, WIDTH + 1):
            node_name = name_node(blizdex, row, col)
            input_graph[node_name] = Node(node_name)

print(f'\tIt was actually {len(input_graph)} nodes')

print(f'Building Graph Edges: (?) size unkown')
edges_added = 0
POSSIBLE_DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

for blizdex in range(blizzard_cycle_length):
    next_blizdex = (blizdex + 1) % blizzard_cycle_length
    for row in range(HEIGHT + 1):
        for col in range(WIDTH + 1):
            # The current node
            node_name = name_node(blizdex, row, col)

            if node_name not in input_graph:
                continue

            # Add SELF EDGE to represent waiting (links to next BLIZDEX)
            if node_name in input_graph:
                current_node = input_graph[node_name]
                next_node_name = name_node(next_blizdex, row, col)
                if next_node_name in input_graph:
                    next_node = input_graph[next_node_name]
                    current_node.add_edge(next_node, 1)
                    edges_added += 1

            for drow, dcol in POSSIBLE_DIRECTIONS:
                next_row = row + drow
                next_col = col + dcol

                # Skip any COORDS that are out of bounds
                next_node_name = name_node(next_blizdex, next_row, next_col)
                if next_node_name not in input_graph:
                    continue

                # Skip Coords that have Blizzards
                if blizdex_oracle[next_blizdex][next_row][next_col]:
                    continue

                current_node = input_graph[node_name]
                next_node = input_graph[next_node_name]
                current_node.add_edge(next_node, 1)
                edges_added += 1

print(f'\tit was {edges_added} edges')


def dijkstra_shortest_path(graph, start) -> int:
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

    return distance, previous


start_suffix = f'({START_ROW},{START_COL})'
end_suffix = f'({END_ROW},{END_COL})'


def print_graph(nodes):
    """Helper func to log graph in DOT"""
    print("""digraph {
    """)
    for name, node in nodes.items():
        node_is_start = start_suffix in node.name
        node_is_end = end_suffix in node.name
        color = ''
        if node_is_start:
            color = '[color="green"]'
        if node_is_end:
            color = '[color="red"]'
        print(f'    "{node.name}"{color};')
        for weight, child in node.edges:
            print(f'    "{node.name}" -> "{child.name}";')
    print('}')


start_nodes = []
end_nodes = []
for name in input_graph.keys():
    if start_suffix in name:
        start_nodes.append(name)

    if end_suffix in name:
        end_nodes.append(name)

# print_graph(input_graph)

print(f'Start Nodes Count: {len(start_nodes)}')
print(f'End Nodes Count = {len(end_nodes)}')

shortest_path = float('inf')
_path = None
for start_node in start_nodes:
    distances, previous = dijkstra_shortest_path(input_graph, start_node)

    for end_node in end_nodes:
        curr = distances[end_node]
        if curr < shortest_path:
            shortest_path = curr
            print(f'New Shortest Path from {start_node} to {end_node} is {distances[end_node]}')
            # Build the shortest path by following the previous nodes
            path = []
            current_node = end_node
            while current_node is not None:
                path.append(current_node)
                current_node = previous[current_node]

            # Reverse the path to get the correct order
            _path = list(reversed(path))

print(f'Final Path: {_path}')
