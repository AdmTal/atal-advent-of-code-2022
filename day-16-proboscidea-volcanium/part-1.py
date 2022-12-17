import re
from collections import defaultdict
from functools import cache
import time

# input_lines = open('./example-input.txt').read().split('\n')
input_lines = open('./input.txt').read().split('\n')

MINUTES_TO_SAVE_ELEPHANTS = 30


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
        print(f'    "{node.name} ({node.flow_rate})";')
        for weight, child in node.edges:
            print(f'    "{node.name} ({node.flow_rate})" -> "{child.name} ({child.flow_rate})";')
    print('}')


def to_str(open_valves):
    return ','.join(sorted([key for key in open_valves.keys() if key]))


@cache
def max_pressure_release(current_position, open_valves_str, minutes_remaining):
    # When time is up, the max pressure that can further be released is ZERO
    if minutes_remaining <= 0:
        return 0

    open_valves = {k: True for k in open_valves_str.split(',') if k}

    new_pressure_released = 0

    # Let's figure out what our options are for a next move
    # We always have the option to NOT open the Valve
    options = [[
        open_valves_str,
        minutes_remaining,
        0
    ]]

    # If the current Valve is CLOSED - we have the option to open it -- but we should skip if flow_rate is ZERO
    if current_position not in open_valves and graph[current_position].flow_rate:
        # Append an option for opening the valve
        open_valves[current_position] = True
        minutes_remaining_after_this_move = minutes_remaining - 1
        pressure_released_for_this_valve = graph[current_position].flow_rate * minutes_remaining_after_this_move
        options.append([
            to_str(open_valves),
            minutes_remaining_after_this_move,
            pressure_released_for_this_valve
        ])

    # Cycles are troubling - but given that the timer is counting down - they will not cause inf loops

    # We have to consider our options for all children
    max_result = float('-inf')
    for next_open_valves_str, next_time_remaining, extra_pressure in options:
        for weight, child in graph[current_position].edges:
            # Visit the Child - keep track of MAX
            max_result = max(
                max_result,
                max_pressure_release(
                    child.name,
                    next_open_valves_str,
                    next_time_remaining - 1
                ) + extra_pressure
            )

    new_pressure_released += max_result
    return new_pressure_released


start = time.time()
print(max_pressure_release('AA', '', MINUTES_TO_SAVE_ELEPHANTS))
end = time.time()
print(f'{end - start}')
