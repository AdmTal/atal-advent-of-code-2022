import re

# input_items = open('./example-input.txt').read().split('\n')
input_items = open('./input.txt').read().split('\n')


number_monkey = re.compile('^([a-z]+): (\d+)$')
math_monkey = re.compile('^([a-z]+): ([a-z]+) ([-+/\\*]) ([a-z]+)$')


class Monkey(object):
    def __init__(self, name, value_or_opcode, left_name=None, right_name=None):
        self._name = name
        self._value = None
        self._opcode = None
        if value_or_opcode in ('/', '+', '-', '*'):
            self._opcode = value_or_opcode
        else:
            self._value = value_or_opcode

        self._left = None
        self._right = None

        self._left_name = left_name
        self._right_name = right_name

    def set_left_child(self, left):
        self._left = left

    def set_right_child(self, right):
        self._right = right

    def is_leaf(self):
        return not (self._left_name or self._right_name)

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def left_name(self):
        return self._left_name

    @property
    def right_name(self):
        return self._right_name

    def __str__(self):
        prefix = f'M({self._name}): '
        if self.is_leaf():
            return f'{prefix}{self._value}'
        return f'{prefix}{self._left_name} {self._opcode} {self.right_name}'

    def get_value(self):
        if self.is_leaf():
            return int(self._value)

        left_value = self.left.get_value()
        right_value = self.right.get_value()

        return eval(f'{left_value} {self._opcode} {right_value}')


MONKEY_LOOKUP = {}
ROOT = None
for line in input_items:
    if number_monkey.match(line):
        number_monkey.match(line).groups()
        name, value = number_monkey.match(line).groups()
        new_monkey = Monkey(name, value)
    else:
        name, left, operation, right = math_monkey.match(line).groups()
        new_monkey = Monkey(name, operation, left, right)

    MONKEY_LOOKUP[name] = new_monkey
    if name == 'root':
        ROOT = new_monkey

# Link monkey to children
for name, monkey in MONKEY_LOOKUP.items():
    if monkey.is_leaf():
        continue

    left_child = MONKEY_LOOKUP[monkey.left_name]
    monkey.set_left_child(left_child)

    right_child = MONKEY_LOOKUP[monkey.right_name]
    monkey.set_right_child(right_child)

print(ROOT.get_value())
