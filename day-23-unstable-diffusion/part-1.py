input_items = open('./example-input.txt').read().split('\n')
# input_items = open('./input.txt').read().split('\n')

print(input_items)

# Parse the starting grid

# Then iterate on cycles
#    At the start of a cycle, everyone figures out their next position
#    Any elves who think of the same position, skip a turn - they do not move
#    Everyone else moves to the new space
#    At the end of the cycle, Elves update their instruction orders, moving the first rule tothe end of the list
#        There is a list of rules in which elves consider their moves, and it's dynamic, cool

# The grid can expand - and the answer is th number of empty spaces "."
