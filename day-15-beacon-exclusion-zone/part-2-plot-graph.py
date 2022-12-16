from matplotlib import pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.ops import unary_union

import re
from collections import defaultdict

# input_items = open('./example-input.txt').read().split('\n')
input_items = open('./input.txt').read().split('\n')
input_re = re.compile('Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)')
beacons = defaultdict(lambda: defaultdict(bool))
XMIN = float('inf')
YMIN = float('inf')
XMAX = float('-inf')
YMAX = float('-inf')
for line in input_items:
    sx, sy, bx, by = input_re.match(line).groups()
    XMIN = min(XMIN, int(sx), int(bx))
    YMIN = min(YMIN, int(sy), int(by))
    XMAX = max(XMAX, int(sx), int(bx))
    YMAX = max(YMAX, int(sy), int(by))

WIDTH = XMAX - XMIN
HEIGHT = YMAX - YMIN

# In order to crop - all NEGATIVES need to be positive - so we need to add MIN to all X,Y

sensor_beacon_pairs = []
for line in input_items:
    sx, sy, bx, by = input_re.match(line).groups()
    sensor_beacon_pairs.append(((int(sx), int(sy)), (int(bx), int(by))))


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


polys = []

for s_coord, b_coord in sensor_beacon_pairs:
    sx, sy = s_coord
    bx, by = b_coord
    manhattan_dist = manhattan_distance(sx, sy, bx, by)

    polys.append(
        Polygon([
            (sx, sy - manhattan_dist),
            (sx - manhattan_dist, sy),
            (sx, sy + manhattan_dist),
            (sx + manhattan_dist, sy),
            (sx, sy - manhattan_dist),
        ]))

mergedPolys = unary_union(polys)
gpd.GeoSeries([mergedPolys]).boundary.plot()
plt.grid(True)
plt.show()
