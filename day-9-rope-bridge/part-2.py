from collections import defaultdict

head_moves = [i.split(' ') for i in open('./input.txt').read().split('\n')]
head_moves = [[i[0], int(i[1])] for i in head_moves]

coords_tail_visited = defaultdict(dict)

NUM_KNOTS = 10
KNOTS = [[0, 0] for i in range(NUM_KNOTS)]

HEAD = 0
TAIL = NUM_KNOTS - 1
X = 0
Y = 1

# First location is considered visited
coords_tail_visited[KNOTS[TAIL][X]][KNOTS[TAIL][Y]] = True


def coord_delta(direction):
    if direction == 'R':
        return 1, 0
    elif direction == 'L':
        return -1, 0
    elif direction == 'U':
        return 0, 1
    return 0, -1  # D


for direction, steps in head_moves:
    head_delta_x, head_delta_y = coord_delta(direction)

    for step in range(steps):
        KNOTS[HEAD][X] += head_delta_x
        KNOTS[HEAD][Y] += head_delta_y

        # Iterate rest of knots in rope
        for curr in range(1, NUM_KNOTS):

            # If they overlap - skip
            if KNOTS[curr - 1][X] == KNOTS[curr][X] and KNOTS[curr - 1][Y] == KNOTS[curr][Y]:
                continue

            if abs(KNOTS[curr - 1][X] - KNOTS[curr][X]) < 2 and abs(KNOTS[curr - 1][Y] - KNOTS[curr][Y]) < 2:
                continue

            if KNOTS[curr - 1][X] == KNOTS[curr][X] and abs(KNOTS[curr - 1][Y] - KNOTS[curr][Y]) == 2 or \
                    KNOTS[curr - 1][Y] == KNOTS[curr][Y] and abs(KNOTS[curr - 1][X] - KNOTS[curr][X]) == 2:
                if KNOTS[curr - 1][X] == KNOTS[curr][X] and abs(KNOTS[curr - 1][Y] - KNOTS[curr][Y]) == 2:
                    # move 1 step UP or DOWN
                    if KNOTS[curr - 1][Y] > KNOTS[curr][Y]:
                        KNOTS[curr][Y] += 1
                    else:
                        KNOTS[curr][Y] -= 1
                elif KNOTS[curr - 1][Y] == KNOTS[curr][Y] and abs(KNOTS[curr - 1][X] - KNOTS[curr][X]) == 2:
                    # move 1 step LEFT or RIGHT
                    if KNOTS[curr - 1][X] > KNOTS[curr][X]:
                        KNOTS[curr][X] += 1
                    else:
                        KNOTS[curr][X] -= 1
                if curr == TAIL:
                    coords_tail_visited[KNOTS[curr][X]][KNOTS[curr][Y]] = True
                continue

            # Move Diagonally 1 step close to H
            if KNOTS[curr - 1][X] > KNOTS[curr][X]:
                tail_delta_x, tail_delta_y = coord_delta('R')
            else:
                tail_delta_x, tail_delta_y = coord_delta('L')

            KNOTS[curr][X] += tail_delta_x
            KNOTS[curr][Y] += tail_delta_y

            if KNOTS[curr - 1][Y] > KNOTS[curr][Y]:
                tail_delta_x, tail_delta_y = coord_delta('U')
            else:
                tail_delta_x, tail_delta_y = coord_delta('D')

            KNOTS[curr][X] += tail_delta_x
            KNOTS[curr][Y] += tail_delta_y

            if curr == TAIL:
                coords_tail_visited[KNOTS[curr][X]][KNOTS[curr][Y]] = True

tail_steps = 0
for x_coord, y_coords in coords_tail_visited.items():
    for y_coord in y_coords.keys():
        tail_steps += 1

print(tail_steps)
