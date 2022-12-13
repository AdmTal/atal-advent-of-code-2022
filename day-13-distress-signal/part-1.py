from itertools import zip_longest

# input_items = open('./example-input.txt').read().split('\n')
input_items = open('./input.txt').read().split('\n')

input_pairs = []
need_a = True
need_b = True
next_pair = []
for line in input_items + ['']:
    if need_a:
        next_pair.append(eval(line))
        need_a = False
        continue
    if need_b:
        next_pair.append(eval(line))
        need_b = False
        continue
    need_a = True
    need_b = True
    input_pairs.append(next_pair)
    next_pair = []


def item_compare(left, right):
    left_is_int = type(left) == int
    right_is_int = type(right) == int

    if left_is_int and right_is_int:
        if left == right:
            return None
        return left <= right

    if not left_is_int and not right_is_int:
        for l_item, r_item in zip_longest(left, right, fillvalue=None):
            if l_item is None:
                return True
            if r_item is None:
                return False
            resp = item_compare(l_item, r_item)
            if resp is not None:
                return resp
        return None

    if not left_is_int and right_is_int:
        return item_compare(left, [right])
    elif left_is_int and not right_is_int:
        return item_compare([left], right)

    raise Exception('This line should be unreachable, and this will let me know if that is true')


sum_of_good_indicies = 0
for idx, pair in enumerate(input_pairs, start=1):
    left, right = pair

    if item_compare(left, right):
        sum_of_good_indicies += idx

print(sum_of_good_indicies)
