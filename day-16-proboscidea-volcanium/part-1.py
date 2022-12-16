import re
from collections import defaultdict
from functools import cache

input_lines = open('./example-input.txt').read().split('\n')


# input_lines = open('./input.txt').read().split('\n')


class Node:
    def __init__(self, name, flow_rate):
        self._name = name
        self._edges = []
        self._flow_rate = flow_rate

    @property
    def name(self):
        return self._name

    @property
    def flow_rate(self):
        return self._flow_rate

    @property
    def edges(self):
        return self._edges

    def add_edge(self, node, weight):
        self._edges.append((weight, node))


graph = {}
edges = defaultdict(list)

input_re = re.compile('Valve ([A-Z]+) has flow rate=(\d+); tunnel(s*) lead(s*) to valve(s*) ([A-Z, ]+)')
for row in input_lines:
    valve_name, flow_rate, _, _, _, destinations = input_re.match(row).groups()
    flow_rate = int(flow_rate)
    destinations = [i.strip() for i in destinations.split(',')]
    graph[valve_name] = Node(valve_name, flow_rate)
    for dest in destinations:
        edges[valve_name].append(dest)

for parent, children in edges.items():
    for child in children:
        graph[parent].add_edge(graph[child], 1)


def print_graph(nodes):
    """Helper func to log graph in DOT"""
    print("""digraph {
    """)
    for name, node in nodes.items():
        print(f'    {node.name};')
        for weight, child in node.edges:
            print(f'    {node.name} -> {child.name} [label="{weight} {node.flow_rate}"];')
    print('}')


###

def to_str(open_valves):
    return ','.join([key for key, value in open_valves.items() if value])


@cache
def max_pressure_release(current_position, open_valves_str, minutes_remaining):
    spacer = ' ' * (30 - minutes_remaining)

    if minutes_remaining <= 1:
        return 0

    open_valves = {k: True for k in open_valves_str.split(',')}

    options = []

    new_pressure_released = 0

    if current_position not in options:
        # If you OPEN
        open_valves[current_position] = True
        options.append([to_str(open_valves), minutes_remaining - 1])
        new_pressure_released += graph[current_position].flow_rate * minutes_remaining - 1

    # if you SKIP
    open_valves[current_position] = False
    options.append([to_str(open_valves), minutes_remaining - 1])

    max_result = float('-inf')
    for next_open_valves_str, next_time_remaining in options:
        for weight, child in graph[current_position].edges:
            max_result = max(
                max_result,
                max_pressure_release(child.name, next_open_valves_str, next_time_remaining - 1)
            )

    print(f'{spacer} min={minutes_remaining} RES={new_pressure_released + max_result}')
    return new_pressure_released + max_result


print(max_pressure_release('AA', '', 2))
