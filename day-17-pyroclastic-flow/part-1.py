import os
import time
import sys

# WIND_DIRECTIONS = open('./example-input.txt').read().split('\n')[0]
WIND_DIRECTIONS = open('./input.txt').read().split('\n')[0]

VERBOSE = len(sys.argv) > 1

LEFT = '<'
RIGHT = '>'

NUM_ROCKS_TO_FALL = 2022
NUM_WIND_DIRECTIONS = len(WIND_DIRECTIONS)

TOWER_WIDTH = 7
ROCK_STATE_FALLING = 'FALLING'
ROCK_STATE_STOPPED = 'STOPPED'

# Simulation + Collision detection (?)
# Model the rocks as Objects in an environment
# The environment can be simulated in a simple game loop
# Every step - a rock is either added, moved by a gust of wind, move down, or LAND and become still.
# The rock is a set of coordinates - and collision detection is a math problemGiven two objects, return TRUE if they collide.
# At any given time, there is only 1 HOT object, the falling rock that is in motion.
# At each step - we have to compare it against a growing list of objects, at MAX, running the CD alg 2022 times ?
# The walls don't need to be modeled - they can be hard coded X coords.
# The space does not need to be modeled - only a list of rocks, their positions, and their states (falling or landed)
# The game loop keeps track of the basics, if a new rock should be added, and if the loop needs to stop
# The HEIGHT of the tower is simply the max Y Coord across all of the ROCKS.

# Shape FIRST POINT, and then the rest are in relation to the first
# The first point should be the LEFT,BOTTOM - and it should have an offset

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


def print_tower(sleep=.05, message=''):
    if not VERBOSE:
        return
    os.system('clear')

    HEIGHT = height_of_tower()
    tower_grid = [['.' for col in range(TOWER_WIDTH)] for row in range(HEIGHT)]

    for rock in ROCKS_IN_EXISTENCE:
        for x, y in rock.particles:
            tower_grid[y - 1][x - 1] = '@' if rock.state == ROCK_STATE_FALLING else '#'

    print('-' * (TOWER_WIDTH + 2) + f' {message}')
    for row in reversed(tower_grid):
        print('|' + ''.join(row) + '|')
    time.sleep(sleep)


num_rock_formations = len(ROCK_FORMATIONS)
current_falling_rock = None
game_step = 0
num_stopped_rocks = 0
# Game Loop
while num_stopped_rocks < NUM_ROCKS_TO_FALL:

    wind_dir = WIND_DIRECTIONS[game_step % NUM_WIND_DIRECTIONS]
    game_step += 1

    # If a rock is not falling - create one
    if not current_falling_rock:
        num_rocks = len(ROCKS_IN_EXISTENCE)
        next_formation_index = num_rocks % num_rock_formations
        shape_name, shape, offsets = ROCK_FORMATIONS[next_formation_index]
        woofp, hoofp = offsets
        LEFT_OFFSET = 3  # by rule, rocks start 2 positions away from wall
        BOTTOM_OFFSET = 4
        current_falling_rock = Rock(
            f'{shape_name}_{num_rocks}',
            shape,
            hoofp,
            woofp,
            left_start=LEFT_OFFSET,
            bottom_start=height_of_tower() + BOTTOM_OFFSET
        )
        ROCKS_IN_EXISTENCE.append(current_falling_rock)
        print_tower(message='new')

    # Try to blow left or right -- result does not matter
    current_falling_rock.try_to_move(-1 if wind_dir == LEFT else 1, 0)
    print_tower()

    # Gravity will attempt to pull the rock 1 step DOWN
    gravity_wins = current_falling_rock.try_to_move(0, -1)
    if gravity_wins:
        print_tower()

    # If Gravity looses - the rock will have stopped
    if not gravity_wins:
        current_falling_rock.stop()
        current_falling_rock = None
        num_stopped_rocks += 1
        print_tower()
        print(f'num stopped = {num_stopped_rocks}')


print_tower()
print(f'Num Rocks = {len(ROCKS_IN_EXISTENCE)}; Final Height = {height_of_tower()}')
