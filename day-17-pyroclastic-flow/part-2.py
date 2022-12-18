import sys

WIND_DIRECTIONS = open('./example-input.txt').read().split('\n')[0]  # 40
# WIND_DIRECTIONS = open('./input.txt').read().split('\n')[0]  # 10091

VERBOSE = len(sys.argv) > 1

LEFT = '<'
RIGHT = '>'

# NUM_ROCKS_TO_FALL = 1_000_000_000_000
NUM_ROCKS_TO_FALL = 100000
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
    def __init__(self, name, shape, hoofp, woofp, left_start, bottom_start, windex):
        self._name = name
        self._shape = shape
        self._hoofp = hoofp
        self._woofp = woofp
        # A rock is basically a list of Particles (pixel coords) in the environment
        self._particles = self._calculate_particles_from_starting_position(left_start, bottom_start)
        self._state = ROCK_STATE_FALLING
        self._windex = windex
        self._move_history = []

    def _calculate_particles_from_starting_position(self, left_start, bottom_start):
        sx, sy = left_start + self._woofp, bottom_start + self._hoofp

        particles = []

        for dx, dy in self._shape:
            particles.append((sx + dx, sy + dy))

        return particles

    def __eq__(self, other):
        return self._name == other._name

    def check_for_soul_mate(self, other_rock):
        return self._windex == other_rock._windex and self._move_history == other_rock._move_history

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
        self._height_when_this_landed = height_of_tower()
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

        self._move_history.append((dx, dy))
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
# Game Loop

from collections import defaultdict

wind_resets_by_rock = defaultdict(int)

landed_heights = [None, ]

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
            bottom_start=height_of_tower() + BOTTOM_OFFSET,
            windex=windex,
        )
        ROCKS_IN_EXISTENCE.append(current_falling_rock)

    # Try to blow left or right -- result does not matter
    current_falling_rock.try_to_move(-1 if wind_dir == LEFT else 1, 0)

    # If Gravity fails to move the rock, the rock will have stopped
    if not current_falling_rock.try_to_move(0, -1):
        current_falling_rock.stop()
        landed_heights.append(height_of_tower())
        current_num = int(current_falling_rock._name.split('_')[1])
        print(f'{current_num} -- {height_of_tower()}')

        for other_rock in ROCKS_IN_EXISTENCE:

            if current_falling_rock == other_rock:
                continue

            if current_falling_rock.check_for_soul_mate(other_rock):
                other_num = int(other_rock._name.split('_')[1])
                current_num = int(current_falling_rock._name.split('_')[1])
                print(f'{other_num} and {current_num} are soul mates')
                print(f'So really, the a Cycle is from {other_num} to {current_num - 1}')
                diff = landed_heights[current_num - 1] - landed_heights[other_num]
                cycle_length = current_num - 1 - other_num
                print(f'that means the height grows {diff} every {cycle_length} rocks')
                a = 1_000_000_000_000
                complete_cycles = int(a / cycle_length)
                remainder_cycles = a % cycle_length
                print(f'The final answer is {complete_cycles * diff} + whatever the height is after the next {remainder_cycles} rocks')
                print(f'There can be {complete_cycles} cycles in {a}')
                expected = 1514285714288
                print(f'Expected = {1514285714288}')
                actual = (complete_cycles * diff) + sum(landed_heights[other_num:other_num + remainder_cycles + 1])
                print(f'Actual   = {actual}')
                print(f'diff     = {actual - expected}')
                exit()

        current_falling_rock = None
        num_stopped_rocks += 1

print(height_of_tower())
