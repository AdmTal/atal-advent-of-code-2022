input_items = open('./input.txt').read().split('\n')

CMD_NOOP = 'noop'
CMD_ADDX = 'addx'

CMD_CYCLES_TO_COMPLETE = {
    CMD_NOOP: 1,
    CMD_ADDX: 2,
}

NUM_REGISTERS = 1
REGISTERS = [1] * NUM_REGISTERS

instructions = []
for input_item in input_items:

    if input_item == CMD_NOOP:
        instructions.append([CMD_NOOP, None])
        continue

    func, arg = input_item.split()
    instructions.append([func, int(arg)])


def crt_row_is_complete(clock_cycle):
    # Why did we have to subtract 20 last time ?
    return clock_cycle % 40 == 0


clock_cycle = 0
signal_strength_sum = 0
current_instruction = None
current_instruction_cycles_remaining = 0

CRT_PIXELS = []

while instructions or current_instruction:
    # CYCLE START
    clock_cycle += 1
    if not current_instruction:
        current_instruction, current_argument = instructions.pop(0)
        current_instruction_cycles_remaining = CMD_CYCLES_TO_COMPLETE[current_instruction]

    # CYCLE MIDDLE

    # draw pixel
    pixel_position = (clock_cycle - 1) % 40
    sprite_position = REGISTERS[0]
    pixel_to_draw = '.'  # DARK
    if any([
        pixel_position - 1 == sprite_position,
        pixel_position == sprite_position,
        pixel_position + 1 == sprite_position,
    ]):
        pixel_to_draw = '#'  # Light
    CRT_PIXELS.append(pixel_to_draw)

    if crt_row_is_complete(clock_cycle):
        signal_strength = REGISTERS[0] * clock_cycle
        signal_strength_sum += signal_strength
        print(''.join(CRT_PIXELS))
        CRT_PIXELS = []

    # CYCLE END
    if current_instruction:
        current_instruction_cycles_remaining -= 1
        if not current_instruction_cycles_remaining:
            # Execute Function
            if current_instruction == CMD_ADDX:
                REGISTERS[0] += current_argument

            current_instruction = None

print(signal_strength_sum)
