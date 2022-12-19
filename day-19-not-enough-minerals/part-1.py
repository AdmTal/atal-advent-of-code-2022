from pprint import pprint
import re

input_items = open('./example-input.txt').read().split('\n')
# input_items = open('./input.txt').read().split('\n')

print(input_items)

input_re = re.compile(
    'Blueprint ([-0-9]+): Each ore robot costs ([-0-9]+) ore. Each clay robot costs ([-0-9]+) ore. Each obsidian robot costs ([-0-9]+) ore and ([-0-9]+) clay. Each geode robot costs ([-0-9]+) ore and ([-0-9]+) obsidian.')
for line in input_items:
    [
        blueprint_id,
        ore_robot_ore_cost,
        clay_robot_ore_cost,
        obsidian_robot_ore_cost,
        obsidian_robot_clay_cost,
        geode_robot_ore_cost,
        geode_robot_obsidian_cost
    ] = list(map(int, input_re.match(line).groups()))

    pprint({
        'blueprint_id': blueprint_id,
        'ore_robot_ore_cost': ore_robot_ore_cost,
        'clay_robot_ore_cost': clay_robot_ore_cost,
        'obsidian_robot_ore_cost': obsidian_robot_ore_cost,
        'obsidian_robot_clay_cost': obsidian_robot_clay_cost,
        'geode_robot_ore_cost': geode_robot_ore_cost,
        'geode_robot_obsidian_cost': geode_robot_obsidian_cost,
    })
