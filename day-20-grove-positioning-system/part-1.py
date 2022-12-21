# input_items = open('./input.txt').read().split('\n')
input_items = open('./example-input.txt').read().split('\n')


class Digit(object):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value


# A list of pointers, so we know original input order
original_digit_order = [Digit(i) for i in list(map(int, input_items))]

NUM_NUMS = len(original_digit_order)

# Also, a list of numbers, so we know the current ordering after mixing
mixed_digits = [i for i in original_digit_order]

zero_digit = None

actuals = [[i.value for i in mixed_digits]]
# Mix all numbers once
for original_digit in original_digit_order:

    # Keep track of Zero, needed later
    if not original_digit.value:
        zero_digit = original_digit
        actuals.append([i.value for i in mixed_digits])
        continue

    # Find the current location of the original digit
    current_location = mixed_digits.index(original_digit)

    # If the value is positive, move it forward in the list
    if original_digit.value > 0:
        next_location = current_location + original_digit.value
        if next_location > NUM_NUMS:
            new_index = next_location % NUM_NUMS + 1
        else:
            new_index = next_location % NUM_NUMS
    else:
        # If the value is negative, move it backwards in the list
        new_index = 0
        # Mod should never be negative ... ?


    mixed_digits.pop(current_location)
    mixed_digits.insert(new_index, original_digit)

    actuals.append([i.value for i in mixed_digits])

location_of_zero = mixed_digits.index(zero_digit)

a = mixed_digits[(location_of_zero + 1000) % NUM_NUMS].value
b = mixed_digits[(location_of_zero + 2000) % NUM_NUMS].value
c = mixed_digits[(location_of_zero + 3000) % NUM_NUMS].value

print(f'1000th = {a}')
print(f'2000th = {b}')
print(f'3000th = {c}')

print('SUM = ', sum((a, b, c)))

tests = [
    [1, 2, -3, 3, -2, 0, 4],
    [2, 1, -3, 3, -2, 0, 4],
    [1, -3, 2, 3, -2, 0, 4],
    [1, 2, 3, -2, -3, 0, 4],
    [1, 2, -2, -3, 0, 3, 4],
    [1, 2, -3, 0, 3, 4, -2],
    [1, 2, -3, 0, 3, 4, -2],
    [1, 2, -3, 4, 0, 3, -2],
]

for expected, actual in zip(tests, actuals):
    print(f'{expected == actual}')
