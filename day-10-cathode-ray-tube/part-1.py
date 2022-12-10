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


def should_observe_signal_strength(clock_cycle):
    return (clock_cycle - 20) % 40 == 0


clock_cycle = 0
signal_strength_sum = 0
current_instruction = None
current_instruction_cycles_remaining = 0

while instructions or current_instruction:
    # CYCLE START
    clock_cycle += 1
    if not current_instruction:
        current_instruction, current_argument = instructions.pop(0)
        current_instruction_cycles_remaining = CMD_CYCLES_TO_COMPLETE[current_instruction]

    # CYCLE MIDDLE
    if should_observe_signal_strength(clock_cycle):
        signal_strength = REGISTERS[0] * clock_cycle
        signal_strength_sum += signal_strength

    # CYCLE END
    if current_instruction:
        current_instruction_cycles_remaining -= 1
        if not current_instruction_cycles_remaining:
            # Execute Function
            if current_instruction == CMD_ADDX:
                REGISTERS[0] += current_argument

            current_instruction = None

print(signal_strength_sum)
