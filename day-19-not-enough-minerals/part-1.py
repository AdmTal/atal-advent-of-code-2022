import re

input_items = open('./example-input.txt').read().split('\n')
# input_items = open('./input.txt').read().split('\n')

BLUEPRINTS = {}

BLUEPRINT_ID = 'blueprint_id'
ORE_BOT_ORE_COST = 'blueprint_id'
CLAY_BOT_ORE_COST = 'ore_robot_ore_cost'
OBSIDIAN_BOT_ORE_COST = 'clay_robot_ore_cost'
OBSIDIAN_BOT_CLAY_COST = 'obsidian_robot_ore_cost'
GEODE_BOT_ORE_COST = 'obsidian_robot_clay_cost'
GEODE_BOT_OBSIDIAN_COST = 'geode_robot_ore_cost'

input_re = re.compile(
    'Blueprint ([-0-9]+): '
    'Each ore robot costs ([-0-9]+) ore. '
    'Each clay robot costs ([-0-9]+) ore. '
    'Each obsidian robot costs ([-0-9]+) ore and ([-0-9]+) clay. '
    'Each geode robot costs ([-0-9]+) ore and ([-0-9]+) obsidian.')
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

    BLUEPRINTS[blueprint_id] = {
        BLUEPRINT_ID: blueprint_id,
        ORE_BOT_ORE_COST: ore_robot_ore_cost,
        CLAY_BOT_ORE_COST: clay_robot_ore_cost,
        OBSIDIAN_BOT_ORE_COST: obsidian_robot_ore_cost,
        OBSIDIAN_BOT_CLAY_COST: obsidian_robot_clay_cost,
        GEODE_BOT_ORE_COST: geode_robot_ore_cost,
        GEODE_BOT_OBSIDIAN_COST: geode_robot_obsidian_cost,
    }

inventories_after_all_possible_purchases_cache = {}


def inventories_after_all_possible_purchases(blueprint_id, inventory):
    cache_key = (blueprint_id, inventory)
    if cache_key in inventories_after_all_possible_purchases_cache:
        return inventories_after_all_possible_purchases_cache[cache_key]

    blueprint = BLUEPRINTS[blueprint_id]
    ore, clay, obsidian, open_geodes, ore_bots, clay_bots, obsidian_bots, geode_bots = inventory

    options = []

    # Explore options if we build an ORE bot
    if ore >= blueprint[ORE_BOT_ORE_COST]:
        updated_inventory = (
            ore - blueprint[ORE_BOT_ORE_COST],
            clay,
            obsidian,
            open_geodes,
            ore_bots + 1,
            clay_bots,
            obsidian_bots,
            geode_bots,
        )
        options += [updated_inventory] + inventories_after_all_possible_purchases(blueprint_id, updated_inventory)

    # Explore options if we build a CLAY bot
    if ore >= blueprint[CLAY_BOT_ORE_COST]:
        updated_inventory = (
            ore - blueprint[CLAY_BOT_ORE_COST],
            clay,
            obsidian,
            open_geodes,
            ore_bots,
            clay_bots + 1,
            obsidian_bots,
            geode_bots,
        )
        options += [updated_inventory] + inventories_after_all_possible_purchases(blueprint_id, updated_inventory)

    # Explore options if we build an OBSIDIAN bot
    if ore >= blueprint[OBSIDIAN_BOT_ORE_COST] and clay >= blueprint[OBSIDIAN_BOT_CLAY_COST]:
        updated_inventory = (
            ore - blueprint[OBSIDIAN_BOT_ORE_COST],
            clay - blueprint[OBSIDIAN_BOT_CLAY_COST],
            obsidian,
            open_geodes,
            ore_bots,
            clay_bots,
            obsidian_bots + 1,
            geode_bots,
        )
        options += [updated_inventory] + inventories_after_all_possible_purchases(blueprint_id, updated_inventory)

    # Explore options if we build a GEODE bot
    if ore >= blueprint[GEODE_BOT_ORE_COST] and obsidian >= blueprint[GEODE_BOT_OBSIDIAN_COST]:
        updated_inventory = (
            ore - blueprint[GEODE_BOT_ORE_COST],
            clay,
            obsidian - blueprint[GEODE_BOT_OBSIDIAN_COST],
            open_geodes,
            ore_bots,
            clay_bots,
            obsidian_bots,
            geode_bots + 1,
        )
        options += [updated_inventory] + inventories_after_all_possible_purchases(blueprint_id, updated_inventory)

    inventories_after_all_possible_purchases_cache[cache_key] = options
    print(f'{cache_key} -> {len(options)}')
    return options


