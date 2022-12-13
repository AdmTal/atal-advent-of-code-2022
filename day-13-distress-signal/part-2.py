from itertools import zip_longest
from functools import total_ordering, cache

# input_items = open('./example-input.txt').read().split('\n')
input_items = open('./input.txt').read().split('\n')


@cache
def item_compare(left_str, right_str):
    left = eval(left_str)
    right = eval(right_str)
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
            resp = item_compare(str(l_item), str(r_item))
            if resp is not None:
                return resp
        return None

    if not left_is_int and right_is_int:
        return item_compare(str(left), str([right]))
    elif left_is_int and not right_is_int:
        return item_compare(str([left]), str(right))

    raise Exception('This line should be unreachable, and this will let me know if that is true')


@total_ordering
class Packet(object):
    def __init__(self, input_line):
        self._list = input_line

    @property
    def list(self):
        return self._list

    def __eq__(self, other):
        return item_compare(self.list, other.list) and item_compare(self.list, other.list)

    def __lt__(self, other):
        left_compare_result = item_compare(self.list, other.list)
        right_compare_result = item_compare(other.list, self.list)
        return left_compare_result and not right_compare_result

    def __str__(self):
        return f'{self._list}'


input_packets = [
    Packet('[[2]]'),
    Packet('[[6]]'),
]
need_a = True
need_b = True
for line in input_items + ['']:
    if need_a:
        input_packets.append(Packet(line))
        need_a = False
        continue
    if need_b:
        input_packets.append(Packet(line))
        need_b = False
        continue
    need_a = True
    need_b = True

decoder_key = 1
for idx, packet in enumerate(sorted(input_packets), start=1):
    if packet.list in ['[[2]]', '[[6]]']:
        decoder_key *= idx
print(decoder_key)
