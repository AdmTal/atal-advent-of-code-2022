from PIL import Image, ImageDraw
import re
from collections import defaultdict

# input_items = open('./example-input.txt').read().split('\n')
# SEARCH_MAX = 4_000_000
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

pixel_size = 1

sensor_beacon_pairs = []
for line in input_items:
    sx, sy, bx, by = input_re.match(line).groups()
    sensor_beacon_pairs.append(
        (
            (
                (int(sx) + XMIN) * pixel_size,
                (int(sy) + YMIN) * pixel_size,
            ),
            (
                (int(bx) + XMIN) * pixel_size,
                (int(by) + YMIN) * pixel_size,
            )
        )
    )

# Create a new image with a blue background
print(WIDTH, HEIGHT)
image = Image.new('RGB', (WIDTH * pixel_size, HEIGHT * pixel_size), (0, 0, 240))
draw = ImageDraw.Draw(image)



def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


for s_coord, b_coord in sensor_beacon_pairs:
    sx, sy = s_coord
    bx, by = b_coord
    manhattan_dist = manhattan_distance(sx, sy, bx, by)
    draw.polygon([
        (sx, sy - manhattan_dist),
        (sx - manhattan_dist, sy),
        (sx, sy + manhattan_dist),
        (sx + manhattan_dist, sy),
    ], outline=(255, 255, 255))
    print([
        (sx, sy - manhattan_dist),
        (sx - manhattan_dist, sy),
        (sx, sy + manhattan_dist),
        (sx + manhattan_dist, sy),
    ])

# Save the image as a PNG file
image.save('polygon.png')