max_geodes_possible_cache = {}


def max_geodes_possible(blueprint_id, inventory, time_left):
    cache_key = (blueprint_id, inventory, time_left)
    if cache_key in max_geodes_possible_cache:
        return max_geodes_possible_cache[cache_key]
    # Parse Invetory
    ore, clay, obsidian, open_geodes, ore_bots, clay_bots, obsidian_bots, geode_bots = inventory

    # Can't make any geodes if there are no time left
    if time_left <= 0:
        max_geodes_possible_cache[cache_key] = open_geodes
        return open_geodes

    # calculate the expected yield at the end of the current minute
    new_materials_at_end_of_minute = (
        ore + ore_bots,
        clay + clay_bots,
        obsidian + obsidian_bots,
        open_geodes + geode_bots,
    )

    if time_left == 1:
        return new_materials_at_end_of_minute[3]

    # Figure out all purchasing options from here
    purchasing_scenarios = inventories_after_all_possible_purchases(blueprint_id, inventory)

    if not purchasing_scenarios:
        updated_inventory = new_materials_at_end_of_minute + (ore_bots, clay_bots, obsidian_bots, geode_bots)
        return max_geodes_possible(blueprint_id, updated_inventory, time_left - 1)

    # To start, this is like, if we make no purchases (do nothing)
    best_option = new_materials_at_end_of_minute[3]

    for resulting_inventory in purchasing_scenarios:
        n_ore, n_clay, n_obsidian, n_open_geodes, n_ore_bots, n_clay_bots, n_obsidian_bots, n_geode_bots = resulting_inventory

        best_option = max(
            best_option,
            max_geodes_possible(
                blueprint_id,
                (
                    n_ore + new_materials_at_end_of_minute[0],
                    n_clay + new_materials_at_end_of_minute[1],
                    n_obsidian + new_materials_at_end_of_minute[2],
                    n_open_geodes + new_materials_at_end_of_minute[3],
                    n_ore_bots + ore_bots,
                    n_clay_bots + clay_bots,
                    n_obsidian_bots + obsidian_bots,
                    n_geode_bots + geode_bots
                ),
                time_left - 1
            )
        )

    max_geodes_possible_cache[cache_key] = best_option
    return best_option


starting_inventory = (
    0,  # ORE
    0,  # CLAY
    0,  # OBSIDIAN
    0,  # OPEN GEODES
    1,  # ORE COLLECTING BOTS
    0,  # CLAY COLLECTING BOTS
    0,  # OBSIDIAN COLLECTING BOTS
    0,  # GEODE CRACKING BOTS
)

ELEPHANT_PATIENCE_IN_MINUTES = 24

quality_level_sum = 0
for blueprint_id in BLUEPRINTS.keys():
    max_geodes = max_geodes_possible(blueprint_id, starting_inventory, ELEPHANT_PATIENCE_IN_MINUTES)
    blueprint_quality = blueprint_id * max_geodes
    print(f'Blueprint ID = {blueprint_id}; Max Geodes = {max_geodes}; Quality Level = {blueprint_quality}')
    quality_level_sum += blueprint_quality

print(f'Sum of all quality levels = {quality_level_sum}')
