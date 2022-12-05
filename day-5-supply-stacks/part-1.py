input_lines = open('./input.txt').read().split('\n')

SCAN_FOR_STACK_IDS = 'SCAN_FOR_STACK_IDS'
SCAN_FOR_MOVES = 'SCAN_FOR_MOVES'

mode = SCAN_FOR_STACK_IDS
stack_lines = []
moves = []
num_stacks = 0
for line in input_lines:

    if not line:
        continue

    tokens = line.split(' ')
    filtered_tokens = list(filter(lambda x: x, tokens))

    if mode == SCAN_FOR_STACK_IDS:
        if not all([i.isdigit() for i in filtered_tokens]):
            stack_lines.insert(0, tokens)
        else:
            num_stacks = max((map(int, filtered_tokens)))
            mode = SCAN_FOR_MOVES
        continue

    if mode == SCAN_FOR_MOVES:
        move_num = tokens[1]
        move_from = tokens[3]
        move_to = tokens[5]
        moves.append(list(map(int, [move_num, move_from, move_to])))


# Clean the lists ... replace 4 spaces with blank token
def standardize_line(line):
    standard_line = []
    curr = 0
    line_length = len(line)
    while curr < line_length:
        token = line[curr]
        if token:
            standard_line.append(token[1])
            curr += 1
        else:
            standard_line.append('')
            curr += 4

    return standard_line


# Build the stacks
stacks = [[] for i in range(num_stacks + 1)]
for line in stack_lines:
    for stack_id, item in enumerate(standardize_line(line), start=1):
        if item:
            stacks[stack_id].append(item)

# Do the moves
for move_num, source_id, dest_id in moves:
    moved = 0
    while moved < move_num:
        item = stacks[source_id].pop()
        stacks[dest_id].append(item)
        moved += 1

top_of_stacks = ''.join([i[-1] for i in stacks if i])
print(top_of_stacks)
