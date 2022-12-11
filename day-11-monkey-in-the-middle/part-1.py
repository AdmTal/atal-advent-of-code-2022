from pprint import pprint
import math
from collections import defaultdict

# input_lines = open('./example-input.txt').read().split('\n')
input_lines = open('./input.txt').read().split('\n')


def array_chunks(lst, size):
    """This func was written ny GPT-3"""
    result = []
    for i in range(0, len(lst), size):
        result.append(lst[i:i + size])
        if not result[-1][-1]:
            result[-1].pop(-1)  # Clear out blank lines
    return result


instruction_groups = array_chunks(input_lines, 7)


class Monkey(object):
    def __init__(self, instruction_group):
        _, \
            starting_items, \
            operation, \
            test, \
            handle_true, \
            handle_false = instruction_group

        self._items = self._parse_starting_items(starting_items)
        self._operation = self._parse_operation(operation)
        self._test = self._parse_test(test)
        self._monkey_when_true = self._get_monkey_for_handler(handle_true)
        self._monkey_when_false = self._get_monkey_for_handler(handle_false)

    @staticmethod
    def _parse_starting_items(starting_items):
        return [int(i) for i in starting_items.split('  Starting items: ')[1].split(',')]

    @staticmethod
    def _parse_operation(operation):
        operation = operation.split('Operation: new = ')[1]
        return lambda old: eval(f'{operation}'.replace('old', str(old)))

    @staticmethod
    def _parse_test(test):
        arg = int(test.split('Test: divisible by ')[1])
        return lambda x: x % arg == 0

    @staticmethod
    def _get_monkey_for_handler(handler):
        return int(handler.split(' throw to monkey ')[1])

    def get_worry_level_after_inspection(self, worry_level):
        return self._operation(old=worry_level)

    def get_monkey_to_throw_to(self, worry_level):
        if self._test(worry_level):
            return self._monkey_when_true
        return self._monkey_when_false

    @property
    def items(self):
        return self._items


monkeys = [Monkey(instruction_group) for instruction_group in instruction_groups]

NUM_MONKEYS = len(monkeys)
NUM_ROUNDS = 20

monkey_num_inspections = defaultdict(int)

for round in range(1, NUM_ROUNDS + 1):
    for monkey_idx in range(NUM_MONKEYS):
        monkey = monkeys[monkey_idx]

        while monkey.items:
            # Monkey Inspect Item (which makes me worry)
            item_worry_level = monkey.get_worry_level_after_inspection(monkey.items.pop(0))
            monkey_num_inspections[monkey_idx] += 1

            # I Reduce Worry (because item was not broken)
            item_worry_level = math.floor(float(item_worry_level) / 3)

            # Monkey considers my feelings
            dest_monkey_idx = monkey.get_monkey_to_throw_to(item_worry_level)

            # Monkey Throw Item
            monkeys[dest_monkey_idx].items.append(item_worry_level)

a, b = sorted(monkey_num_inspections.values(), reverse=True)[:2]
monkey_business = a * b
print(monkey_business)
