import os
import time
import sys

# WIND_DIRECTIONS = open('./example-input.txt').read().split('\n')[0]  # 40
WIND_DIRECTIONS = open('./input.txt').read().split('\n')[0]  # 10091

VERBOSE = len(sys.argv) > 1

LEFT = '<'
RIGHT = '>'

NUM_ROCKS_TO_FALL = 1_000_000_000_000
NUM_WIND_DIRECTIONS = len(WIND_DIRECTIONS)

# There must be a periodic pattern ...
# Every time the First Block lines up with the first Wind ... should reveal it ?

TOWER_WIDTH = 7
ROCK_STATE_FALLING = 'FALLING'
ROCK_STATE_STOPPED = 'STOPPED'

ROCK_FORMATIONS = [
    [
        'Horizontal Line',
        [(0, 0), (1, 0), (2, 0), (3, 0)],  # POINTS
        (0, 0),  # (Height Offset of First Point, Width Offset of First Point) (HOOFP, WOOFP)
    ],

    [
        'Cross',
        [(0, 0), (1, 0), (-1, 0), (0, -1), (0, 1)],
        (1, 1),
    ],

    [
        'Reverse L',
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        (0, 0),
    ],

    [
        'Vertical Line',
        [(0, 3), (0, 2), (0, 1), (0, 0)],
        (0, 0),
    ],
    [
        'Box',
        [(1, 1), (0, 0), (1, 0), (0, 1)],
        (0, 0),
    ]
]

ROCKS_IN_EXISTENCE = []


class Rock(object):
    def __init__(self, name, shape, hoofp, woofp, left_start, bottom_start):
        self._name = name
        self._shape = shape
        self._hoofp = hoofp
        self._woofp = woofp
        # A rock is basically a list of Particles (pixel coords) in the environment
        self._particles = self._calculate_particles_from_starting_position(left_start, bottom_start)
        self._state = ROCK_STATE_FALLING

    def _calculate_particles_from_starting_position(self, left_start, bottom_start):
        sx, sy = left_start + self._woofp, bottom_start + self._hoofp

        particles = []

        for dx, dy in self._shape:
            particles.append((sx + dx, sy + dy))

        return particles

    def __eq__(self, other):
        return self._name == other._name

    def __str__(self):
        particles = []
        for x, y in self._particles:
            particles.append(f'({x},{y})')

        ps = ','.join(particles)
        return f'{self._name} -> {ps}'

    @property
    def particles(self):
        return self._particles

    def max_y(self):
        return max([y for _, y in self.particles])

    def stop(self):
        self._state = ROCK_STATE_STOPPED

    @property
    def state(self):
        return self._state

    def try_to_move(self, dx, dy):
        """Attempt to relocate the rock, returns True on success else False (collision)"""
        new_particles = []
        for x, y in self._particles:
            new_particles.append((x + dx, y + dy))

        # First ... return FALSE if any of the particles overlap with a WALL or FLOOR
        for x, y in new_particles:
            if x < 1 or x > TOWER_WIDTH or y < 1:
                return False

        # Then ... return FALSE if any of the new particles MATCH any particles in the other rocks
        for rock in ROCKS_IN_EXISTENCE:
            if self == rock:
                continue
            for rx, ry in rock.particles:
                for x, y in new_particles:
                    if x == rx and y == ry:
                        return False

        self._particles = new_particles
        return True


def height_of_tower():
    if not ROCKS_IN_EXISTENCE:
        return 0

    return max([i.max_y() for i in ROCKS_IN_EXISTENCE])


num_rock_formations = len(ROCK_FORMATIONS)
current_falling_rock = None
game_step = 0
num_stopped_rocks = 0
x_marker = None
diffs = []
rock_counts = []
# Game Loop
while num_stopped_rocks < NUM_ROCKS_TO_FALL:

    # Wind Index = Windex - I'm having the time of my life here :)
    windex = game_step % NUM_WIND_DIRECTIONS
    wind_dir = WIND_DIRECTIONS[windex]
    game_step += 1

    num_rocks = len(ROCKS_IN_EXISTENCE)
    rockdex = num_rocks % num_rock_formations

    # If a rock is not falling - create one
    if not current_falling_rock:
        shape_name, shape, offsets = ROCK_FORMATIONS[rockdex]
        woofp, hoofp = offsets
        LEFT_OFFSET = 3  # by rule, rocks start 2 positions away from wall
        BOTTOM_OFFSET = 4
        rock_name = f'{shape_name}_{num_rocks + 1}'
        current_falling_rock = Rock(
            rock_name,
            shape,
            hoofp,
            woofp,
            left_start=LEFT_OFFSET,
            bottom_start=height_of_tower() + BOTTOM_OFFSET
        )
        ROCKS_IN_EXISTENCE.append(current_falling_rock)

    # Try to blow left or right -- result does not matter
    current_falling_rock.try_to_move(-1 if wind_dir == LEFT else 1, 0)

    # If Gravity fails to move the rock, the rock will have stopped
    if not current_falling_rock.try_to_move(0, -1):
        if x_marker is None:
            x_marker = current_falling_rock.particles[0][0]
            wind_marker = windex
            print(f'set x mark {x_marker}; wind_marker={wind_marker}')
            h_prev = 0
        curr_x_marker = current_falling_rock.particles[0][0]
        current_falling_rock.stop()
        current_falling_rock = None
        num_stopped_rocks += 1

        # Find the first one - then wait to find it again ....

        if x_marker is not None and x_marker == wind_marker and rockdex == 0:
            h = height_of_tower()
            h_prev_diff = h - h_prev
            rock_counts.append(len(ROCKS_IN_EXISTENCE))
            diffs.append(h_prev_diff)
            print(
                f'num_rocks={len(ROCKS_IN_EXISTENCE)}; height={h}; diff_since_last={h_prev_diff};')
            h_prev = h

            if len(diffs) <= 2:
                continue

            second_diff = diffs[1]
            latest_diff = diffs[-1]

            if second_diff == latest_diff:
                break

print(f'Pattern Detected ...')
period = diffs[1:-1]
len_period = len(period)
amount = sum(diffs[1:-1])
sum(diffs[1:-1])
print(diffs)
print(f'Tower grows {amount} every {len_period} rocks')

first_height = diffs[0]
answer = int(((NUM_ROCKS_TO_FALL-1) / len_period) * amount)
print(f'Answer is {answer}')
