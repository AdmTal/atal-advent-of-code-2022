import re
from collections import defaultdict

# input_items = open('./example-input.txt').read().split('\n')
input_items = open('./input.txt').read().split('\n')

input_re = re.compile('Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)')
sensor_beacon_pairs = []
sensors = defaultdict(lambda: defaultdict(bool))
beacons = defaultdict(lambda: defaultdict(bool))
coords_that_are_totally_not_beacons_dude = defaultdict(lambda: defaultdict(bool))
for line in input_items:
    sx, sy, bx, by = input_re.match(line).groups()
    sensor_beacon_pairs.append(((int(sx), int(sy)), (int(bx), int(by))))
    sensors[sx][sy] = True
    beacons[bx][by] = True


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


POSSIBLE_DIRECTIONS = [(1, 0), (-1, 0)]

TARGET_Y = 2_000_000


def generate_all_coords_within_manhattan_distance(sx, sy, max_manhattan_distance):
    coords = []
    to_visit = [(sx, sy)]
    visited = defaultdict(lambda: defaultdict(bool))
    while to_visit:
        x, y = to_visit.pop(0)
        coords.append((x, TARGET_Y))
        visited[x][y] = True
        for dx, dy in POSSIBLE_DIRECTIONS:
            next_x, next_y = x + dx, y + dy
            next_y = TARGET_Y
            next_manhattan_dist = manhattan_distance(sx, sy, next_x, next_y)
            next_is_beacon = beacons[next_x][next_y]
            if not visited[next_x][next_y] and not next_is_beacon and next_manhattan_dist <= max_manhattan_distance:
                to_visit.append((next_x, next_y))

    return coords


# We can observe each sensor to get a list of spaces that CANNOT be beacons
for s_coord, b_coord in sensor_beacon_pairs:
    sx, sy = s_coord
    bx, by = b_coord
    manhattan_dist = manhattan_distance(sx, sy, bx, by)
    coords = generate_all_coords_within_manhattan_distance(sx, sy, manhattan_dist)
    for x, y in coords:
        coords_that_are_totally_not_beacons_dude[y][x] = True

positions_that_cannot_be_a_beacon = sum(coords_that_are_totally_not_beacons_dude[TARGET_Y].values()) - 1
print(positions_that_cannot_be_a_beacon)
