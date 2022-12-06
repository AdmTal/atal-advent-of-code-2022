from collections import OrderedDict

input_items = open('./input.txt').read().split('\n')


def find_start_of_packet_marker(sequence, expected_len=14):
    buffer = OrderedDict()
    for idx, char in enumerate(sequence):

        # If a duplicate will be inserted, remove everything before it's original
        if char in buffer:
            original = buffer[char]
            keys_to_delete = [key for key, value in buffer.items() if value <= original]
            for key in keys_to_delete:
                del buffer[key]

        # Insert Char - it cannot be a duplicate at this point
        buffer[char] = idx

        # If the buffer is full, the answer has been found
        if len(buffer) == expected_len:
            return idx + 1


for line in input_items:
    answer = find_start_of_packet_marker(line)
    print(answer, line[answer - 4:answer])
