from collections import defaultdict
import math

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
        self._divisible_check = self._parse_test(test)
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
        return int(test.split('Test: divisible by ')[1])

    @staticmethod
    def _get_monkey_for_handler(handler):
        return int(handler.split(' throw to monkey ')[1])

    def get_worry_level_after_inspection(self, worry_level):
        return self._operation(old=worry_level)

    def get_monkey_to_throw_to(self, worry_level):
        # Return TRUE of given number is divisible by

        _ = math.gcd(self._divisible_check, worry_level)
        if _ == min(self._divisible_check, worry_level):
            return self._monkey_when_true
        return self._monkey_when_false

    @property
    def items(self):
        return self._items

    @property
    def divisible_check(self):
        return self._divisible_check


monkeys = [Monkey(instruction_group) for instruction_group in instruction_groups]

NUM_MONKEYS = len(monkeys)
NUM_ROUNDS = 10_000

monkey_num_inspections = defaultdict(int)

# I'm not this smart, I found help from the subreddit, specifically this link
# https://nickymeuleman.netlify.app/garden/aoc2022-day11#part-2
required_divisible_checks = [monkey.divisible_check for monkey in monkeys]
_MATH_MAGIC_I_STOLE_FROM_NICKY_MEULEMAN = required_divisible_checks[0]
for required_divisible_check in required_divisible_checks[1:]:
    _MATH_MAGIC_I_STOLE_FROM_NICKY_MEULEMAN *= required_divisible_check

for round in range(1, NUM_ROUNDS + 1):

    for monkey_idx in range(NUM_MONKEYS):
        monkey = monkeys[monkey_idx]

        while monkey.items:
            # Monkey Inspect Item (which makes me worry)
            item_worry_level = monkey.get_worry_level_after_inspection(monkey.items.pop(0))
            monkey_num_inspections[monkey_idx] += 1

            # I Reduce Worry (because item was not broken)
            item_worry_level = item_worry_level % _MATH_MAGIC_I_STOLE_FROM_NICKY_MEULEMAN

            # Monkey considers my feelings
            dest_monkey_idx = monkey.get_monkey_to_throw_to(item_worry_level)

            # Monkey Throw Item
            monkeys[dest_monkey_idx].items.append(item_worry_level)

a, b = sorted(monkey_num_inspections.values(), reverse=True)[:2]
monkey_business = a * b
print(monkey_business)
