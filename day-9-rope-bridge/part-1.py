from collections import defaultdict

head_moves = [
    i.split(' ') for i in open('./input.txt').read().split('\n')
]
head_moves = [[i[0], int(i[1])] for i in head_moves]

coords_tail_visited = defaultdict(dict)

head_x = 0
head_y = 0
tail_x = 0
tail_y = 0

# First location is considered visited
coords_tail_visited[tail_x][tail_y] = True


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
        head_x += head_delta_x
        head_y += head_delta_y

        # If they overlap - skip
        if head_x == tail_x and head_y == tail_y:
            continue

        if abs(head_x - tail_x) < 2 and abs(head_y - tail_y) < 2:
            continue

        if head_x == tail_x and abs(head_y - tail_y) == 2 or head_y == tail_y and abs(head_x - tail_x) == 2:
            if head_x == tail_x and abs(head_y - tail_y) == 2:
                # move 1 step UP or DOWN
                if head_y > tail_y:
                    tail_y += 1
                else:
                    tail_y -= 1
            elif head_y == tail_y and abs(head_x - tail_x) == 2:
                # move 1 step LEFT or RIGHT
                if head_x > tail_x:
                    tail_x += 1
                else:
                    tail_x -= 1
            coords_tail_visited[tail_x][tail_y] = True
            continue

        # Move Diagonally 1 step close to H
        if head_x > tail_x:
            tail_delta_x, tail_delta_y = coord_delta('R')
        else:
            tail_delta_x, tail_delta_y = coord_delta('L')

        tail_x += tail_delta_x
        tail_y += tail_delta_y

        if head_y > tail_y:
            tail_delta_x, tail_delta_y = coord_delta('U')
        else:
            tail_delta_x, tail_delta_y = coord_delta('D')

        tail_x += tail_delta_x
        tail_y += tail_delta_y

        coords_tail_visited[tail_x][tail_y] = True

tail_steps = 0
for x_coord, y_coords in coords_tail_visited.items():
    for y_coord in y_coords.keys():
        tail_steps += 1

print(tail_steps)
