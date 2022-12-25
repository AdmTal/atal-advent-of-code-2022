# snafu_numbers = open('./example-input.txt').read().split('\n')
snafu_numbers = open('./input.txt').read().split('\n')


def snafu_to_decimal(snafu_number):
    result = 0
    curr_place = 0
    snafu_digits = list(reversed(snafu_number))
    while snafu_digits:
        curr_digit = snafu_digits.pop(0)
        curr_digit_value = snafu_digit_to_decimal(curr_digit)
        result += curr_digit_value * (5 ** curr_place)
        curr_place += 1
    return result


def snafu_digit_to_decimal(snafu_digit):
    return {
        '=': -2,
        '-': -1,
        '0': 0,
        '1': 1,
        '2': 2,
    }[snafu_digit]


def _snafit_for_digit(digit):
    return {
        '4': '-',
        '3': '=',
        '2': '2',
        '1': '1',
        '0': '0',
    }[str(int(digit))]


def decimal_to_snafu(decimal):
    """https://www.reddit.com/r/adventofcode/comments/zur1an/comment/j1mkms7"""
    # (1) Have an accumulator initialized to the decimal value.
    accum = decimal

    # (2) Have a string buffer to store the output.
    string_buffer = ''

    # (3) Take the modulo of the accumulator by the base size (in our case, 5).
    base = 5
    result = accum % base

    # (4) Convert the result of the previous step to the character that represents
    # the value on the other base. In our case, 4 becomes -, and 3 becomes =.
    # The other results remain the same.
    result_char = _snafit_for_digit(result)

    # (5) Append the character to the left of the string.
    string_buffer = f'{result_char}{string_buffer}'

    # (6) Subtract the digit's value from the accumulator.
    # Do not forget that - has a value of -1 and = a value of -2
    # (in which cases, you end up actually adding 1 or 2 to the accumulator).
    digit_value = snafu_digit_to_decimal(result_char)
    accum -= digit_value

    # (7) Divide the accumulator by the base size (in our case, 5).
    # Note: the accumulator should be divisible by the base size,
    # if you did not do anything wrong.
    accum = accum // base

    # 8 Repeat steps 3 to 7 until the accumulator is zero.
    # Then you have the string that represents the number in the other base.
    while accum != 0:
        # (3) Take the modulo of the accumulator by the base size (in our case, 5).
        base = 5
        result = accum % base

        # (4) Convert the result of the previous step to the character that represents
        # the value on the other base. In our case, 4 becomes -, and 3 becomes =.
        # The other results remain the same.
        result_char = _snafit_for_digit(result)

        # (5) Append the character to the left of the string.
        string_buffer = f'{result_char}{string_buffer}'

        # (6) Subtract the digit's value from the accumulator.
        # Do not forget that - has a value of -1 and = a value of -2
        # (in which cases, you end up actually adding 1 or 2 to the accumulator).
        accum -= snafu_digit_to_decimal(result_char)

        # (7) Divide the accumulator by the base size (in our case, 5).
        # Note: the accumulator should be divisible by the base size,
        # if you did not do anything wrong.
        accum = accum / base

    return ''.join(string_buffer)


input_sum = 0
for snafu_number in snafu_numbers:
    input_sum += snafu_to_decimal(snafu_number)

print(f'Input sum is {input_sum}')
print(f'Input sum converted to Snafu is {decimal_to_snafu(input_sum)}')
