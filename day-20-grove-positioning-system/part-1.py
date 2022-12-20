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

# Mix all numbers once
for digit in original_digit_order:

    # Keep track of Zero, needed later
    if not digit.value:
        zero_digit = digit
        print([i.value for i in mixed_digits])
        continue

    # Find the current location of the original digit
    current_location = mixed_digits.index(digit)

    # If the value is positive, move it forward in the list
    if digit.value > 0:
        new_index = (current_location + 1 + digit.value) % NUM_NUMS
    else:
        # If the value is negative, move it backwards in the list
        # Cheated = https://stackoverflow.com/questions/14785443/is-there-an-expression-using-modulo-to-do-backwards-wrap-around-reverse-overfl
        new_index = ((current_location - 1 + digit.value) % NUM_NUMS + NUM_NUMS) % NUM_NUMS

    mixed_digits.pop(current_location)
    mixed_digits.insert(new_index, digit)

    print([i.value for i in mixed_digits])

location_of_zero = mixed_digits.index(zero_digit)
print(mixed_digits[location_of_zero].value)

a = mixed_digits[(location_of_zero + 1000) % NUM_NUMS].value
b = mixed_digits[(location_of_zero + 2000) % NUM_NUMS].value
c = mixed_digits[(location_of_zero + 3000) % NUM_NUMS].value

print(f'1000th = {a}')
print(f'2000th = {b}')
print(f'3000th = {c}')

print('SUM = ', sum((a, b, c)))
