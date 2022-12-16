import re
from collections import defaultdict

SEARCH_MAX = 20
input_items = open('./example-input.txt').read().split('\n')
# SEARCH_MAX = 4_000_000
# input_items = open('./input.txt').read().split('\n')


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


def generate_all_non_beacon_or_sensor_coords_within_manhattan_distance(sx, sy, max_manhattan_distance, target_y):
    coords = []
    to_visit = [(sx, sy)]
    visited = defaultdict(lambda: defaultdict(bool))
    while to_visit:
        x, y = to_visit.pop(0)
        coords.append((x, y))
        visited[x][y] = True
        for next_x in range(sx - manhattan_dist, sx + manhattan_dist + 1):
            next_y = target_y
            next_manhattan_dist = manhattan_distance(sx, sy, next_x, next_y)
            next_is_beacon = beacons[next_x][next_y]
            if not visited[next_x][next_y] and not next_is_beacon and next_manhattan_dist <= max_manhattan_distance:
                to_visit.append((next_x, next_y))

    return coords


print('starting 1')

# We can observe each sensor to get a list of spaces that CANNOT be beacons
for idx, xxx in enumerate(sensor_beacon_pairs, start=1):
    s_coord, b_coord = xxx
    sx, sy = s_coord
    bx, by = b_coord
    print(f'{idx} / {len(sensor_beacon_pairs)}')
    manhattan_dist = manhattan_distance(sx, sy, bx, by)
    for _y in range(sy - manhattan_dist, sy + manhattan_dist + 1):
        coords = generate_all_non_beacon_or_sensor_coords_within_manhattan_distance(sx, sy, manhattan_dist, _y)
        for x, y in coords:
            coords_that_are_totally_not_beacons_dude[y][x] = True

print('starting 2')

for x in range(1, SEARCH_MAX + 1):
    for y in range(1, SEARCH_MAX + 1):
        if not coords_that_are_totally_not_beacons_dude[y][x]:
            answer = (x * 4_000_000) + y
            print(answer)
            exit()
