import math
import shelve
import operator
import sys
import os

import libtcodpy as libtcod

# import json
import yaml

# from operator import itemgetter, attrgetter

# actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MESSAGE_BAR_HEIGHT = 10
INFO_BAR_WIDTH = 40

VIEWPORT_WIDTH = SCREEN_WIDTH - INFO_BAR_WIDTH
VIEWPORT_HEIGHT = SCREEN_HEIGHT - MESSAGE_BAR_HEIGHT

WELCOME_SCREEN_HEIGHT = 10

# size of the map
MAP_WIDTH = 40
MAP_HEIGHT = 40

# set this up for a new game
libtcod.namegen_parse('standard_names.txt')

pause = False
debug_mode = 0

log_information = 0  # always should be at zero unless bughunting for specifics.
log_sales = 0

# gameplay variables set at start

f = open('data/init/available_fonts.txt', 'r')
available_fonts = yaml.load(f.read())
f.close()

f = open('data/init/menu_title.txt', 'r')
menu_title = yaml.load(f.read())
f.close()

font_index = 0

# item examined: Player gets to examine a single item per day, resetting every day.
item_examined = 0

evil_counter = 0
chaos_counter = 0

player_name = 'Player'

#############
## NAME LISTS ##
#############

contract_types = [
    'dungeon',  # go to a dungeon and do shit
    'monster',  # go and kill a monster
    'item_hunt',
]

f = open('data/names/male_forename_list.txt', 'r')
male_forename_list = yaml.load(f.read())
f.close()

f = open('data/names/female_forename_list.txt', 'r')
female_forename_list = yaml.load(f.read())
f.close()

f = open('data/names/hero_surname_list.txt', 'r')
hero_surname_list = yaml.load(f.read())
f.close()

# one wonders what the difference between a male and a female surname is?

f = open('data/names/monster_forenames.txt', 'r')
monster_forenames = yaml.load(f.read())
f.close()

f = open('data/names/wandering_monster_types.txt', 'r')
wandering_monster_types = yaml.load(f.read())
f.close()

f = open('data/dungeons/dungeon_type_list.txt', 'r')
dungeon_type_list = yaml.load(f.read())
f.close()
# type of place, and associated icon

f = open('data/names/nasty_things_suffixes.txt', 'r')
nasty_things_suffixes = yaml.load(f.read())
f.close()

f = open('data/names/nasty_things_prefixes.txt', 'r')
nasty_things_prefixes = yaml.load(f.read())
f.close()
# some nasty prefixes e.g. Y X -> Horrible Keep

common_quirks = [  # some common personality quirks
                   'thrifty',  # accepts a smaller mark up
                   'extravagant',  # low interest in money - spends more
                   'unfriendly',  # gains unfriendly relationship twice as fast
                   'friendly',  # gains positive relationship points twice as fast
                   'hoarder',
                   'luxuriant',
                   'lazy',
                   'critic',
                   'musician',
                   'thief',
                   'spartan',  # only wears clothing? Temple quirk?
                   ]

uncommon_quirks = [
    'miser',  # very tight on mark up
    'wasteful',  # very loose on mark up
]

f = open('data/names/town_names.txt', 'r')
town_names = yaml.load(f.read())
f.close()

f = open('data/events/event_chat_with_pre.txt', 'r')
event_chat_with_pre = yaml.load(f.read())
f.close()

f = open('data/events/event_chat_with_post.txt', 'r')
event_chat_with_post = yaml.load(f.read())
f.close()

f = open('data/events/event_enter_town_by_faction.txt', 'r')
event_enter_town_by_faction = yaml.load(f.read())
f.close()

f = open('data/events/event_leave_town_by_faction.txt', 'r')
event_leave_town_by_faction = yaml.load(f.read())
f.close()

f = open('data/events/event_world_by_faction.txt', 'r')
event_world_by_faction = yaml.load(f.read())
f.close()

f = open('data/events/event_tout.txt', 'r')
event_tout = yaml.load(f.read())
f.close()

f = open('data/events/event_fight_monster.txt', 'r')
event_fight_monster = yaml.load(f.read())
f.close()

f = open('data/events/event_fight.txt', 'r')
event_fight = yaml.load(f.read())
f.close()

f = open('data/events/event_success_fight.txt', 'r')
event_success_fight = yaml.load(f.read())
f.close()

f = open('data/events/event_damaged_fight.txt', 'r')
event_damaged_fight = yaml.load(f.read())
f.close()

f = open('data/events/event_down_stairs.txt', 'r')
event_down_stairs = yaml.load(f.read())
f.close()

f = open('data/events/event_up_stairs.txt', 'r')
event_up_stairs = yaml.load(f.read())
f.close()

f = open('data/events/event_misc_evil.txt', 'r')
event_misc_evil = yaml.load(f.read())
f.close()

f = open('data/events/event_misc_good.txt', 'r')
event_misc_good = yaml.load(f.read())
f.close()

f = open('data/events/event_misc_neutral.txt', 'r')
event_misc_neutral = yaml.load(f.read())
f.close()

f = open('data/events/event_item_location.txt', 'r')
event_item_location = yaml.load(f.read())
f.close()

f = open('data/events/event_item_found.txt', 'r')
event_item_found = yaml.load(f.read())
f.close()

f = open('data/events/event_item_bought.txt', 'r')
event_item_bought = yaml.load(f.read())
f.close()

f = open('data/events/event_item_sold.txt', 'r')
event_item_sold = yaml.load(f.read())
f.close()

f = open('data/events/event_gain_level.txt', 'r')
event_gain_level = yaml.load(f.read())
f.close()

f = open('data/events/event_puzzle.txt', 'r')
event_puzzle = yaml.load(f.read())
f.close()

f = open('data/events/event_lair.txt', 'r')
event_lair = yaml.load(f.read())
f.close()

f = open('data/events/event_avoid_trap.txt', 'r')
event_avoid_trap = yaml.load(f.read())
f.close()

f = open('data/events/event_trap.txt', 'r')
event_trap = yaml.load(f.read())
f.close()

f = open('data/events/event_sneak_fight.txt', 'r')
event_sneak_fight = yaml.load(f.read())
f.close()

f = open('data/events/event_avoid_trapdoor.txt', 'r')
event_avoid_trapdoor = yaml.load(f.read())
f.close()

f = open('data/events/event_trapdoor.txt', 'r')
event_trapdoor = yaml.load(f.read())
f.close()

f = open('data/events/event_gain_entry.txt', 'r')
event_gain_entry = yaml.load(f.read())
f.close()

f = open('data/events/event_failed_entry.txt', 'r')
event_failed_entry = yaml.load(f.read())
f.close()

f = open('data/events/event_know_treasure_room.txt', 'r')
event_know_treasure_room = yaml.load(f.read())
f.close()

f = open('data/events/event_bemused_treasure_room.txt', 'r')
event_bemused_treasure_room = yaml.load(f.read())
f.close()

f = open('data/events/event_graveyard.txt', 'r')
event_graveyard = yaml.load(f.read())
f.close()

##################
## DUNGEON LAYOUTS ##
##################

dungeon_tasks = [  # list of tasks that should ONLY happen in dungeon (but may be accidentally called in town ...)
                   'find_item',
                   'trap',
                   'treasure_room',
                   'secret_room',
                   'trap_door',
                   'mundane',
                   'lair',
                   'graveyard',
                   'puzzle',
                   'cursed_altar',
                   'explore',
                   'fight'
                   ]

f = open('data/dungeons/dungeon_layouts.txt', 'r')
dungeon_layouts = yaml.load(f.read())
f.close()


# ~ dungeon_layouts = {
# ~ 'default':{'trap': 10, 'treasure_room': 10, 'secret_room': 20, 'trap_door': 20, 'mundane': 200 },
# ~ 'lair':{'trap': 20, 'lair': 60, 'graveyard':10, 'mundane': 100 },
# ~ 'crypt':{'trap': 40, 'treasure_room': 20, 'graveyard': 20, 'puzzle': 20, 'trap_door': 10, 'cursed_altar': 5, 'mundane': 120}
# ~ }

def build_dungeon_room_tables():
    global built_dungeon_room_tables, dungeon_layout_list

    built_dungeon_room_tables = {}
    dungeon_layout_list = []

    for key, value in dungeon_layouts.iteritems():

        max_dice_roll = 0
        rooms = []

        for sub_key, sub_value in value.iteritems():
            max_dice_roll += sub_value
            this_chance = max_dice_roll
            rooms.append([sub_key, this_chance])

        built_dungeon_room_tables[key] = [rooms, max_dice_roll]
        dungeon_layout_list.append(key)


def floor_feature(dungeon_type):
    max_roll = built_dungeon_room_tables[dungeon_type][1]

    roll = libtcod.random_get_int(0, 0, max_roll)

    for n in built_dungeon_room_tables[dungeon_type][0]:
        if roll <= n[1]:
            room_type = n[0]
            break

    if debug_mode:
        message('EXPLORED: ' + str(room_type) + ', dungeon type ' + str(dungeon_type), libtcod.light_grey,
                libtcod.light_grey)

    return room_type


#############################
## GAME FLOW and OTHER VARIABLES  ##
#############################
##OPTIONS
# game speed

daft_speed = 3
fast_speed = 8  # ticks per hour, fast (key 5) DEFAULT = 8
normal_speed = 12
slow_speed = 20  # ticks per hour, slow (default - key 6) DEFAULT = 15

LIMIT_FPS = 25  # frames-per-second maximum, controls game speed / flow

game_speed = slow_speed

day = 1
day_count = 0  # total days
year = 0

# chaos and evil based event spawning

base_chaos_event_rate = 30  # first new dungeon in approximately one month at 25 and 3 dungeons
evil_event_rate = 130  # first monster mid february at 100 ... generally, but currently looking c. 125

maximum_monsters = 1

# heroes visiting town
contract_visit_rate = 2  # relative effect of additional contracts
base_visit_rate = 10  # base rate - 10 is about 1 (or slightly less than 1) per day with no contract modifiers.

merchant_enter_town_rate = 5  # percent enter town every day. about 8 or 9 merchants on average ... do the math ...

# contract cost balancing
contract_base_price = 10  # base acceptance cost per level
contract_base_stat_modifier = 5  # bravado, wimp etc.

# hero balancing
hero_base_hp = 2
hero_base_hp_level_gain = 3
hero_base_markup = 1.2

# hero move chance. Number of hours per move average.
hero_base_speed = 2

# hero town rest etc.
base_heal_rate = 1

# starting population of dungeons
min_dungeon_pop = 35
max_dungeon_pop = 70

churn_rate = 15

# monster stuff.
monster_move_chance = 15  # percentage per hour

monster_base_strength = 8
monster_base_hp = 8

# turns and sub-turns for game flow management, start at the beginning
turns = 0
sub_turns = 0

## hero corpse behaviour

hero_rot_time = 15  # hero rots in this number of days

## World chaos variables

total_item_evil = 50  # starting points
total_item_chaos = 50

############################
## experience counting / level pacing  ##
############################

# measure how fast levels go up (x * base_level to get to next level)

dungeon_base_level_exp = 3  # x dead heroes at level 1 ... 4 seems to be about right?? Tweaked down to 3 for new system
store_base_level_exp = 90  # a bit slow at 100 probably ...
hero_base_level_exp = 150  # a bit quick at 100 probably ... 200 now seems a bit slow on rebalance of monster appearance / deaths etc.

############
## FINANCES  ##
############

tax_rate = 25  # starter tax, per month. To change depending on circumstances (mainly world chaos)

# shop statuses

selling_goods = 1  # shop open for business
accepting_offers = 0  # won't accept offers from Heroes


##############
##    CLASSES    ##
##############

class Tile:
    # a tile of the map and its properties

    def __init__(self, blocked, block_sight, faction, name, legend, shop, dungeon, color):
        self.blocked = blocked
        self.block_sight = block_sight
        self.faction = faction
        self.name = name
        self.legend = legend
        self.shop = shop
        self.dungeon = dungeon
        self.color = color


class Reputation:
    def __init__(self, xp, by_faction):
        self.xp = xp  # a measure of experience ... thinking 100*base_level to go up a level, could have a look-up table ...
        self.by_faction = by_faction  # what is this? a dictionary? It appears so ...

    def improve_reputation(self, faction, value=1):
        self.by_faction[faction] += value

    def worsen_reputation(self, faction, value=1):
        self.by_faction[faction] -= value


class Store:
    # the details of a shop, or anything within a building / cellar or whatever
    # Note the class is called a Store, the attribute of Tile is called a shop
    def __init__(self, inventory, wealth, base_level, reputation, owner_name, activitylog, layout):

        self.inventory = inventory
        self.wealth = wealth
        self.base_level = base_level
        self.reputation = reputation
        self.owner_name = owner_name
        self.activitylog = activitylog

    def gain_experience(self, exp):

        self.reputation.xp += exp  # add the amount of experience points
        if self.reputation.xp >= (self.base_level * store_base_level_exp):  # check if we cross our level threshold
            self.gain_level()  # gain a level
            self.reputation.xp = 0  # reset the experience counter

    def gain_level(self):

        self.base_level += 1
        if self == player:
            message('Level up!', libtcod.light_green, libtcod.dark_green)
            choose_upgrade()

    def raise_contract(self, asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                       visible, paid, accepted=False):

        new_contract = Contract(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                                visible, paid, accepted)

        the_mayoress.noticeboard.notices.append(new_contract)

    def rescue_corpse(self, hero):

        for shop in shop_list:
            faction = shop[0]
            name = shop[1]
            x = shop[2]
            y = shop[3]
            if map[x][y].shop == self:
                break

        asking_price = hero.base_level * 10
        mission_type = 'raise_dead'
        target_name = hero.name
        contract_type = 'town'
        asking_faction = faction
        defining_motive = ['balance']
        visible = True
        paid = False

        self.raise_contract(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                            visible, paid, False)

    def delve_dungeon(self, dungeon_name):

        for shop in shop_list:
            faction = shop[0]
            name = shop[1]
            sx = shop[2]
            sy = shop[3]
            if map[sx][sy].shop == self:
                break

        dungeon_location = return_dungeon_location_by_name(dungeon_name)

        x = dungeon_location[2]
        y = dungeon_location[3]

        asking_price = map[x][y].dungeon.base_level * 10 + libtcod.random_get_int(0, 0, 10)
        mission_type = 'default'
        target_name = dungeon_name
        contract_type = 'dungeon'
        asking_faction = faction
        defining_motive = ['glory', 'leadership']
        visible = True
        paid = False

        self.raise_contract(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                            visible, paid, False)

    def fetch_me_an_item(self, dungeon_name):

        for shop in shop_list:
            faction = shop[0]
            name = shop[1]
            sx = shop[2]
            sy = shop[3]
            if map[sx][sy].shop == self:
                break

        dungeon_location = return_dungeon_location_by_name(dungeon_name)

        x = dungeon_location[2]
        y = dungeon_location[3]

        asking_price = libtcod.random_get_int(0, 0, 20) + map[x][y].dungeon.base_level * 10
        mission_type = 'item_hunt'
        target_name = dungeon_name
        contract_type = 'dungeon'
        asking_faction = faction
        defining_motive = ['loot', 'contracts']
        visible = True
        paid = False

        self.raise_contract(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                            visible, paid, False)

    def stay_a_while_and_listen(self):

        for shop in shop_list:
            faction = shop[0]
            name = shop[1]
            x = shop[2]
            y = shop[3]
            if map[x][y].shop == self:
                break

        asking_price = 0
        mission_type = 'socialise'
        target_name = None
        contract_type = 'town'
        asking_faction = faction
        defining_motive = ['social']
        visible = False
        paid = True


class Mayoress:
    # the town power figure
    def __init__(self, inventory, wealth, base_level, reputation, population, alignment, order, noticeboard,
                 personality, flags):

        self.inventory = inventory
        self.wealth = wealth
        self.base_level = base_level
        self.reputation = reputation
        self.population = population
        self.alignment = alignment
        self.order = order
        self.noticeboard = noticeboard
        self.personality = personality
        self.flags = flags

    def raise_contract(self, asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                       visible, paid, accepted=False):

        new_contract = Contract(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                                visible, paid, accepted)
        self.noticeboard.notices.append(new_contract)

    def review_town_safety(self):
        ##function to determine how safe the town is, and raise contracts accordingly.
        contract_types = []
        contract_targets = []

        for contract in self.noticeboard.notices:
            contract_types.append(contract.contract_type)
            contract_targets.append(contract.target_name)

        dead_count = self.flags.count('hero_died')
        for n in range(dead_count):
            hero_index = -1 - n
            if self.wealth > dead_heroes[hero_index][0].base_level * 20:
                self.rescue_corpse(dead_heroes[hero_index][0])
                self.flags.remove('hero_died')

        bored_hero = self.flags.count('bored_hero')
        for n in range(bored_hero):
            hero_index = -1 - n
            self.stay_a_while_and_listen()
            self.flags.remove('bored_hero')

        for dungeon in dungeon_list:
            x = dungeon[2]
            y = dungeon[3]

            if map[x][y].dungeon.population > map[x][y].dungeon.base_level * 150:
                if map[x][y].name not in contract_targets:
                    if self.wealth > map[x][y].dungeon.base_level * 20:
                        self.delve_dungeon(map[x][y].name)
                        message('The Mayoress is taking action against the ' + map[x][y].name, libtcod.light_green,
                                libtcod.dark_green)

        # general maintenance
        if len(monster_list) > 0:
            for monster in monster_list:
                if monster.name not in contract_targets:
                    if self.wealth > monster.base_level * 30:
                        self.repel_monster(monster)

    def rescue_corpse(self, hero):

        asking_price = hero.base_level * 20
        mission_type = 'raise_dead'
        target_name = hero.name
        contract_type = 'town'
        asking_faction = 'Mayoress'
        defining_motive = ['balance', 'leadership']
        visible = True
        paid = False

        new_contract = Contract(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                                visible, paid, False)
        self.noticeboard.notices.append(new_contract)

    def delve_dungeon(self, dungeon_name):

        dungeon_location = return_dungeon_location_by_name(dungeon_name)

        x = dungeon_location[2]
        y = dungeon_location[3]

        asking_price = map[x][y].dungeon.base_level * 20
        mission_type = 'default'
        target_name = dungeon_name
        contract_type = 'dungeon'
        asking_faction = 'Mayoress'
        defining_motive = ['glory', 'leadership']
        visible = True
        paid = False

        new_contract = Contract(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                                visible, paid, False)
        self.noticeboard.notices.append(new_contract)

    def repel_monster(self, monster):

        asking_price = monster.base_level * 30
        mission_type = 'monster_hunt'
        target_name = monster.name
        contract_type = 'monster'
        asking_faction = 'Mayoress'
        defining_motive = ['glory', 'contracts', 'balance']
        visible = True
        paid = False

        new_contract = Contract(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                                visible, paid, False)
        self.noticeboard.notices.append(new_contract)

    def stay_a_while_and_listen(self):

        asking_price = 0
        mission_type = 'socialise'
        target_name = None
        contract_type = 'town'
        asking_faction = 'Mayoress'
        defining_motive = ['social', 'knowledge']
        visible = False
        paid = True

        new_contract = Contract(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                                visible, paid, False)
        self.noticeboard.notices.append(new_contract)


class Noticeboard:
    # the collection of information that the mayoress holds, accessible to all heroes. Allows for information dispersal back to town.
    def __init__(self, notices, rumours):
        self.notices = notices
        self.rumours = rumours


class Rumour:
    def __init__(self, dungeon_name, dungeon_level, rumour_type, rumour_length):
        self.dungeon_name = dungeon_name
        self.dungeon_level = dungeon_level
        self.rumour_type = rumour_type
        self.rumour_length = rumour_length

    def pass_day(self):
        self.rumour_length -= 1


class Brain:
    # the new personality / black
    def __init__(self, flags, personality, decisions, contract, phase):
        self.flags = flags  # list of things relevant to activity, for polling by other functions
        self.personality = personality  # the personality of the brain defined in line with the guild membership and at 'birth'
        self.decisions = decisions  # list of decisions made in line with the personality
        self.contract = contract  # used to hold any contract information
        self.phase = phase  # over arching theme of adventuring purpose


class Contract:
    # contracts to be defined as a class for information sharing around
    def __init__(self, asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive, visible,
                 paid, accepted):
        self.asking_price = asking_price
        self.mission_type = mission_type
        self.target_name = target_name
        self.contract_type = contract_type
        self.asking_faction = asking_faction
        self.defining_motive = defining_motive
        self.visible = visible
        self.paid = paid
        self.accepted = accepted

    def accept_me(self, name):
        self.accepted = name


class Dungeon:
    # the details of a dungeon
    def __init__(self, inventory, wealth, base_level, reputation, population, alignment, order, layout, dungeon_type):

        self.inventory = inventory
        self.wealth = wealth
        self.base_level = base_level
        self.reputation = reputation
        self.population = population
        self.alignment = alignment
        self.order = order
        self.layout = layout
        self.dungeon_type = dungeon_type

    def churn(self):  # function churns the population of the dungeon to reflect an ideal population level

        daily_shift = churn_rate / len(dungeon_list)  # the maximum percentage shift per day in population back to ideal

        wealth_pop = self.wealth / 10  # modifier for wealth
        level_pop = self.base_level * 100  # modifier for dungeon level
        item_pop = len(self.inventory)  # modifier for number of items held by dungeon
        # need a modifier for the evil-ness of the world

        ideal_population = wealth_pop + level_pop + item_pop  # plus other modifiers as they appear

        population_difference = self.population - ideal_population

        if population_difference < 0:
            population_difference = ((population_difference ** 2) ** 0.5)

            mod = int(population_difference * daily_shift / 100)
            if not mod == 0:
                modify_population = libtcod.random_get_int(0, 0, mod)

                self.population += modify_population
        else:
            mod = int(population_difference * daily_shift / 100)
            if not mod == 0:
                modify_population = libtcod.random_get_int(0, 0, mod)

                self.population -= modify_population

    def breed_creatures(self, number=50):  # add number to the population counter, default 50

        self.population += number

    def gain_experience(self, level):

        self.reputation.xp += level  # gain experience equivalent to the level of the hero killed (or whatever we send to the dungeon)
        if self.reputation.xp >= (self.base_level * dungeon_base_level_exp):  # do we cross the level threshold
            self.gain_level()
            self.reputation.xp = 0

    def gain_level(self):

        self.base_level += 1
        message('A Dungeon has increased in its evil power! Monsters flock from the forest!', libtcod.red,
                libtcod.dark_red)

        self.breed_creatures()
        self.wealth += libtcod.random_get_int(0, self.base_level * 500, self.base_level * 1000)

        new_items = generate_inventory(self.base_level * 10, self.base_level * 20, 1, self.base_level + 2)

        for item in new_items:
            self.inventory.append(item)


class Hero:
    # The details of a Hero, who moves around the place for the benefit of his faction or himself
    def __init__(self, inventory, equipment, wealth, base_level, reputation, stats, faction, x, y, itch, in_dungeon,
                 name, age, hp, wounds, brain, alignment, order, activitylog, owner_name):

        self.inventory = inventory  # carried stuff, for selling, stuff that has been bought.
        self.equipment = equipment  # current equipment. Will try to equip one armor, one weapon, one clothing.
        self.wealth = wealth  # wealth, in dollars
        self.base_level = base_level  # level of hero
        self.reputation = reputation  # measure of reputation (or experience points ...)
        self.stats = stats  # the real and perceived effectiveness of a hero. If he thinks is not good enough, he could use up scrolls to buff himself {perceived:value , real:value}
        self.faction = faction  # associated faction
        self.x = x  # x location on map -> tends to visit shops
        self.y = y  # y location on map -> tends to visit shops
        self.itch = itch  # a timer to dictate how long hero stays in town (days)
        self.in_dungeon = in_dungeon  # is hero in a dungeon?
        self.name = name  # name of hero
        self.age = age  # age of hero, in years
        self.hp = hp  # hitpoints
        self.wounds = wounds  # details of any lingering wounds, including mortal ones that may lead to death in town (drive to visit temple?) LIST
        self.brain = brain
        # self.personality = personality #personality tokens, for flavour and future decision making - NOW CONTAINED IN BRAIN
        self.alignment = alignment  # alignment, 1-100 (evil - good)
        self.order = order  # order, 1-100 (chaotic - lawful)
        self.activitylog = activitylog  # to log the memory and actions of the hero ... notable or otherwise
        self.owner_name = owner_name

    def gain_experience(self, number):

        self.reputation.xp += number  # gain the number of xp
        if self.reputation.xp >= (self.base_level * hero_base_level_exp):  # do we cross the level threshold
            self.gain_level()
            self.reputation.xp = 0

    def gain_level(self):

        self.base_level += 1
        # hero_message(self.name + ' has gained a level!')
        self.activitylog['history'].append(pick_random_from_list(event_gain_level))
        self.hp['max'] += hero_base_hp_level_gain
        # need to also add personality defects ...

        self.add_perks()

    def add_perks(self):  # a hero might get a new perk at each level

        try:
            new_perk = perk_tables[self.faction][self.base_level]
            self.brain.personality.perk.append(new_perk)
        except:
            pass

    def go_home(self):  ##PLEASE DON'T CALL GO HOME UNNECCASARILY WHILST IN DUNGEON
        if find_shop_by_faction(self.faction):
            [x, y] = find_shop_by_faction(self.faction)
            self.x = x
            self.y = y
        else:
            destination = pick_random_from_list(shop_list_inc_player)

            [x, y] = [destination[2], destination[3]]
            self.x = x
            self.y = y

    def browse_stock(self,
                     type='all'):  # currently make an attempt to buy anything we like the look of. Can ask for a type.
        x = self.x
        y = self.y
        # which shop are we at? Location defined by location of hero ...

        for shops in shop_list:
            if x == shops[2]:
                if y == shops[3]:  # shop location found
                    if shops[1] == 'Auction House':
                        pass  # need to place a bid, rather than purchase ... not currently supported
                    elif shops[1] == 'Players Shop' and not selling_goods:
                        pass
                    else:
                        for index in range(len(map[x][
                                                   y].shop.inventory)):  # hero x,y matches the shop that he is present at, of course
                            item = map[x][y].shop.inventory[index]
                            appraised_value = appraise_value(item, self.faction,
                                                             self.base_level) * self.brain.personality.markup  # find out what we think it is worth
                            appraised_value += self.reputation.by_faction[map[x][y].faction]

                            item_type = master_item_list[item[0]][9]
                            if item_type == type or type == 'all':  # this item matches our shopping preferences
                                ##CAN WE CHECK HERE WHETHER IT IS GOOD ENOUGH?? i.e. better than what we hold ...
                                if item[5] <= appraised_value:  # this item is priced in our range
                                    item_type = master_item_list[item[0]][
                                        9]  # reference before we muck about with inventories
                                    price = item[5]
                                    if buy_item(self, map[x][y].shop,
                                                index):  # make an attempt to buy it, if we think it is worthwhile. The player is a shop, in terms of the 'buy_item' function
                                        self.reputation.improve_reputation(map[x][y].faction)
                                        if map[x][y].faction == player_name:
                                            hero_message(
                                                self.name + ' bought ' + item_type + ' from ' + map[x][y].faction,
                                                libtcod.light_green, libtcod.dark_green)
                                            log_sale(player_item_display(item), price, self.name)
                                        # now we've bought it, lets reassign a value - change the value of the last item in the inventory (which has just been appended)
                                        map[x][y].shop.gain_experience(item_experience(
                                            item))  # add experience to the shop equivalent to the level of the item
                                        self.inventory[-1][5] = appraise_value(self.inventory[-1], self.faction,
                                                                               self.base_level)
                                        if item_type == 'weapon' or item_type == 'scroll':
                                            self.activitylog['history'].append(
                                                'I have bought a ' + item_type + ' from ' + map[x][y].faction + '.')
                                        else:
                                            self.activitylog['history'].append(
                                                'I have bought some ' + item_type + ' from ' + map[x][y].faction + '.')
                                        if libtcod.random_get_int(0, 0, 4) == 4:
                                            self.activitylog['history'].append(pick_random_from_list(event_item_bought))
                                        sales_metrics.log_item_sold(item_type, price, map[x][y].faction, day_count)
                                        break  # then leave the loop, so we only buy one thing at most

    def appraise_inventory(self):
        # go through all hero inventory, and assign a value (price) appropriately
        for n in range(len(self.inventory)):
            set_value = appraise_value(self.inventory[n], self.faction, self.base_level)
            self.inventory[n][5] = set_value

    def sell_items(self, type='all'):

        x = self.x
        y = self.y  # hero location

        for shops in shop_list:
            if x == shops[2]:
                if y == shops[3]:  # shop location found

                    no_items = len(self.inventory) - 1  # define the length of the hero inventory
                    if no_items > 0:  # only if the number of items is greater than 1 for now
                        if type == 'all':
                            chosen_item_index = libtcod.random_get_int(0, 0,
                                                                       no_items)  # select an item to sell (at the chosen price)
                            # hero_message('Chose ' + str(chosen_item_index) + ' of ' + str(no_items))
                            # player sale interface, the hero will offer us the item in a box similar to 'item interface'
                            if not map[x][y].shop == player:
                                hero_sale(x, y, map[x][y].shop, self,
                                          chosen_item_index)  # (x, y, buy_shop, sell_shop, index)
                                self.reputation.improve_reputation(map[x][y].faction)
                            elif accepting_offers:
                                hero_sale(x, y, map[x][y].shop, self, chosen_item_index)
                                self.reputation.improve_reputation(map[x][y].faction)
                            else:
                                pass
                        else:
                            if not map[x][y].shop == player:
                                for index, item in enumerate(self.inventory):
                                    if master_item_list[item[0]][9] == type:
                                        hero_sale(x, y, map[x][y].shop, self, index)
                                        self.reputation.improve_reputation(map[x][y].faction)
                                        break
                            elif accepting_offers:
                                for index, item in enumerate(self.inventory):
                                    if master_item_list[item[0]][9] == type:
                                        hero_sale(x, y, map[x][y].shop, self, index)
                                        self.reputation.improve_reputation(map[x][y].faction)
                                        break
                            else:
                                pass

    def dress_thineself(self):
        # should do this just as we enter a dungeon. Hero should try and keep one of each items on hand at all times ...

        item_list = []
        for index, item in enumerate(self.inventory):
            assessed_item_power = assess_item(item, self.faction,
                                              self.base_level)  # a measure of how good the hero thinks the item is
            item_list.append([assessed_item_power, item, index])  # throw them in a list, with the index

        sorted_item_list = sorted(item_list, reverse=True)
        # 0_index, 1_quality[real, known], 2_bonus[real,known], 3_effects[rl, kn], 4_realvalue, 5_marketvalue, 6_cursedstatus

        # can this be made generic, based on slots?
        # for slot in len(self.equipment) ... or some such dictionary fuckwaddery ... probably ...
        armor_power = 0
        weapon_power = 0
        clothing_power = 0

        for armor in sorted_item_list:
            if master_item_list[armor[1][0]][9] == 'armor':  # if the item is an armor ...
                armor_power = armor[0]
                if armor_power > self.stats['perceived_armor']:
                    armor_index = armor[2]
                    self.equipment['armor'] = armor[1]
                    self.inventory.remove(armor[1])

                    self.stats['perceived_armor'] = armor_power  # remember how good we think this is ...

                    # equip this armor, as better than existing (according to our hero)
                    break  # then leave the loop

        for weapon in sorted_item_list:
            if master_item_list[weapon[1][0]][9] == 'weapon':
                weapon_power = weapon[0]
                if weapon_power > self.stats['perceived_weapon']:
                    weapon_index = weapon[2]
                    self.equipment['weapon'] = weapon[1]
                    self.inventory.remove(weapon[1])

                    self.stats['perceived_weapon'] = weapon_power

                    # equip this weapon as the best type (according to our hero)
                    break  # then leave the loop

        for clothing in sorted_item_list:
            if master_item_list[clothing[1][0]][9] == 'clothing':
                clothing_power = clothing[0]  # perception only, related to assess_item() function
                if clothing_power > self.stats['perceived_clothing']:
                    clothing_index = clothing[2]
                    self.equipment['clothing'] = clothing[1]
                    self.inventory.remove(clothing[1])

                    self.stats['perceived_clothing'] = clothing_power

                    # equip this clothing, as the best type (according to our hero)
                    break  # then leave the loop

        # Now we want to decide how strong this has made us feel ...
        self.stats['perceived'] = self.base_level + self.stats['perceived_clothing'] + self.stats['perceived_weapon'] + \
                                  self.stats['perceived_armor']
        # add personality effects to this, in time ...


        # find real bonuses - real quality, real bonus, real level
        if self.equipment['clothing']:  # did we put anything on?
            clothing_bonus = self.equipment['clothing'][1][0] + self.equipment['clothing'][2][0] + \
                             master_item_list[self.equipment['clothing'][0]][3]
        else:
            clothing_bonus = 0

        if self.equipment['armor']:
            armor_bonus = self.equipment['armor'][1][0] + self.equipment['armor'][2][0] + \
                          master_item_list[self.equipment['armor'][0]][3]
        else:
            armor_bonus = 0

        if self.equipment['weapon']:
            weapon_bonus = self.equipment['weapon'][1][0] + self.equipment['weapon'][2][0] + \
                           master_item_list[self.equipment['weapon'][0]][3]
        else:
            weapon_bonus = 0

        stat_bonus = 0

        if 'warrior' in self.brain.personality.perk:
            stat_bonus = 2
        elif 'wimp' in self.brain.personality.perk:
            stat_bonus = -2

        self.stats['real'] = self.base_level + weapon_bonus + armor_bonus + clothing_bonus + stat_bonus

        if self.stats['real'] < 1:
            self.stats['real'] = 1

    def undress_thineself(self):
        # empty equipment slots, so that we are free to fuck about with our inventory (sell etc.) whilst in town.

        clothing = self.equipment['clothing']
        self.equipment['clothing'] = 0
        weapon = self.equipment['weapon']
        self.equipment['weapon'] = 0
        armor = self.equipment['armor']
        self.equipment['armor'] = 0

        if clothing:
            self.inventory.append(clothing)
        if weapon:
            self.inventory.append(weapon)
        if armor:
            self.inventory.append(armor)

        self.stats['perceived'] = self.base_level
        self.stats['perceived_armor'] = 0
        self.stats['perceived_clothing'] = 0
        self.stats['perceived_weapon'] = 0
        self.stats['real'] = self.base_level

    def demotivate(self):
        self.brain.personality.motivation = []

    def shops_by_distance(self):

        distance = []

        for shop in shop_list_inc_player:
            # distance_measure(here_x, here_y, there_x, there_y)
            distance_to_shop = distance_measure(self.x, self.y, shop[2], shop[3])
            distance.append([distance_to_shop, shop[1]])

        distances_in_order = sorted(distance)  # sort the distance to the shops
        distances_in_order.reverse()

        return distances_in_order  # returns a sorted list of distances, shop names

    def pick_closest_shop(self):

        distances_in_order = self.shops_by_distance()

        distances_in_order.pop()  # get rid of the closest one (it will be the one we are at)

        closest_shop_name = distances_in_order[0][1]

        return closest_shop_name

    def assess_contracts(self):

        acceptable_contracts = []

        if len(contract_list) > 0:
            for index, item in enumerate(contract_list):
                if not item['assigned']:
                    if self.value_contract(item):
                        acceptable_contracts.append(index)

        if len(acceptable_contracts) > 0:
            contract_index = pick_random_from_list(acceptable_contracts)
            return contract_index + 1  # don't want a returned value of zero to be misunderstood?
        else:
            return False

    def value_contract(self, contract):

        if log_information:
            log_info('Valuing contract')
            log_info(str(contract))

        perks = self.brain.personality.perk

        quirks = self.brain.personality.quirk

        base_value = contract_base_price  # base acceptable cost for a level 1 hero to venture in a level 1 dungeon, or attack a level 1 monster

        # ['dungeon', 'dungeon_name', 'item_fetch', COST, 'faction' ]
        # ['monster', 'monster_name', 'monster_hunt', COST, 'faction' ]

        asking_price = contract['asking_price']
        mission_type = contract['mission_type']
        target_name = contract['target_name']
        contract_type = contract['contract_type']
        asking_faction = contract['asking_faction']

        relations = self.reputation.by_faction[asking_faction]

        base_value -= relations  # subtract a positive relationship with the asking faction from the base cost

        if 'bravado' in perks:  # far keener to go and kick shit out of stuff for cash
            base_value -= contract_base_stat_modifier
        elif 'wimp' in perks:
            base_value += contract_base_stat_modifier

        if base_value < 10:  # minimum cost
            base_value = 10

        base_level = 0

        contract_void = 0

        if contract_type == 'dungeon':
            for dungeon in dungeon_list:
                if dungeon[1] == target_name:
                    dungeon_x = dungeon[2]
                    dungeon_y = dungeon[3]
                    base_level = map[dungeon_x][dungeon_y].dungeon.base_level
                    break
            if base_level:  # so we have found the dungeon, it still exists
                base_value *= base_level
            else:
                contract_list.remove(contract)  # the contract is no longer valid.
                message('A Hero has thrown away a void contract from the noticeboard.', libtcod.light_red,
                        libtcod.dark_red)
                contract_void = 1

        elif contract_type == 'monster':
            for monster in monster_list:
                if monster.name == target_name:
                    base_level = monster.base_level
                    break
            if base_level:  # so we found the monster
                base_value *= base_level
            else:
                contract_list.remove(contract)  # the contract is no longer valid (monster dead)
                message('A Hero has thrown away a void contract from the noticeboard.', libtcod.light_red,
                        libtcod.dark_red)
                contract_void = 1

        if not contract_void:
            if asking_price >= base_value:  # hero values this contract in the right region

                if log_information:
                    log_info('Contract acceptable at $' + str(
                        asking_price) + ' by ' + self.name + ' but would have taken $' + str(base_value))

                return True
            else:
                if log_information:
                    log_info(
                        'Contract not acceptable at $' + str(asking_price) + ' by ' + self.name + ', more like $' + str(
                            base_value))
                return False
        else:
            return False

    def tout(self, faction):  # marketing in its basest form. Yuck.

        self.reputation.worsen_reputation(faction, 2)
        self.move_to_new_shop(faction)
        self.activitylog['history'].append(pick_random_from_list(event_tout))

    def assess_my_condition(self):
        hp_float = float(self.hp['current'])
        maxhp_float = float(self.hp['max'])

        hero_condition = hp_float / maxhp_float

        return hero_condition

    def find_another_shop_social(self):
        shops = self.shops_by_distance()
        # shops.pop()

        shop_weights = {}

        for shop in shops:
            this_shop_location = find_shop(shop[1])
            x = this_shop_location[0]
            y = this_shop_location[1]

            faction = map[x][y].faction

            if shop[0] == 0:
                shop_weights[faction] = 4  # penalise the shop we are standing on, to open up movement a bit
            else:
                shop_weights[faction] = shop[
                    0]  # store the distances to the shops, for further weighting by additional factors.

            heroes_here = 0  # for each shop, count up the heroes present.
            for hero in town_heroes:
                if [hero.x, hero.y] == [x, y]:
                    heroes_here += 1

            shop_weights[faction] -= heroes_here  # weight by the number of heroes here

        if log_sales:
            log_sales_info(shop_weights)

        shop_list_weighted = []

        for key, value in shop_weights.iteritems():
            shop_list_weighted.append([value, key])

        shop_list_weighted.sort()
        # shop_list_weighted.reverse()

        return shop_list_weighted  # [ weighted_distance_factor, shop_faction ]

    def find_another_shop_item(self,
                               item_type='random'):  # returns a sorted list of shops, by faction, and 'weighted' distance.

        if item_type == 'random':
            type = libtcod.random_get_int(0, 0, 3)
            if type == 0:
                item_type = 'clothing'
            elif type == 1:
                item_type = 'weapon'
            elif type == 2:
                item_type = 'armor'
            elif type == 3:
                item_type = 'scroll'

        shops = self.shops_by_distance()

        # shops.pop() #get rid of the closest one - it should be where we are. If not, who cares.

        shop_weights = {}

        for shop in shops:
            this_shop_location = find_shop(shop[1])
            x = this_shop_location[0]
            y = this_shop_location[1]

            faction = map[x][y].faction

            if shop[0] == 0:
                shop_weights[faction] = 4  # penalise the shop we are standing on, to open up movement a bit
            else:
                shop_weights[faction] = shop[
                    0]  # store the distances to the shops, for further weighting by additional factors.

        if log_sales:
            log_sales_info(shop_weights)

        for shop in shop_count_by_item_type(item_type):
            x = shop[1]
            y = shop[2]
            faction = map[x][y].faction

            shop_weights[faction] -= shop[
                0]  # adjust distances by the number of items held by the shops of the type we are after

        if log_sales:
            log_sales_info(shop_weights)

        marketing = self.personality_based_marketing_decision()

        if marketing == 'social':  # heavily weights distance by activity
            sales_list = sales_metrics.return_sales_number()

            if log_sales:
                log_sales_info(sales_list)

            purchases_list = sales_metrics.return_purchases_number()

            if log_sales:
                log_sales_info(sales_list)
                log_sales_info(purchases_list)

            for shop in sales_list:
                faction = shop[1]
                sales_number = shop[0]

                shop_weights[faction] -= sales_number

            for shop in purchases_list:
                faction = shop[1]
                purchases_number = shop[0]

                shop_weights[faction] -= purchases_number

        elif marketing == 'balance':  # heavily weights distance by lack of activity
            sales_list = sales_metrics.return_sales_number()
            purchases_list = sales_metrics.return_purchases_number()

            if log_sales:
                log_sales_info(sales_list)
                log_sales_info(purchases_list)

            for shop in sales_list:
                faction = shop[1]
                sales_number = shop[0]

                shop_weights[faction] += sales_number

            for shop in purchases_list:
                faction = shop[1]
                purchases_number = shop[0]

                shop_weights[faction] += purchases_number

        elif marketing == 'loot':  # weights distance by items bought in
            purchases_list = sales_metrics.return_purchases_number()

            if log_sales:
                log_sales_info(purchases_list)

            for shop in purchases_list:
                faction = shop[1]
                purchases_number = shop[0]

                shop_weights[faction] -= purchases_number

        elif marketing == 'wealth':  # weights distance by value of items sold / bought
            sales_value = sales_metrics.return_sales_value()
            purchases_value = sales_metrics.return_purchases_value()

            if log_sales:
                log_sales_info(sales_value)

            sales_value.sort()
            purchases_value.sort()  # highest values at the end of the list

            ## NEEDS COMPLETING ## i.e. what weight for what value? value / 10 ... ? \/ \/

            for sale in sales_value:
                faction = sale[1]
                sale_val = sale[0] / 10

                shop_weights[faction] -= sale_val

            for purchase in purchases_value:
                faction = purchase[1]
                purchase_val = purchase[0] / 10

                shop_weights[faction] -= purchase_val

        shop_list_weighted = []

        for key, value in shop_weights.iteritems():
            shop_list_weighted.append([value, key])

        shop_list_weighted.sort()

        if log_sales:
            log_sales_info(shop_list_weighted)

        # shop_list_weighted.reverse()

        return shop_list_weighted  # [distance_weighted_by_needs, faction_of_shop_owner]

    def personality_based_marketing_decision(self):

        seeks_social = self.brain.personality.seeks_social
        seeks_balance = self.brain.personality.seeks_balance
        seeks_loot = self.brain.personality.seeks_loot
        seeks_wealth = self.brain.personality.seeks_wealth

        total_decision_weighting = seeks_social + seeks_balance + seeks_loot + seeks_wealth

        decision_weighting_score = libtcod.random_get_int(0, 0, total_decision_weighting)

        if decision_weighting_score < seeks_social:
            return 'social'
        elif decision_weighting_score < seeks_social + seeks_balance:
            return 'balance'
        elif decision_weighting_score < seeks_social + seeks_balance + seeks_loot:
            return 'loot'
        elif decision_weighting_score < seeks_social + seeks_balance + seeks_loot + seeks_wealth:
            return 'wealth'
        else:
            return 'social'  # for edge cases

    def determine_phase_of_operations(self):  # used for a hero with zero decisions
        # function to determine if a) we have just arrived in to town b) we have just finished a goal c) something else
        # Phase 1: Arrive in to town. Make a list of things we need to do before we take a job.
        # Phase 2: Find some work
        # Phase 3: Carry Out Work
        # Phase 4: Tie up after work which may have been successful or unsuccessful.
        # Phase 5: Leave town.

        # Phase 2 or 4 may follow Phase 3.
        random_chance = libtcod.random_get_int(0, 0, 100)

        if len(self.brain.flags) == 0:  # we have a blank slate ...
            return 'Phase_1'
        elif 'mission_failed' in self.brain.flags:
            if random_chance < 80:
                return 'Phase_5'
            else:
                return 'Phase_2'
        elif 'mission_complete' in self.brain.flags:
            if random_chance < 40:
                return 'Phase_5'
            else:
                return 'Phase_2'

    def hero_make_a_fucking_decision(self):  # polled if hero passes an action check.

        outstanding_things_to_do = len(self.brain.decisions)
        this_phase = self.brain.phase

        if this_phase == 'Phase_1':

            if not outstanding_things_to_do:
                if self.prepare_yourself():
                    self.populate_action_list()
            else:
                self.action_your_decision()

        elif this_phase == 'Phase_2':

            if not outstanding_things_to_do:
                master_plan = self.brain.personality.return_decision_personality()

                task = self.check_noticeboard(master_plan)
                if task:
                    if self.seek_contract_acceptance(task):
                        self.populate_action_list()  # generate a list of actions based on the contract received
                else:
                    task = self.self_motivate(master_plan)
                    if task:
                        self.brain.contract = task
                        self.populate_action_list()
                    else:
                        pass
            else:
                self.action_your_decision()

        elif this_phase == 'Phase_3':
            if not outstanding_things_to_do:
                self.leave_town()
            else:
                self.action_your_decision()

    def resolve_contract(self):
        global the_mayoress

        contract = self.brain.contract

        asking_price = contract.asking_price
        paid = contract.paid
        asking_faction = contract.asking_faction
        mission_type = contract.mission_type
        contract_type = contract.contract_type

        if asking_price:  # there is coin to collect, if not it could be a self motivated contract or otherwise.
            if not paid:  # and I haven't been paid, yet
                ## go to shop (or not in mayoress' case)
                if asking_faction == 'Mayoress':
                    if the_mayoress.wealth >= asking_price:
                        the_mayoress.wealth -= asking_price
                        self.wealth += asking_price
                    else:
                        self.brain.phase = 'Phase_3'  # storm off in a huff
                else:
                    [x, y] = find_shop_by_faction(asking_faction)
                    [self.x, self.y] = [x, y]

                    if mission_type == 'item_hunt':
                        if len(self.activitylog['contract_cargo']) > 0:
                            if map[x][y].shop.wealth >= asking_price:
                                map[x][y].shop.wealth -= asking_price
                                for item in self.activitylog['contract_cargo']:
                                    map[x][y].shop.inventory.append(item)
                                if asking_faction == player_name:
                                    message(self.name + ' returns with loot!', libtcod.light_yellow,
                                            libtcod.dark_yellow)
                            else:
                                for item in self.activitylog['contract_cargo']:
                                    self.inventory.append(item)
                                    self.reputation.worsen_reputation(
                                        asking_faction)  # not that bothered ... they get to keep the item ...
                        else:
                            if asking_faction == player_name:
                                message(self.name + ' has failed to find an item!', libtcod.light_red, libtcod.dark_red)
                    else:
                        if map[x][y].shop.wealth >= asking_price:
                            map[x][y].shop.wealth -= asking_price
                            self.wealth += asking_price

                            self.reputation.improve_reputation(asking_faction)

                            if asking_faction == player_name:
                                log_purchase('CONTRACT', asking_price, self.name)

                            if mission_type == 'item_hunt':
                                if len(self.activitylog['contract_cargo']) > 0:
                                    for item in self.activitylog['contract_cargo']:
                                        map[x][y].shop.inventory.append(item)
                        else:
                            self.brain.phase = 'Phase_3'  # storm off in a huff
            else:
                ##already been paid, but might still need to meet other obligations e.g. item hunts? not yet ...
                pass  # let's just clear the contracts then ...

        try:  # whatever the result of the above, we should wrap things up and move on.
            the_mayoress.noticeboard.notices.remove(
                self.brain.contract)  # may not have ever appeared here if self-motivated
        except:
            pass  # might want to put in something about self-fulfilment here

        self.brain.contract = 0

    def populate_action_list(self):  # function that tells us what to do, based on a chosen contract

        task = self.brain.contract

        mission_type = task.mission_type
        contract_type = task.contract_type
        asking_price = task.asking_price

        if debug_mode:
            message(self.name + ' POPULATE ACTIONS for: ' + str(mission_type) + ',' + str(contract_type) + ',' + str(
                asking_price), libtcod.light_grey, libtcod.light_grey)

        self.brain.decisions.append(
            'resolve_contract')  # every new contract has to end with the resolution of it afterwards.

        if contract_type == 'dungeon':
            danger = self.measure_danger(task)
            perceived_power = self.stats['perceived']

            if debug_mode:
                message(self.name + 'DELVING; PCVD PWR:' + str(self.stats['perceived']) + ', RL PWR:' + str(
                    self.stats['real']) + ' DNGR:' + str(danger), libtcod.light_grey, libtcod.light_grey)

            if mission_type == 'default':
                danger_vs_power = ((perceived_power) - danger)

                if debug_mode:
                    message(' FEELING THIS CONFIDENT: ' + str(danger_vs_power), libtcod.light_grey, libtcod.light_grey)

                if danger_vs_power < 1:
                    danger_vs_power = 1

                self.brain.decisions.append('go_home')

                self.brain.decisions.append('explore')

                for n in range(danger_vs_power):
                    self.brain.decisions.append('descend')

            elif mission_type == 'item_hunt':
                danger_vs_power = ((perceived_power) - danger)

                if danger_vs_power < 1:
                    danger_vs_power = 1

                if debug_mode:
                    message(' FEELING THIS CONFIDENT: ' + str(danger_vs_power), libtcod.light_grey, libtcod.light_grey)

                self.brain.decisions.append('go_home')

                self.brain.decisions.append('find_item')

                for n in range(danger_vs_power):
                    self.brain.decisions.append('descend')

        elif contract_type == 'town':

            if mission_type == 'buy':  # target name determines item type
                self.brain.decisions.append('buy')
                self.brain.decisions.append('move_shop')

            elif mission_type == 'sell':  # target_name determines item type
                self.brain.decisions.append('sell')
                self.brain.decisions.append('move_shop')

            elif mission_type == 'socialise':
                self.brain.decisions.append('socialise')
                self.brain.decisions.append('move_shop')

            elif mission_type == 'rest':
                self.brain.decisions.append('rest')
                self.brain.decisions.append('go_home')

            elif mission_type == 'raise_dead':
                self.brain.decisions.append('go_home')
                if 'healer' in self.brain.personality.perk:  # need to ensure entry point is limited to heroes with healer or defiler only
                    self.brain.decisions.append('raise_dead')
                elif 'defiler' in self.brain.personality.perk:
                    self.brain.decisions.append('defile_corpse')
                self.brain.decisions.append('find_corpse')

        elif contract_type == 'monster':
            if mission_type == 'monster_hunt':
                self.brain.decisions.append('duel')
                self.brain.decisions.append('move_to_monster')

    def action_your_decision(self):
        x = self.x
        y = self.y

        if len(self.brain.decisions) > 0:
            action = self.brain.decisions[-1]
        else:
            action = False

        if action:
            if not self.in_dungeon:  # WE ARE IN TOWN!!!
                if action == 'move_to_monster':  # is this redundant? You cannae duel without finding a monster? Entry action might be useful, though ...
                    if self.move_to_monster(self.brain.contract.target_name):
                        self.brain.decisions.pop(-1)
                    else:
                        self.brain.decisions.pop(-1)
                        # monster not found ...

                elif action == 'duel':  # fight to the death with the monster ...
                    if self.move_to_monster(
                            self.brain.contract.target_name):  # code allows for the possibility of monster moving, or a break in the duel process
                        for monster in monster_list:
                            if [self.x, self.y] == [monster.x, monster.y]:
                                adversary = monster
                                break
                        self.duel(adversary)
                    else:
                        self.brain.decisions.remove('duel')  # should empty the brain of the last decision ...

                elif action == 'buy_cargo':
                    if libtcod.random_get_int(0, 0, 1) == 1:  # 50 / 50 whether we find somewhere else ...
                        shops = self.find_another_shop_item()
                        self.move_to_new_shop(
                            shops[0][1])  # move to shop, by faction, of 'nearest' (or most attractive) shop.
                    if map[x][y].shop:
                        self.browse_stock()  # need a better function to assess whether the item is better than the one we hold?
                    self.brain.decisions.pop(-1)
                elif action == 'sell_cargo':
                    if libtcod.random_get_int(0, 0, 1) == 1:  # 50 / 50 whether we find somewhere else ...
                        shops = self.find_another_shop_item()
                        self.move_to_new_shop(
                            shops[0][1])  # move to shop, by faction, of 'nearest' (or most attractive) shop.
                    if map[x][y].shop:
                        self.sell_items()
                    self.brain.decisions.pop(-1)
                elif action == 'go_home':
                    self.go_home()
                    self.brain.decisions.remove('go_home')

                elif action == 'rest':
                    if self.hp['current'] < self.hp['max']:
                        self.rest()
                    else:
                        self.brain.decisions.remove('rest')  # should empty us?

                elif action == 'move_shop':
                    if self.brain.contract.mission_type == 'buy':
                        shops = self.find_another_shop_item(self.brain.contract.target_name)
                    elif self.brain.contract.mission_type == 'sell':
                        shops = self.find_another_shop_item(self.brain.contract.target_name)
                    else:
                        shops = self.find_another_shop_social()

                    if [self.brain.contract.mission_type, shops[0][1]] == ['buy', 'Merchants']:
                        self.move_to_new_shop(
                            shops[1][1])  # second 'nearest' shop because we can't buy at the merchants house
                    else:
                        self.move_to_new_shop(
                            shops[0][1])  # move to shop, by faction, of 'nearest' (or most attractive) shop.
                    self.brain.decisions.pop(-1)  # empty this action from the list of decisions


                elif action == 'socialise':

                    heroes_here = []

                    for hero in town_heroes:
                        if hero != self:
                            if [hero.x, hero.y] == [self.x, self.y]:
                                heroes_here.append(hero)

                    if heroes_here:
                        hero_chat = pick_random_from_list(heroes_here)

                        log_or_not = libtcod.random_get_int(0, 0, 4)

                        if log_or_not == 1:
                            self.activitylog['history'].append(
                                pick_random_from_list(event_chat_with_pre) + hero_chat.name)
                        elif log_or_not == 2:
                            self.activitylog['history'].append(
                                hero_chat.name + pick_random_from_list(event_chat_with_post))
                        else:
                            pass
                        self.brain.decisions.pop(-1)

                    else:  # no one around ... lets wait for someone to come?
                        if 'dead_around_here' in self.brain.flags:
                            self.brain.decisions.append('move_shop')  # fuck it lets try somewhere else
                            self.brain.flags.remove('dead_around_here')
                            self.brain.flags.remove('quiet_around_here')

                        elif 'quiet_around_here' in self.brain.flags:
                            self.brain.flags.append('dead_around_here')
                        else:
                            self.brain.flags.append('quiet_around_here')

                elif action == 'buy':
                    if map[x][y].shop:
                        self.browse_stock(self.brain.contract.target_name)
                            # need a better function to assess whether the item is better than the one we hold?
                    self.brain.decisions.pop(-1)
                elif action == 'sell':
                    if map[x][y].shop:
                        self.sell_items(self.brain.contract.target_name)
                    self.brain.decisions.pop(-1)
                elif action == 'descend':
                    self.move_to_dungeon(self.brain.contract.target_name)
                    self.brain.decisions.pop(-1)

                elif action == 'resolve_contract':
                    self.resolve_contract()
                    self.brain.decisions.pop(-1)

                elif action == 'raise_dead':
                    if 'healer' in self.brain.personality.perk:
                        for corpse in dead_heroes:
                            hero = corpse[0]
                            if [self.x, self.y] == [hero.x, hero.y]:  # check if there is a hero here
                                if corpse[1] < hero_rot_time:  # the corpse is still there
                                    hero.hp['current'] = hero.hp[
                                        'max']  # ressurect! To max points, otherwise they just die again ...
                                    dead_heroes.remove(corpse)
                                    town_heroes.append(corpse[0])
                                    self.gain_experience(10)
                                    self.activitylog['history'].append(
                                        'I have restored the life force to a soul in need.')
                                    self.brain.decisions.pop(-1)

                                    hero_message(str(self.name) + ' has raised ' + str(hero.name) + '!',
                                                 libtcod.light_yellow, libtcod.dark_yellow)
                                    if hero.faction == 'Necromancers':
                                        hero.activitylog['history'].append(
                                            self.name + ' has brought me back from death.')
                                    else:
                                        hero.activitylog['history'].append(self.name + ' has given me back life!')

                elif action == 'defile_corpse':
                    if 'defiler' in self.brain.personality.perk:
                        for corpse in dead_heroes:
                            hero = corpse[0]
                            if [self.x, self.y] == [hero.x, hero.y]:
                                if corpse[1] < hero_rot_time:  # the corpse is still there
                                    dead_heroes.remove(corpse)
                                    hero_message(hero.name + ' is defiled!', libtcod.light_red, libtcod.dark_red)

                                    self.activitylog['history'].append(
                                        'I have gained power from the corpse of another.')
                                    self.gain_experience(10)
                                    self.brain.decisions.pop(-1)

                                    gender_test = libtcod.random_get_int(0, 0, 1)  # now make a replacement ...
                                    if gender_test == 0:
                                        gender = 'm'
                                    else:
                                        gender = 'f'

                                    birth_hero(gender)
                                    hero_message(hero_list[-1].name + ' takes up the fight!', libtcod.light_yellow,
                                                 libtcod.dark_yellow)

                elif action == 'find_corpse':
                    corpse_location = self.find_corpse(self.brain.contract.target_name)
                    if debug_mode:
                        message('Trying to find CORPSE: X - ' + str(corpse_location[0]) + ', Y - ' + str(
                            corpse_location[1]), libtcod.light_grey, libtcod.light_grey)
                    if corpse_location[2]:  # hero in a dungeon
                        for n in range(corpse_location[2]):
                            # #AAARGH WHAT ABOUT KNOWING WHICH DUNGEON TO GO TO? SHALL WE CHANGE IT HERE?

                            self.brain.decisions.append('descend')
                        self.brain.contract.target_name = map[corpse_location[0]][
                            corpse_location[1]].name  # reassign target name from corpse, to dungeon
                    else:  # hero on the overworld
                        self.move_to_map_location(corpse_location[0], corpse_location[1])
                    self.brain.decisions.pop(-1)
                elif action in dungeon_tasks:  # shouldn't be here - but might be a holdover from something unexpected happening
                    self.brain.decisions.pop(-1)  # just get rid of it

            elif self.in_dungeon:

                if self.assess_my_condition() < 0.5:
                    self.stop_descending()

                random_event = libtcod.random_get_int(0, 0, 100)
                dlev = map[self.x][self.y].dungeon.base_level

                if action == 'descend':  # take on an aggressive manner
                    if random_event < 25:
                        self.dungeon_descend()
                        self.brain.decisions.remove('descend')
                    elif random_event < 50:
                        self.brain.decisions.append('fight')  # violence begets violence
                        self.fight(generate_encounter(1, dlev, 1, dlev + (self.in_dungeon / 3)))
                    elif random_event < 96:
                        self.misc_monologue()
                    elif random_event < 99:
                        self.find_item()
                    else:
                        self.explore_floor()

                elif action == 'explore':
                    if random_event < 15:
                        self.explore_floor()
                        self.brain.decisions.pop(-1)
                    elif random_event < 30:
                        if 'sneaky' in self.brain.personality.perk:
                            self.gain_experience(3)
                            self.activitylog['history'].append(pick_random_from_list(event_sneak_fight))
                        else:
                            self.brain.decisions.append('fight')  # stumble in to a possible encounter
                    elif random_event < 40:
                        self.brain.decisions.append('fight')  # possible encounter
                    elif random_event < 50:
                        self.brain.decisions.append('fight')  # serial scrapper
                        self.fight(generate_encounter(1, dlev, 1, dlev + (self.in_dungeon / 3)))
                    elif random_event < 90:
                        self.misc_monologue()
                    else:
                        self.find_item()

                elif action == 'fight':  # violence begets violence
                    if random_event < 30:
                        self.fight(generate_encounter(1, dlev, 1, dlev + (self.in_dungeon / 3)))
                    if random_event < 50:
                        if 'sneaky' in self.brain.personality.perk:  # chance for sneaky heroes to avoid
                            self.brain.decisions.remove('fight')
                            self.activitylog['history'].append(pick_random_from_list(event_sneak_fight))
                            self.gain_experience(3)
                        else:
                            self.fight(generate_encounter(1, dlev, 1, dlev + (self.in_dungeon / 3)))
                    else:
                        self.brain.decisions.remove('fight')

                elif action == 'trap':
                    if random_event < 25:
                        self.brain.decisions.pop(-1)
                        self.activitylog['history'].append(pick_random_from_list(event_trap))
                        self.activate_trap()
                    elif random_event < 50:
                        if 'agile' in self.brain.personality.perk or 'sneaky' in self.brain.personality.perk:
                            self.gain_experience(3)
                            self.activitylog['history'].append(pick_random_from_list(event_avoid_trap))
                            self.brain.decisions.pop(-1)
                        else:
                            self.brain.decisions.pop(-1)
                            self.activitylog['history'].append(pick_random_from_list(event_trap))
                            self.activate_trap()
                    else:
                        self.activitylog['history'].append(pick_random_from_list(event_avoid_trap))
                        self.brain.decisions.pop(-1)

                elif action == 'treasure_room':  # shall we only let sneaky characters in?
                    if 'sneaky' in self.brain.personality.perk:
                        self.brain.decisions.pop(-1)
                        self.activitylog['history'].append(pick_random_from_list(event_know_treasure_room))
                        if random_event < 50:
                            self.activitylog['history'].append(pick_random_from_list(event_failed_entry))
                        else:
                            self.activitylog['history'].append(pick_random_from_list(event_gain_entry))
                            for n in range(libtcod.random_get_int(0, 1, 3)):
                                self.find_item()
                            take_dungeon_coin(libtcod.random_get_int(0, 0, 100))
                    else:
                        self.brain.decisions.pop(-1)
                        self.activitylog['history'].append(pick_random_from_list(event_bemused_treasure_room))

                elif action == 'secret_room':
                    pass

                elif action == 'trap_door':
                    if random_event < 25:
                        if 'descend' in self.brain.decisions:
                            self.brain.decisions.remove('descend')
                        self.brain.decisions.pop(-1)
                        self.in_dungeon += 1
                        self.activitylog['history'].append(pick_random_from_list(event_trapdoor))
                        self.activate_trap()
                    elif random_event < 50:
                        if 'agile' in self.brain.personality.perk:
                            self.gain_experience(3)
                            self.activitylog['history'].append(pick_random_from_list(event_avoid_trapdoor))
                            self.brain.decisions.pop(-1)
                        else:
                            if 'descend' in self.brain.decisions:
                                self.brain.decisions.remove('descend')
                            self.brain.decisions.pop(-1)
                            self.in_dungeon += 1
                            self.activitylog['history'].append(pick_random_from_list(event_trapdoor))
                            self.activate_trap()
                    else:
                        self.activitylog['history'].append(pick_random_from_list(event_avoid_trapdoor))
                        self.brain.decisions.pop(-1)

                elif action == 'lair':
                    jabber_chance = libtcod.random_get_int(0, 0, 100)

                    if jabber_chance < self.brain.personality.verbosity:
                        self.activitylog['history'].append(pick_random_from_list(event_lair))

                    no_encounters = libtcod.random_get_int(0, 1, 4)

                    for n in range(no_encounters):
                        self.brain.decisions.append('fight')

                elif action == 'graveyard':
                    self.activitylog['history'].append(pick_random_from_list(event_graveyard))
                    if self.faction == 'Necromancers':
                        self.gain_experience(5)
                    else:
                        self.brain.decisions.append('fight')

                elif action == 'puzzle':
                    jabber_chance = libtcod.random_get_int(0, 0, 100)

                    if jabber_chance < self.brain.personality.verbosity:
                        self.activitylog['history'].append(pick_random_from_list(event_puzzle))

                    if random_event < 25:
                        self.brain.decisions.pop(-1)
                    if random_event < 45:
                        if 'quick_witted' in self.brain.personality.perk:
                            self.brain.decisions.pop(-1)
                            self.gain_experience(3)
                        else:
                            pass
                    if random_event < 90:
                        pass
                    else:
                        self.brain.decisions.append('puzzle')  # deeper in to the mire ...

                elif action == 'cursed_altar':  # one for the demon worshippers amongst us
                    if 'demon_worship' in self.brain.personality.perk:
                        self.gain_experience(35)
                        self.activitylog['history'].append('I have found a shrine to evil!')
                        items_cursed = self.check_cursed('cursed')
                        if items_cursed:
                            self.activitylog['history'].append('My Gods take my offering!')
                            for each_item in items_cursed:
                                item = each_item[0]
                                location = each_item[1]
                                if location == 'inventory':
                                    self.inventory.remove(item)
                                elif location == 'armor' or location == 'clothing' or location == 'weapon':
                                    self.equipment[location] = 0
                                elif location == 'contract':
                                    self.activitylog['contract_cargo'].remove(item)
                                item_level = master_item_list[item[0]][3]
                                item_enchant = item[2][0]
                                item_quality = item[1][0]
                                self.gain_experience(item_level + item_enchant + item_quality)
                    else:
                        self.activitylog['history'].append('I have found a monument to evil!')
                    self.brain.decisions.pop(-1)

                elif action == 'find_item':  # take on an exploratory role
                    if random_event < 10:
                        self.find_item()  # additional (quite large) chance to find item
                    elif random_event < 35:
                        self.fight(generate_encounter(1, dlev, 1, dlev + (self.in_dungeon / 3)))
                    elif random_event < 95:
                        pass
                    else:
                        self.explore_floor()

                elif action == 'go_home':  # defensive, let's get outta here!
                    if random_event < 25:
                        self.leave_dungeon()
                    elif random_event < 35:
                        self.fight(generate_encounter(1, dlev, 1, dlev + (self.in_dungeon / 3)))
                    else:
                        pass

                elif action == 'raise_dead':
                    if 'healer' in self.brain.personality.perk:
                        for corpse in dead_heroes:
                            hero = corpse[0]
                            if [self.x, self.y, self.in_dungeon] == [hero.x, hero.y,
                                                                     hero.in_dungeon]:  # check if there is a hero here
                                if corpse[1] < hero_rot_time:  # the corpse is still there
                                    hero.hp['current'] = hero.hp[
                                        'max']  # ressurect! To max points, otherwise they just die again ...
                                    dead_heroes.remove(corpse)
                                    town_heroes.append(corpse[0])
                                    self.gain_experience(10)
                                    self.activitylog['history'].append(
                                        'I have restored the life force to a soul in need.')

                                    hero_message(str(self.name) + ' has raised ' + str(hero.name) + '!',
                                                 libtcod.light_yellow, libtcod.dark_yellow)
                                    if hero.faction == 'Necromancers':
                                        hero.activitylog['history'].append(
                                            self.name + ' has brought me back from death.')
                                    else:
                                        hero.activitylog['history'].append(self.name + ' has given me back life!')
                    self.brain.decisions.pop(-1)

                elif action == 'defile_corpse':
                    if 'defiler' in self.brain.personality.perk:
                        for corpse in dead_heroes:
                            hero = corpse[0]
                            if [self.x, self.y, self.in_dungeon] == [hero.x, hero.y, hero.in_dungeon]:
                                if corpse[1] < hero_rot_time:  # the corpse is still there
                                    dead_heroes.remove(corpse)
                                    hero_message(hero.name + ' is defiled!', libtcod.light_red, libtcod.dark_red)

                                    self.activitylog['history'].append(
                                        'I have gained power from the corpse of another.')
                                    self.gain_experience(10)

                                    gender_test = libtcod.random_get_int(0, 0, 1)  # now make a replacement ...
                                    if gender_test == 0:
                                        gender = 'm'
                                    else:
                                        gender = 'f'

                                    birth_hero(gender)
                                    hero_message(hero_list[-1].name + ' takes up the fight!', libtcod.light_yellow,
                                                 libtcod.dark_yellow)
                    self.brain.decisions.pop(-1)

    def take_dungeon_coin(self, coin_treasure):

        if map[self.x][self.y].dungeon:
            if map[self.x][self.y].dungeon.wealth > 0:
                map[self.x][self.y].dungeon.wealth -= coin_treasure
                self.wealth += coin_treasure
                if map[self.x][self.y].dungeon.wealth < 0:
                    map[self.x][self.y].dungeon.wealth = 0
            else:
                pass  # we've bled the dungeon dry ...

    def activate_trap(self):

        if self.hp['current'] > 1:
            self.hp['current'] -= 1

    def check_cursed(self, status):
                     # returns a list of heroes equipment, and whether this is cursed / blessed / uncursed (by request)

        curse_items = []

        for items in self.inventory:
            if items[6] == status:
                curse_items.append([items, 'inventory'])

        if self.equipment['armor'][6] == status:
            curse_items.append([self.equipment['armor'], 'armor'])
        if self.equipment['weapon'][6] == status:
            curse_items.append([self.equipment['weapon'], 'weapon'])
        if self.equipment['clothing'][6] == status:
            curse_items.append([self.equipment['clothing'], 'clothing'])

        for items in self.activitylog['contract_cargo']:
            if items[6] == status:
                curse_items.append([items, 'contract'])

        if len(curse_items) > 0:
            return curse_items
        else:
            return False

    def explore_floor(self):
        x = self.x
        y = self.y
        dungeon_level = self.in_dungeon

        try:
            local_feature = map[self.x][self.y].dungeon.layout[self.in_dungeon]  # has a local feature been assigned?
        except:
            local_feature = floor_feature(map[self.x][self.y].dungeon.dungeon_type)  # if not create one ...
            map[self.x][self.y].dungeon.layout[self.in_dungeon] = local_feature  # and store it for other heroes to find

        if local_feature == 'mundane':
            pass
        elif local_feature == 'treasure_room':
            self.brain.decisions.append('treasure_room')
            rumour_length = 30  # days
            the_mayoress.noticeboard.rumours.append(
                Rumour(map[x][y].name, dungeon_level, 'treasure_room', rumour_length))
        elif local_feature == 'cursed_altar':
            self.brain.decisions.append('cursed_altar')
            rumour_length = 10  # days
            the_mayoress.noticeboard.rumours.append(
                Rumour(map[x][y].name, dungeon_level, 'cursed_altar', rumour_length))
        elif local_feature == 'lair':
            self.brain.decisions.append('lair')
            rumour_length = 20  # days
            the_mayoress.noticeboard.rumours.append(Rumour(map[x][y].name, dungeon_level, 'lair', rumour_length))
        else:
            self.brain.decisions.append(local_feature)

    def find_corpse(self, target_name):
        for corpse in dead_heroes:
            hero = corpse[0]
            if hero.name == target_name:
                [x, y, dungeon_level] = [hero.x, hero.y, hero.in_dungeon]
                return [x, y, dungeon_level]
                break
        return False

    def move_to_map_location(self, x, y):
        [self.x, self.y] = [x, y]

    def return_item_types_in_inventory(self):
        inventory = self.inventory

        if len(inventory) > 0:
            chuck_bass = []
            for item in inventory:
                item_type = master_item_list[item[0]][9]
                chuck_bass.append(item_type)
            return chuck_bass
        else:
            return False

    def self_motivate(self, motive):
        # #NEEDS A BIT MORE CREATIVE THOUGHT ON ADDITIONAL CONTRACTS ETC. PLUS PETITIONS
        x = self.x
        y = self.y

        dice_roll = libtcod.random_get_int(0, 0, 100)

        if motive == 'wealth':
            if dice_roll < 65:
                item_types_held = self.return_item_types_in_inventory()
                if item_types_held:
                    new_contract = Contract(0, 'sell', pick_random_from_list(item_types_held), 'town', self.faction, [],
                                            False, True, True)
                    return new_contract
                else:
                    return False
            else:
                self.brain.phase = 'Phase_3'  # let us leave town
                return False
        elif motive == 'social':
            the_mayoress.stay_a_while_and_listen()  # get the town to generate a socially motivated contract
            return False
        elif motive == 'knowledge':
            if dice_roll < 65:
                new_contract = Contract(0, 'buy', 'scroll', 'town', self.faction, [], False, True, True)
                return new_contract
            else:
                self.brain.phase = 'Phase_3'
                return False
        elif motive == 'contracts':  # not impressed with surfeit of jobs
            if dice_roll < 65:  # hang about for a bit, but do naught else
                return False
            else:
                self.brain.phase = 'Phase_3'
                return False
        elif motive == 'loot':
            if map[x][y].shop:
                if dice_roll < 75:
                    # take some positive action.
                    quest_type = libtcod.random_get_int(0, 0, 100)

                    x = self.x
                    y = self.y

                    dungeon_name = pick_random_from_list(dungeon_list)[1]  # pick a random dungeon ...

                    if map[x][y].shop != player:
                        message(self.name + ' is petitioning ' + map[x][y].faction + ' to bring forth quests!',
                                libtcod.chartreuse, libtcod.dark_chartreuse)

                    if quest_type < 25:
                        # petition the local faction to commission a dungeon delve.
                        if map[x][y].shop != player:  # can't petition the player ...
                            if map[x][y].shop.wealth > 150:  # only if the shop is a bit flush ...
                                map[x][y].shop.delve_dungeon(dungeon_name)
                    else:
                        if map[x][y].shop.wealth > 150:
                            map[x][y].shop.fetch_me_an_item(dungeon_name)

                    return False
                else:
                    self.brain.phase = 'Phase_3'  # let us leave town
                    return False

        elif motive == 'glory':
            if dice_roll < 65:  # hang about for a bit, but do naught else
                return False
            else:
                self.brain.phase = 'Phase_3'  # not impressed with the lack of opportunity here
                return False
        elif motive == 'leadership':
            if map[x][y].shop:
                if dice_roll < 55:
                    # take some positive action.
                    quest_type = libtcod.random_get_int(0, 0, 100)

                    x = self.x
                    y = self.y

                    dungeon_name = pick_random_from_list(dungeon_list)[1]  # pick a random dungeon ...

                    if map[x][y].shop != player:
                        message(self.name + ' is petitioning ' + map[x][y].faction + ' to bring forth quests!',
                                libtcod.chartreuse, libtcod.dark_chartreuse)

                    if quest_type < 70:
                        # petition the local faction to commission a dungeon delve.
                        if map[x][y].shop != player:  # can't petition the player ...
                            if map[x][y].shop.wealth > 150:  # only if the shop is a bit flush ...
                                map[x][y].shop.delve_dungeon(dungeon_name)
                    else:
                        if map[x][y].shop.wealth > 150:
                            map[x][y].shop.fetch_me_an_item(dungeon_name)

                    return False

            elif dice_roll < 80:  # hang about for a bit, but do naught else
                return False
            else:
                self.brain.phase = 'Phase_3'  # not impressed with the lack of opportunity here
                return False
                # petition your shop to raise a contract on your behalf - check personality again?
        elif motive == 'balance':
            if dice_roll < 85:  # hang about for a bit, but do naught else
                return False
            else:
                self.brain.phase = 'Phase_3'
                return False  # who knows? Chill out in the woods

    def check_noticeboard(self, motive):

        noticeboard = the_mayoress.noticeboard.notices

        considered_tasks = []

        for task in noticeboard:
            if motive in task.defining_motive:
                if not task.accepted:
                    considered_tasks.append(task)

        if len(considered_tasks) == 0:
            return False

        tasks_sorted = []

        for task in considered_tasks:
            # now assess which is the most preferable
            # need to measure danger level
            danger = self.measure_danger(task)
            price = task.asking_price

            if 'bravado' in self.brain.personality.perk:
                danger -= 2

            if 'wimp' in self.brain.personality.perk:
                danger += 2

            if danger < 0:
                danger = 0

            price -= danger
            # modify the price so that more dangerous tasks appear below equivalently priced tasks in priority terms

            tasks_sorted.append([price, danger, task])

        tasks_sorted.sort()
        tasks_sorted.reverse()

        danger_level_accepted = self.stats['perceived']

        for task in tasks_sorted:
            if danger_level_accepted > task[1]:
                return task[2]

        if 'strike_two' in self.brain.flags:
            self.brain.flags.append('strike_three')
        elif 'strike_one' in self.brain.flags:
            self.brain.flags.append('strike_two')
        else:
            self.brain.flags.append('strike_one')

        return False

    def measure_danger(self, task):
        # task(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive)
        danger_level = 0

        if task.mission_type == 'item_hunt':
            danger_level += 2
        else:
            pass

        name = task.target_name

        ##level = dungeon_spawn[0]
        ##name = dungeon_spawn[1]
        ##x = dungeon_spawn[2]
        ##y = dungeon_spawn[3]\\

        if task.contract_type == 'dungeon':
            danger_level += 4
            for dungeon in dungeon_list:
                if name == dungeon[1]:
                    x = dungeon[2]
                    y = dungeon[3]
                    break
            danger_level += map[x][y].dungeon.base_level * 4

        elif task.contract_type == 'monster':
            danger_level += 4
            for monster in monster_list:
                if monster.name == name:
                    danger_level += monster.base_level * 5
                    break
        # alternative contract types required

        sweetener = task.asking_price / 5

        danger_level -= sweetener

        # ~ if 'strike_three' in self.brain.flags:
        # ~ danger_level -= 15
        # ~ elif 'strike_two' in self.brain.flags:
        # ~ danger_level -= 10
        # ~ elif 'strike_one' in self.brain.flags: #ignored an available mission, getting more likely to accept something next time
        # ~ danger_level -= 5

        ##example: Level 1 dungeon crawl: 10 + 10 + 0 = 20.
        ##example: Level 2 dungeon crawl: 10 + 20 + 0 = 30.

        ##Hero will accept perceived power * 4. So hero level1 with lvl2 + lvl1 + lvl1 items will be happy to delve a basic dungeon.

        ##Hero level 2 - well equipped with (lvl2 + lvl3 + lvl2) * 4 = 36.

        return danger_level

    def determine_prepared(self):
        self.dress_thineself()

        weapon = False
        armor = False
        clothing = False

        if self.equipment['weapon']:
            weapon = True

        if self.equipment['armor']:
            armor = True

        if self.equipment['clothing']:
            clothing = True

        has_equipment = {'clothing': clothing, 'weapon': weapon, 'armor': armor}  # true or false for each type of item

        return has_equipment

    def prepare_yourself(self):

        has_equipment = self.determine_prepared()

        if [has_equipment['clothing'], has_equipment['armor'], has_equipment['weapon']] == [True, True, True]:
            self.brain.phase = 'Phase_2'
            return False

        if not has_equipment['clothing']:
            new_contract = Contract(0, 'buy', 'clothing', 'town', self.faction, [], False, True, True)
            self.brain.contract = new_contract
            return True
        elif not has_equipment['armor']:
            new_contract = Contract(0, 'buy', 'armor', 'town', self.faction, [], False, True, True)
            self.brain.contract = new_contract
            return True
        elif not has_equipment['weapon']:
            new_contract = Contract(0, 'buy', 'weapon', 'town', self.faction, [], False, True, True)
            self.brain.contract = new_contract
            return True

    def misc_monologue(self):

        soliloquy_chance = libtcod.random_get_int(0, 0, 100)

        if soliloquy_chance < self.brain.personality.verbosity:  # link to hero personality
            if map[self.x][self.y].dungeon.alignment < 50:  # evil dungeon
                self.activitylog['history'].append(pick_random_from_list(event_misc_evil))
            elif map[self.x][self.y].dungeon.alignment > 50:  # good dungeon
                self.activitylog['history'].append(pick_random_from_list(event_misc_good))
            else:
                self.activitylog['history'].append(pick_random_from_list(event_misc_neutral))

    def hero_decision(self):  # massively and gloriously deprecated. Never to be seen again.

        hp_float = float(self.hp['current'])
        maxhp_float = float(self.hp['max'])

        hero_condition = hp_float / maxhp_float
        x = self.x
        y = self.y

        if self.check_hero_engaged():
            for monster in monster_list:
                if [self.x, self.y] == [monster.x, monster.y]:
                    adversary = monster
                    break

            self.duel(adversary)

        if not self.personality.motivation:  # we need to define a goal
            if self.hp['current'] > 0:  # we aren't dead
                # what do we need?
                cash_motive = self.wealth / self.base_level  # try and get everything sorted in to a relative motive. Could be modified by personality.
                # $ per level, useful if we decide to go on a shopping spree ... ?

                buy_motive = 0
                equipment_wants = []

                has_armor = 0
                has_weapon = 0
                has_clothing = 0

                scrolls_held = 0

                cautious_dungeon = 30  # the percent chance we will go in to the dungeon if we are not 100% happy with our equipment
                normal_dungeon = 60  # the percent chance we will go in to the dungeon if we have three items of equipment. SHould be modified by personality aspects.

                for item in self.inventory:
                    item_type = master_item_list[item[0]][9]
                    if item_type == 'armor':
                        has_armor += 1

                    if item_type == 'weapon':
                        has_weapon += 1

                    if item_type == 'clothing':
                        has_clothing += 1

                    if item_type == 'scroll':
                        scrolls_held += 1

                if not has_clothing:
                    equipment_wants.append('clothing')
                    buy_motive += 1
                if not has_weapon:
                    equipment_wants.append('weapon')
                    buy_motive += 1
                if not has_armor:
                    equipment_wants.append('armor')
                    buy_motive += 1

                # so buy motive can be 1 to 3

                sell_motive = 0

                items_held = len(self.inventory)

                sell_motive = items_held - 3

                if self.faction in scroll_users:
                    sell_motive -= scrolls_held  # we want to keep our scrolls

                # start of main motivation setting decision tree
                if not self.faction == 'Merchants':  # we are an adventurer
                    if buy_motive == 3:
                        # we haven't got anything of use, we can't go dungeoneering like this.
                        self.activitylog['history'].append('I am completely unprepared for this life.')
                        if cash_motive >= 90:
                            # we've probably got enough money to buy some stuff
                            self.personality.motivation = ['buy',
                                                           equipment_wants]  # given shopping list. Hero will try and buy this stuff.
                            # There should be a chance of getting demotivated with any task, particularly something like this which might put them in an unachievable loop.
                        elif self.faction in scroll_users:  # we don't have any equipment, and not enough cash to do anything about it.
                            if libtcod.random_get_int(0, 0, 10) < 6:
                                self.personality.motivation = ['buy_scrolls']
                            else:
                                self.personality.motivation = ['leave_town']
                        elif scrolls_held >= 1:
                            self.personality.motivation = ['sell_scrolls',
                                                           scrolls_held]  # this number should correlate to attempts, not necessarily successful sales
                        else:
                            self.personality.motivation = ['leave_town']

                    elif buy_motive == 2:
                        # we are short of equipment, we should try and get some more.
                        if cash_motive >= 60:
                            # we probably have enough cash to do something about it
                            self.personality.motivation = ['buy', equipment_wants]
                        elif self.faction in scroll_users:
                            if libtcod.random_get_int(0, 0, 10) < 5:
                                self.personality.motivation = ['buy_scrolls']
                            else:
                                self.personality.motivation = ['leave_town']
                        elif scrolls_held >= 1:  # just try and palm off some unwanted stuff
                            self.personality.motivation = ['sell_scrolls', scrolls_held]
                        else:
                            self.personality.motivation = ['leave_town']

                    elif buy_motive == 1:
                        # we are probably okay to go dungeoneering ...
                        if cash_motive >= 30:
                            # lets try and fix the hole in our equipment
                            self.personality.motivation = ['buy', equipment_wants]
                        elif self.faction in scroll_users:
                            if sell_motive > 1:
                                self.personality.motivation = ['sell', sell_motive]
                            else:
                                if libtcod.random_get_int(0, 0, 100) < cautious_dungeon:
                                    self.personality.motivation = ['go_dungeon']
                                else:
                                    if libtcod.random_get_int(0, 0, 10) < 4:
                                        self.personality.motivation = ['buy_scrolls']
                                    else:
                                        self.personality.motivation = ['leave_town']
                        elif sell_motive >= 1:
                            self.personality.motivation = ['sell', sell_motive]
                        else:
                            if libtcod.random_get_int(0, 0, 100) < cautious_dungeon:
                                self.personality.motivation = ['go_dungeon']
                            else:
                                self.personality.motivation = ['leave_town']

                    elif sell_motive >= 3:  # carrying far too much equipment ...
                        self.personality.motivation = ['sell', sell_motive]  # lets get rid of some ...

                    else:
                        ready_decision = libtcod.random_get_int(0, 0, 100)
                        if self.faction in scroll_users:  # maybe do a spot of shopping first ...
                            if ready_decision < 25:
                                self.personality.motivation = ['buy_scrolls']
                            elif ready_decision < 80 and self.assess_contracts():
                                self.personality.motivation = ['seek_contract']
                            else:
                                self.personality.motivation = ['go_dungeon']
                        elif libtcod.random_get_int(0, 0, 100) < normal_dungeon:
                            if ready_decision < 55 and self.assess_contracts():
                                self.personality.motivation = ['seek_contract']
                            else:
                                self.personality.motivation = ['go_dungeon']
                        else:
                            self.personality.motivation = ['leave_town']
                else:
                    self.personality.motivation = ['leave_town']
                    # any merchant that has been demotivated has likely achieved his goal. So he should get outta town.
                    # merchant goals set up on initial arrival

        if self.in_dungeon == 0:  # are we in a dungeon? No? Lets proceed ...
            if self.hp['current'] == self.hp['max']:  # we are fully rested ...
                wild_decision = libtcod.random_get_int(0, 0, 100)

                motive = self.personality.motivation[0]

                if motive == 'leave_town':
                    if wild_decision < 4:
                        self.demotivate()  # change our minds ... something might have changed? Possibly just an extension of the idle command ...
                    elif wild_decision < 35:
                        pass  # we don't have to leave just yet ...
                    else:
                        self.leave_town()  # get the hero out of town.

                elif motive == 'seek_contract':

                    contract_index = self.assess_contracts()

                    if contract_index:
                        contract_index -= 1
                        self.seek_contract_acceptance(contract_list[contract_index])
                    else:
                        self.demotivate()  # none that we fancy just yet


                elif motive == 'buy_scrolls':
                    if wild_decision < 2:  # lets rethink things ...
                        self.demotivate()
                    elif wild_decision < 16:
                        self.move_to_new_shop('Random')
                    elif wild_decision < 45:
                        self.browse_stock('scroll')  # try and have a go for one ...
                        self.demotivate()  # then move on ...
                    else:
                        pass

                elif motive == 'sell_scrolls':
                    if wild_decision < 2:  # lets rethink things ...
                        self.demotivate()
                    elif wild_decision < 16:
                        self.move_to_new_shop('Random')
                    elif wild_decision < 45:
                        self.sell_items('scroll')
                        self.personality.motivation[1] -= 1
                        if self.personality.motivation[1] <= 0:
                            self.demotivate()
                    else:
                        pass

                elif motive == 'sell':
                    if wild_decision < 2:  # lets rethink things ...
                        self.demotivate()
                    elif wild_decision < 16:
                        self.move_to_new_shop('Random')
                    elif wild_decision < 45:
                        self.sell_items()
                        self.personality.motivation[1] -= 1
                        if self.personality.motivation[1] <= 0:
                            self.demotivate()
                    else:
                        pass
                        # event_item_bought

                        # event_item_sold

                elif motive == 'sell_cargo':
                    if wild_decision < 1:  # lets rethink things ... 4 days?
                        self.demotivate()
                    elif wild_decision < 16:
                        self.move_to_new_shop('Random')
                    elif wild_decision < 45:
                        self.sell_items()
                        if len(self.inventory) <= 0:
                            self.demotivate()  # stock sold
                    else:
                        pass

                elif motive == 'buy_cargo':
                    if wild_decision < 1:  # lets rethink things ...
                        self.demotivate()
                    elif wild_decision < 16:
                        self.move_to_new_shop('Random')
                    elif wild_decision < 45:
                        self.browse_stock()  # buy whatever we fancy ...
                        if self.wealth <= (20 * self.base_level):  # running out of cash
                            self.demotivate()
                    else:
                        pass

                elif motive == 'buy':
                    if wild_decision < 2:  # lets rethink things ...
                        self.demotivate()
                    elif wild_decision < 15:
                        self.move_to_new_shop('Random')
                    elif wild_decision < 45:
                        need = self.personality.motivation[1].pop()
                        self.browse_stock(need)
                        if len(self.personality.motivation[1]) <= 0:
                            self.demotivate()
                    else:
                        pass

                elif motive == 'go_dungeon':
                    dungeon_visit = 0
                    for dungeon in dungeon_list:
                        if dungeon[1] == self.activitylog['visit_history'][-1]:  # just visited this dungeon
                            dungeon_visit = 1

                    if dungeon_visit != 1:
                        if wild_decision < 30:
                            self.dress_thineself()
                            dungeon_choice = self.find_dungeon()
                            if dungeon_choice:
                                self.move_to_dungeon(dungeon_choice)
                            else:
                                self.personality.motivation = ['leave_town']
                        elif wild_decision < 32:
                            self.demotivate()
                        else:
                            pass
                    else:
                        self.demotivate()

                elif motive == 'contract':

                    contract = self.personality.motivation[1]

                    asking_price = contract['asking_price']
                    mission_type = contract['mission_type']
                    target_name = contract['target_name']
                    contract_type = contract['contract_type']
                    asking_faction = contract['asking_faction']

                    if self.activitylog['visit_history'][
                        -1] == target_name:  # JUST been in to the dungeon, i.e first active turn in town
                        # need to resolve contract.
                        if self.move_to_new_shop(asking_faction):  # check if it's a valid move
                            self.resolve_contract()
                        else:  # got away with it somehow, maybe the shop was destroyed
                            for items in self.activitylog['contract_cargo']:  # transfer cargo in to our own inventory
                                self.inventory.append(items)
                            self.activitylog['contract_cargo'] = []
                            self.demotivate()



                    elif contract_type == 'monster':
                        # insert monster interaction code here
                        self.move_to_monster(target_name)
                    elif contract_type == 'dungeon':
                        # go to the particular dungeon related to the contract
                        self.dress_thineself()
                        self.move_to_dungeon(target_name)
                    else:
                        self.demotivate()

                else:
                    self.demotivate()  # start again?

                    # ~ if wild_decision <= 5:
                    # ~ self.move_to_new_shop('Random')
                    # ~ elif wild_decision <= 14:
                    # ~ self.browse_stock()
                    # ~ elif wild_decision <= 22:
                    # ~ self.sell_items()
                    # ~ elif wild_decision <= 23: #once every four days? #debugged up to a daft level ... set as 23 normally
                    # ~ self.move_to_dungeon(self.find_dungeon())
                    # ~ hero_message(self.name + ' descends, for glory!')
                    # ~ else:
                    # ~ #hero_message(self.name + ' does nothing ...')
                    # ~ pass
            else:
                pass

        # logic for heroes in the dungeon

        # event_success_fight ##list of flavour text items
        # event_damaged_fight
        # event_down_stairs
        # event_up_stairs
        # event_misc_evil
        # event_misc_good
        # event_misc_neutral
        # event_item_found

        elif self.in_dungeon > 0:  # so we are in a dungeon
            if self.hp['current'] > 0:
                if map[self.x][self.y].dungeon:
                    dlev = map[x][y].dungeon.base_level  # dungeon base level

                    if self.in_dungeon:  # first things first, run a check for healers and defilers.
                        if libtcod.random_get_int(0, 0,
                                                  4) == 4:  # one in four chance of getting to interact with a possible corpse
                            for corpse in dead_heroes:
                                hero = corpse[0]
                                if [self.x, self.y] == [hero.x, hero.y]:  # check if there is a hero here
                                    if hero.hp['current'] <= 0:  # check if the hero is dead
                                        if self.in_dungeon == hero.in_dungeon:  # we are on the same level
                                            if corpse[1] < hero_rot_time:  # the corpse is still there
                                                if 'healer' in self.personality.perk:
                                                    hero.hp['current'] = hero.hp[
                                                        'max']  # ressurect! To max points, otherwise they just die again ...
                                                    dead_heroes.remove(corpse)
                                                    town_heroes.append(corpse[0])
                                                    self.gain_experience(10)
                                                    self.activitylog['history'].append(
                                                        'I have restored the life force to a soul in need.')

                                                    hero_message(str(self.name) + ' has raised ' + str(hero.name) + '!',
                                                                 libtcod.light_yellow, libtcod.dark_yellow)
                                                    if hero.faction == 'Necromancers':
                                                        hero.activitylog['history'].append(
                                                            self.name + ' has brought me back from death.')
                                                    else:
                                                        hero.activitylog['history'].append(
                                                            self.name + ' has given me back life!')

                                                    hero.in_dungeon = 0
                                                    hero.go_home()
                                                    hero.undress_thineself()

                                                    # self.in_dungeon = 0 #keep the resurrector in the dungeon, commented out
                                                    # self.go_home() #no choice, gameplay wise, but to teleport them back home?
                                                    # self.undress_thineself()

                                                elif 'defiler' in self.personality.perk:
                                                    dead_heroes.remove(corpse)
                                                    hero_message(hero.name + ' is defiled!', libtcod.light_red,
                                                                 libtcod.dark_red)

                                                    self.activitylog['history'].append(
                                                        'I have gained power from the corpse of another.')
                                                    self.gain_experience(10)

                                                    gender_test = libtcod.random_get_int(0, 0, 1)
                                                    if gender_test == 0:
                                                        gender = 'm'
                                                    else:
                                                        gender = 'f'

                                                    birth_hero(gender)
                                                    hero_message(hero_list[-1].name + ' takes up the fight!',
                                                                 libtcod.light_yellow, libtcod.dark_yellow)

                    event_chance = libtcod.random_get_int(0, 0,
                                                          100)  # an event might take us, whether we like it or not.

                    if event_chance < 20:
                        # event happens, regardless of heroes motivations.
                        event = libtcod.random_get_int(0, 0, 100)  # roll d100 to determine the event.
                        if event < 20:  # nothing really. Flavour text added to heroes experience.
                            if map[self.x][self.y].dungeon.alignment < 50:  # evil dungeon
                                self.activitylog['history'].append(pick_random_from_list(event_misc_evil))
                            elif map[self.x][self.y].dungeon.alignment > 50:  # good dungeon
                                self.activitylog['history'].append(pick_random_from_list(event_misc_good))
                            else:
                                self.activitylog['history'].append(pick_random_from_list(event_misc_neutral))


                    else:
                        if hero_condition < 0.4:  # in this case, the hero is likely to want to escape.
                            next_move = libtcod.random_get_int(0, 0, 100)
                            if next_move < 15:
                                self.fight(generate_encounter(1, dlev, 1, dlev + (self.in_dungeon / 3)))
                            elif next_move < 20:
                                self.dungeon_descend()

                                # hero_message(self.name + ' goes deeper, despite himself!')
                            elif next_move < 50:
                                self.leave_dungeon()
                                # hero_message(self.name + ' is getting out, while he can!')
                            elif next_move < 51:
                                pass
                                # self.find_item()
                            else:
                                pass
                        elif hero_condition < 0.8:  # slightly more cautious
                            next_move = libtcod.random_get_int(0, 0, 100)
                            if next_move < 25:
                                self.fight(generate_encounter(1, dlev, 1, dlev + (self.in_dungeon / 3)))
                            elif next_move < 35:
                                self.dungeon_descend()
                                # hero_message(self.name + ' goes deeper!')
                            elif next_move < 40:
                                self.leave_dungeon()
                                # hero_message(self.name + ' steps back through the dungeon.')
                            elif next_move < 41:
                                self.find_item()
                            else:
                                pass
                        else:  # not cautious. Looking for trouble.
                            next_move = libtcod.random_get_int(0, 0, 100)
                            if next_move < 45:
                                self.fight(generate_encounter(1, dlev, 1, dlev + (self.in_dungeon / 3)))
                            elif next_move < 55:
                                self.dungeon_descend()
                                # hero_message(self.name + ' goes deeper, for glory!')
                            elif next_move < 56:
                                self.leave_dungeon()
                                # hero_message(self.name + ' steps back through the dungeon, in shame.')
                            elif next_move < 58:
                                self.find_item()
                            else:
                                pass

                                # generate_encounter(level_min, level_max, pop_low, pop_high):

    def move_to_monster(self, target_name):

        if len(monster_list) > 0:
            monster_found = 0
            for monster in monster_list:
                if monster.name == target_name:
                    monster_found = 1
                    x = monster.x
                    y = monster.y
                    break

            if monster_found:
                self.x = x
                self.y = y
                return True

            else:
                return False  # scrap contract, monster gone
        else:
            return False  # scrap contract, monster gone

    def world_sell_item(self):  # currently abstracted to any item

        no_items = len(self.inventory)

        if no_items > 0:  # we actually have something to sell
            item = libtcod.random_get_int(0, 0, no_items - 1)

            self.wealth += self.inventory[item][5]  # get what you think it is worth ...

            item_index = self.inventory[item][0]
            item_type = master_item_list[item_index][9]

            if item_type == 'weapon' or item_type == 'scroll':
                self.activitylog['history'].append(
                    'I have sold a ' + item_type + ' to a shop in ' + pick_random_from_list(town_names))
            else:
                self.activitylog['history'].append(
                    'I have sold some ' + item_type + ' to a shop in ' + pick_random_from_list(town_names))

            del self.inventory[item]

    def world_buy_item(self):
        item = create_item(1, 1 + self.base_level, 'all')
        self.inventory.append(item)  # add an item to our inventory
        self.inventory[-1][5] = appraise_value(self.inventory[-1], self.faction, self.base_level)  # give it a value

        item_type = master_item_list[item[0]][9]

        if item_type == 'weapon' or item_type == 'scroll':
            self.activitylog['history'].append(
                'I have bought a ' + item_type + ' from a shop in ' + pick_random_from_list(town_names))
        else:
            self.activitylog['history'].append(
                'I have bought some ' + item_type + ' from a shop in ' + pick_random_from_list(town_names))
            # no cost outside the world ...

    def pay_rent(self):

        x = self.x
        y = self.y
        if map[x][y].shop:  # are we on a shop?
            if not map[x][y].faction == self.faction:  # is this home?
                rent_rate = map[x][y].shop.base_level  # No, then pay rent for the night.
                if rent_rate < self.wealth:
                    self.wealth -= rent_rate
                    map[x][y].shop.wealth += rent_rate
                else:
                    self.go_home()

    def world_wage(self):

        if self.wealth < (self.base_level * 100):
            wage = libtcod.random_get_int(0, 0, self.base_level * 10)
            self.wealth += wage

    def world_hero_decision(self):

        random_decision = libtcod.random_get_int(0, 0, 100)
        random_sub_decision = libtcod.random_get_int(0, 0, 100)

        if self.hp['current'] < self.hp['max']:
            self.hp['current'] = self.hp['max']

        if self.faction == 'Merchants':
            if len(self.inventory) > 2:  # general purge of items ...
                self.world_sell_item()
            elif random_decision < merchant_enter_town_rate:
                self.enter_town()
                self.gain_experience(20)
                self.go_home()
            else:
                pass
        else:
            if random_decision < (base_visit_rate + (len(the_mayoress.noticeboard.notices) * contract_visit_rate)):
                # our hero will carry something out
                if random_sub_decision < 5:
                    self.enter_town()
                    self.go_home()
            elif random_decision > 95:
                if random_sub_decision < 50:
                    self.world_sell_item()
                    pass
                elif random_sub_decision < 65:
                    self.world_buy_item()
                else:
                    pass

        scribble = libtcod.random_get_int(0, 0, 450) + self.brain.personality.verbosity

        if scribble >= 450:
            self.activitylog['history'].append(pick_random_from_list(event_world_by_faction[self.faction]))

    def enter_town(self):  # move hero from global list to local list
        global hero_list, town_heroes

        for index, heroes in enumerate(hero_list):
            if self == heroes:
                entering_hero = hero_list.pop(index)
                if self.faction == 'Merchants':
                    entering_hero.brain.phase = 'Phase_3'
                else:
                    entering_hero.brain.phase = 'Phase_1'
                break

        town_heroes.append(entering_hero)
        self.demotivate()

        self.activitylog['visit_history'].append('Out of town')

        if self.faction == 'Merchants':
            cargo = libtcod.random_get_int(0, 4, 8)

            if libtcod.random_get_int(0, 0, 100) < 67:  # use this to weight the proportion of sell cargo vs buy cargo

                item_type = assess_town_demand()
                for n in range(cargo):
                    self.brain.decisions.append('sell_cargo')
                    if libtcod.random_get_int(0, 0, 1) == 1:  # 50/50 chance it is the shortfall item
                        new_goods = create_item(1, 1 + self.base_level, 'all', item_type)
                    else:
                        new_goods = create_item(1, 1 + self.base_level, 'all')
                    self.inventory.append(new_goods)  # add an item to our cargo
                    self.inventory[-1][5] = appraise_value(self.inventory[-1], self.faction, self.base_level)
                    if log_information:
                        log_info(str(master_item_list[new_goods[0]][1]) + ' added to merchant cargo')
                if item_type == 'weapon' or item_type == 'scroll':
                    self.activitylog['history'].append('I come to town with a cargo of ' + item_type + 's.')
                else:
                    self.activitylog['history'].append('I come to town with a cargo of ' + item_type + '.')
                self.activitylog['history'].append('Word is, the town was running short.')
                hero_message(self.name + ' arrives with goods', libtcod.light_green, libtcod.dark_green)
            else:
                self.wealth += libtcod.random_get_int(0, 10 * self.base_level,
                                                      100 * self.base_level)  # little extra cash ...
                for n in range(cargo):
                    self.brain.decisions.append('buy_cargo')  # buy loads of stuff and get out of dodge
                hero_message(self.name + ' arrives, looking for goods', libtcod.light_green, libtcod.dark_green)
                self.activitylog['history'].append('Word is, their are bargains to be had in this town.')
        else:
            hero_message(self.name + ' arrives in to town', libtcod.light_yellow, libtcod.dark_yellow)
            self.activitylog['history'].append(
                'I enter the town, ' + pick_random_from_list(event_enter_town_by_faction[self.faction]))

    def leave_town(self):
        global hero_list, town_heroes

        if self.hp['current'] > 0:
            for index, heroes in enumerate(town_heroes):
                if self == heroes:
                    leaving_hero = town_heroes.pop(index)
                    break

            hero_list.append(leaving_hero)
            hero_message(self.name + ' leaves town', libtcod.light_red, libtcod.dark_red)
            self.activitylog['history'].append(
                'I leave town, ' + pick_random_from_list(event_leave_town_by_faction[self.faction]))
            self.activitylog['visit_history'] = []

    def move_to_new_shop(self, faction):  # picks by faction
        if faction == 'Random':
            faction_destination = libtcod.random_get_int(0, 0, len(
                shop_list_inc_player) - 1)  # find a shop random index from the available

            shop = shop_list_inc_player[faction_destination]

            self.x = shop[2]
            self.y = shop[3]
            self.activitylog['visit_history'].append(map[self.x][self.y].name)
            return True

        # collate a list of shops in the correct faction:
        else:

            possible_destinations = []

            for shop in shop_list_inc_player:
                if shop[0] == faction:
                    possible_destinations.append(shop)

            # now we have a list of possible venues.
            if len(possible_destinations) > 0:
                faction_destination = libtcod.random_get_int(0, 0, len(possible_destinations) - 1)

                shop = possible_destinations[faction_destination]

                self.x = shop[2]
                self.y = shop[3]
                self.activitylog['visit_history'].append(map[self.x][self.y].name)

                return True
            else:
                return False

    def move_to_dungeon(self, dungeon_name):
        if dungeon_name:
            for dungeon in dungeon_list:
                if dungeon[1] == dungeon_name:
                    self.x = dungeon[2]
                    self.y = dungeon[3]
            self.in_dungeon = 1
            # hero_message(self.name + ' descends, for glory!')
            self.activitylog['history'].append('I enter the ' + str(map[self.x][self.y].name) + '!')
            self.activitylog['visit_history'].append(dungeon_name)

            return True
        else:
            return False

    def find_dungeon(self):

        desired_dungeon_level = self.stats['perceived'] / 6
        if desired_dungeon_level < 1:
            desired_dungeon_level = 1

        dungeon_name = False

        possible_dungeons = []

        for dungeon in dungeon_list:  # iterate through the list of dungeons

            if desired_dungeon_level == dungeon[0]:  # does the dungeon level match the one we want?
                possible_dungeons.append(dungeon)  # add it to the list

        if len(possible_dungeons) > 0:
            index = libtcod.random_get_int(0, 0, len(possible_dungeons) - 1)
            dungeon_name = possible_dungeons[index][1]
            self.activitylog['history'].append('I prepare to travel to a nearby dungeon.')
            return dungeon_name
        else:
            # hero_message(self.name + ' wants more challenge.') #can't find an appropriate dungeon

            return False  # he should leave these lands. He wants to go to a deeper dungeon.

    def leave_dungeon(self):  # leave dungeon, or go up a level in the current dungeon
        self.in_dungeon -= 1
        if self.in_dungeon == 0:
            self.go_home()
            # self.undress_thineself()
            # hero_message(self.name + ' returns to town a hero!')
            self.activitylog['history'].append('I enjoy a heroes welcome back in town!')
        else:
            if libtcod.random_get_int(0, 0, 4) == 4:
                self.activitylog['history'].append('I ascend, ' + pick_random_from_list(event_up_stairs))

    def stop_descending(self):
        descent_count = self.brain.decisions.count('descend')

        if descent_count:
            for n in range(descent_count):
                self.brain.decisions.remove('descend')

    def dungeon_descend(self):  # go deeper in to the dungeon ...
        if self.in_dungeon:
            self.in_dungeon += 1
            if libtcod.random_get_int(0, 0, 4) == 4:
                self.activitylog['history'].append('I descend, ' + pick_random_from_list(event_down_stairs))

    def rest(self):  # restore an amount of hitpoints per day ...

        self.hp['current'] += base_heal_rate
        if self.hp['current'] > self.hp['max']:
            self.hp['current'] = self.hp['max']
        if libtcod.random_get_int(0, 0, 4) == 4:
            self.activitylog['history'].append('I need time to rest.')

    def find_item(self):
        x = self.x
        y = self.y

        if map[x][y].dungeon:
            if map[x][y].dungeon.inventory:
                number_items = len(map[x][y].dungeon.inventory) - 1
                item_won = libtcod.random_get_int(0, 0, number_items)

                item = map[x][y].dungeon.inventory.pop(item_won)

                if log_information:
                    log_info(str(item_won) + ' ' + str(item) + ' ' + self.faction + ' ' + str(self.base_level))

                set_value = appraise_value(item, self.faction, self.base_level)
                item[5] = set_value

                if 'find_item' in self.brain.decisions:
                    self.activitylog['contract_cargo'].append(item)
                    self.brain.decisions.remove('find_item')
                else:
                    self.inventory.append(item)

                item_type = master_item_list[item[0]][9]

                # hero_message(self.name + ' finds ' + master_item_list[item[0]][9] + '!')
                if item_type == 'weapon' or item_type == 'scroll':
                    if libtcod.random_get_int(0, 0, 3) == 3:
                        self.activitylog['history'].append('I find a ' + str(item_type) + '.')
                        self.activitylog['history'].append(pick_random_from_list(event_item_found))
                    else:
                        self.activitylog['history'].append(
                            'I find a ' + str(item_type) + pick_random_from_list(event_item_location))
                else:
                    if libtcod.random_get_int(0, 0, 3) == 3:
                        self.activitylog['history'].append('I find some ' + str(item_type) + '.')
                        self.activitylog['history'].append(pick_random_from_list(event_item_found))
                    else:
                        self.activitylog['history'].append(
                            'I find some ' + str(item_type) + pick_random_from_list(event_item_location))

            else:
                pass

    def fight(self, encounter):
        hero_power = self.stats['real']

        dungeon_vanquished = 0

        kills = 0
        damage = 0

        for monster in encounter:
            monster_power = master_monster_list[monster]['power']
            hero_roll = libtcod.random_get_int(0, 0, hero_power)
            monster_roll = libtcod.random_get_int(0, 0, monster_power)
            if hero_roll < monster_roll:  # hero loses fight, lose a hp. Monster survive? Doesn't matter ...
                self.hp['current'] -= 1
                damage += 1
                if self.hp['current'] < 1:
                    hero_message(self.name + ' is vanquished by evil!', libtcod.red, libtcod.dark_red)
                    self.die()
                    map[self.x][self.y].dungeon.breed_creatures()  # add to the population of the dungeon.
                    message('The ' + map[self.x][self.y].name + ' ranks swell ...', libtcod.red, libtcod.dark_red)
                    break
            else:
                self.gain_experience(monster_power)
                # hero_message(self.name + ' gains ' + str(monster_power) + ' exp!')
                self.activitylog['kills'].append(monster)  # record kills ...
                kills += 1
                # manage the dungeon population
                if map[self.x][self.y].dungeon:
                    if map[self.x][self.y].dungeon.population > 0:  # there are some of the little bastards left to kill
                        map[self.x][self.y].dungeon.population -= 1
                    else:
                        # dungeon has just been cleared
                        dungeon_vanquished = 1
                        break  # exit for monster in encounter

        if self.hp['current'] > 0:
            coin_treasure = libtcod.random_get_int(0, 0, (kills + self.in_dungeon))
            # self.activitylog['history'].append('I meet, and kill ' + str(kills) + ' creature(s) in the dungeon.')
            if libtcod.random_get_int(0, 0, 4) == 4:  # report a flavour message
                if damage:
                    self.activitylog['history'].append(str(pick_random_from_list(event_fight)))
                    self.activitylog['history'].append(str(pick_random_from_list(event_damaged_fight)))
                    # event_success_fight
                    # event_damaged_fight
                else:
                    self.activitylog['history'].append(str(pick_random_from_list(event_fight)))
                    self.activitylog['history'].append(str(pick_random_from_list(event_success_fight)))

            if map[self.x][self.y].dungeon:
                if map[self.x][self.y].dungeon.wealth > 0:
                    map[self.x][self.y].dungeon.wealth -= coin_treasure
                    self.wealth += coin_treasure
                    if map[self.x][self.y].dungeon.wealth < 0:
                        map[self.x][self.y].dungeon.wealth = 0
                else:
                    pass  # we've bled the dungeon dry ...

            item_chance = 4

            if libtcod.random_get_int(0, 0, 100) < item_chance:  # any treasure?
                self.find_item()

        if dungeon_vanquished:
            hero_message(self.name + ' cleanses the ' + map[self.x][self.y].name + '!', libtcod.green,
                         libtcod.dark_green)
            decommission_dungeon(self.x, self.y)
            self.activitylog['history'].append('That is the last of them in this hell hole!')
            # hero_message(str(kills) + ' kills for ' + self.name + '!') #glory to the hero!

    def check_hero_engaged(self):
        engaged = 0
        if self.in_dungeon == 0:
            for monster in monster_list:
                if [monster.x, monster.y] == [self.x, self.y]:
                    engaged = 1  # there is a hero in this square, and they are alive
            if engaged:
                return True
            else:
                return False
        else:
            return False

    def check_hero_has_company(self):
        company = []

        for heroes in town_heroes:
            if [heroes.x, heroes.y, heroes.in_dungeon] == [self.x, self.y, self.in_dungeon]:
                if heroes != self:
                    company.append(heroes)

        return company

    def check_for_corpses(self):
        corpses = 0

        for heroes in dead_heroes:
            if [heroes.x, heroes.y, heroes.in_dungeon] == [self.x, self.y, self.in_dungeon]:
                corpses += 1

        return corpses

    def die(self):
        global dead_heroes

        hero_message(self.name + ' has DIED!!', libtcod.red, libtcod.red)

        x = self.x
        y = self.y

        if len(self.inventory) > 0:
            for items in self.inventory:
                dropped = items
                if map[x][y].dungeon:
                    map[x][y].dungeon.inventory.append(
                        dropped)  # give the dungeon your items! What about monster deaths in the field?
                elif self.check_hero_engaged():
                    pass

            for items in self.activitylog['contract_cargo']:
                dropped = items
                if map[x][y].dungeon:
                    map[x][y].dungeon.inventory.append(dropped)  # give the dungeon your items!
                elif self.check_hero_engaged():
                    pass

        self.inventory = []
        self.activitylog['contract_cargo'] = []

        if map[x][y].dungeon:
            map[x][y].dungeon.wealth += self.wealth
            map[x][y].dungeon.gain_experience(self.base_level)
        self.wealth = 0  # give the dungeon your coin!

        contract = self.brain.contract
        self.brain.contract = 0

        if contract.asking_faction == player_name:
            message(self.name + ' has died, releasing them from the terms of your contract!', libtcod.light_red,
                    libtcod.dark_red)

        try:
            the_mayoress.noticeboard.notices.remove(contract)
        except:
            pass

        the_mayoress.flags.append('hero_died')

        dead_heroes.append([self, 0])
        if log_information:
            log_info(str(dead_heroes[-1][0].name) + ' dies.')
            for hero in town_heroes:
                log_info(hero.name)

        town_heroes.remove(self)  # take ourselves out of the town_heroes list

    def seek_contract_acceptance(self, contract):

        for index, item in enumerate(the_mayoress.noticeboard.notices):
            if contract == item:
                contract_index = index
                break

        asking_price = contract.asking_price
        mission_type = contract.mission_type
        target_name = contract.target_name
        contract_type = contract.contract_type
        asking_faction = contract.asking_faction

        if self.move_to_new_shop(asking_faction):
            # we are able to move to the shop, i.e. it exists
            # we have already determined the terms are acceptable to us.
            if asking_faction == player_name:
                # need a pop-up for the player to make a decision
                if discuss_contract(contract_index, self):  # we accept the terms, try and pay
                    if mission_type == 'item_hunt':
                        the_mayoress.noticeboard.notices[contract_index].accept_me(self.name)
                        self.brain.contract = the_mayoress.noticeboard.notices[contract_index]

                        message(self.name + ' has taken on your contract!', libtcod.light_yellow, libtcod.dark_yellow)
                        return True

                    elif player.wealth >= asking_price:
                        # we have enough funds
                        the_mayoress.noticeboard.notices[contract_index].paid = True
                        the_mayoress.noticeboard.notices[contract_index].accept_me(self.name)

                        self.brain.contract = the_mayoress.noticeboard.notices[
                            contract_index]  # set the motivation for the hero to carry out the contract

                        player.wealth -= asking_price
                        self.wealth += asking_price

                        message(self.name + ' has taken on your contract!', libtcod.light_yellow, libtcod.dark_yellow)
                        self.reputation.improve_reputation(player_name)
                        log_purchase('CONTRACT', asking_price, self.name)
                        return True

                    else:
                        message('You no longer have the funds to honour the contract! Contract repealed.',
                                libtcod.light_red, libtcod.dark_red)
                        try:  # whatever the result of the above, we should wrap things up and move on.
                            the_mayoress.noticeboard.notices.remove(
                                contract)  # may not have ever appeared here if self-motivated
                        except:
                            pass  # might want to put in something about self-fulfilment here
                        self.reputation.worsen_reputation(player_name)
                        return False
                else:
                    message('Contract NOT assigned to ' + self.name + '.', libtcod.light_red, libtcod.dark_red)
                    self.reputation.worsen_reputation(player_name)
                    return False
            else:
                if mission_type == 'item_hunt':
                    the_mayoress.noticeboard.notices[contract_index].accept_me(self.name)
                    self.brain.contract = the_mayoress.noticeboard.notices[contract_index]
                    return True
                else:
                    [x, y] = find_shop_by_faction(asking_faction)
                    if map[x][y].shop.wealth >= asking_price:

                        the_mayoress.noticeboard.notices[contract_index].paid = True
                        the_mayoress.noticeboard.notices[contract_index].accept_me(self.name)
                        self.brain.contract = the_mayoress.noticeboard.notices[contract_index]

                        map[x][y].shop.wealth -= asking_price
                        self.wealth += asking_price
                        self.reputation.improve_reputation(asking_faction)  # increase relations
                        return True
                    else:
                        self.reputation.worsen_reputation(asking_faction)
                        return False
        elif asking_faction == 'Mayoress':
            if mission_type == 'item_hunt':
                the_mayoress.noticeboard.notices[contract_index].accept_me(self.name)
                self.brain.contract = the_mayoress.noticeboard.notices[contract_index]
                return True
            else:
                if the_mayoress.wealth >= asking_price:

                    the_mayoress.noticeboard.notices[contract_index].paid = True
                    the_mayoress.noticeboard.notices[contract_index].accept_me(self.name)
                    self.brain.contract = the_mayoress.noticeboard.notices[contract_index]

                    the_mayoress.wealth -= asking_price
                    self.wealth += asking_price
                    return True
                    ##self.reputation.improve_reputation(asking_faction) #increase relations
                else:
                    return False
                    ##self.reputation.worsen_reputation(asking_faction)
        else:  # shop burnt down or something ...
            try:
                the_mayoress.noticeboard.notices.remove(contract)
            except:
                pass

            self.brain.contract = 0
            return False

    def resolve_contract_deprecated(self):

        x = self.x
        y = self.y
        receiving_store = map[x][y].shop.inventory

        number_items = len(self.activitylog['contract_cargo'])

        for items in self.activitylog['contract_cargo']:
            receiving_store.append(items)
            log_purchase(player_item_display(items), 'CTR', self.name)

        if map[x][y].faction == player_name:
            message('The Hero ' + self.name + ' has completed a contract on your behalf.', libtcod.light_yellow,
                    libtcod.dark_yellow)
            if number_items:
                message(str(number_items) + ' items added to your shop stock!', libtcod.light_green, libtcod.dark_green)
            else:
                message('Unfortunately, ' + self.name + ' has returned empty-handed.', libtcod.light_red,
                        libtcod.dark_red)

        contract = self.brain.personality.motivation[1]

        contract_list.remove(contract)

        self.demotivate()  # note this function should also remove the contract cargo from the hero

    #######################################
    ## MONSTER RELATED FUNCTIONS, under class HERO  ##
    #######################################
    def monster_die(self):

        affected_contracts = []
        if len(contract_list) > 0:
            for contract in the_mayoress.noticeboard.notices:
                if contract['target_name'] == self.name:
                    affected_contracts.append(contract)

        for contract in affected_contracts:
            the_mayoress.noticeboard.notices.remove(contract)

        monster_list.remove(self)

    def duel(self, adversary):

        self.dress_thineself()

        strength = self.stats['real']
        opp_strength = adversary.stats['real']

        my_roll = libtcod.random_get_int(0, 0, strength)
        their_roll = libtcod.random_get_int(0, 0, opp_strength)

        if debug_mode:
            message('Hero roll: ' + str(my_roll) + ', Monster Roll: ' + str(their_roll), libtcod.grey, libtcod.grey)
        # combat violent beast flavour text required

        if my_roll >= their_roll:  # slight favour to attacker (greater than or equal)
            adversary.hp['current'] -= 1
            self.gain_experience(adversary.base_level * 2)
            if adversary.hp['current'] <= 0:
                adversary.monster_die()
                message('The monster, ' + adversary.name + ' has been destroyed!', libtcod.yellow, libtcod.dark_yellow)
        else:
            self.hp['current'] -= 1
            if self.hp['current'] <= 0:
                self.die()

        if libtcod.random_get_int(0, 0, 100) < self.brain.personality.verbosity:
            self.activitylog['history'].append(pick_random_from_list(event_fight_monster))

    def monster_set_target(self):
        # look for a shop to ransack
        shop_measures = []

        for shops in shop_list_inc_player:
            dist = [distance_measure(self.x, self.y, shops[2], shops[3]), shops[1], shops[2], shops[3]]

            shop_measures.append(dist)  # make list of shops with distance to monster

        shop_measures_sorted = sorted(shop_measures)  # sort them out
        # shop_measures_sorted.reverse() #spin them round

        return [shop_measures_sorted[0][2], shop_measures_sorted[0][3]]  # define the location of the shop to ransack

    def check_monster_engaged(self):
        engaged = 0
        for hero in town_heroes:
            if [hero.x, hero.y] == [self.x, self.y] and hero.hp['current'] > 0 and hero.in_dungeon == 0:
                engaged = 1  # there is a hero in this square, and they are alive

        if engaged:
            return True
        else:
            return False

    def monster_decision(self):

        if not self.check_monster_engaged():
            terry = libtcod.random_get_int(0, 0, 100)
            if terry < monster_move_chance:
                if len(self.brain.decisions) > 0:
                    self.monster_action()
                else:
                    self.monster_contract()
                    self.monster_populate_actions()

    def monster_contract(self):

        [x, y] = self.monster_set_target()

        contract_target = map[x][y].name

        new_contract = Contract(0, 'ransack', contract_target, 'rampage', None, None, False, False, self.name)
        self.brain.contract = new_contract

    def monster_populate_actions(self):

        if self.brain.contract:
            if find_shop(self.brain.contract.target_name):

                self.brain.decisions.append('resolve_contract')

                self.brain.decisions.append('ransack')

                self.brain.decisions.append('move')
            else:
                pass
        else:
            pass

    def monster_action(self):

        decision = self.brain.decisions[-1]

        company = self.check_hero_has_company()

        if len(company) > 0:  # best scrap
            for hero in company:
                self.duel(self, hero)
                if self.hp['current'] <= 0:
                    break

        elif decision == 'move':

            if find_shop(self.brain.contract.target_name):
                shop = find_shop(self.brain.contract.target_name)

                [x, y] = shop

                if [self.x, self.y] == [x, y]:
                    self.brain.decisions.pop(-1)

                else:
                    delta_x = x - self.x
                    delta_y = y - self.y

                    magnitude = ((delta_x ** 2) + (delta_y ** 2)) ** 0.5

                    move_x = int(round(delta_x / magnitude))
                    move_y = int(round(delta_y / magnitude))

                    # message('Moving '+ str(move_x) + ' X & ' + str(move_y) + ' Y - ' + self.name)

                    self.x += move_x
                    self.y += move_y

            else:
                self.brain.decisions = []  # demotivate

        elif decision == 'ransack':

            self.ransack()

        elif decision == 'resolve_contract':

            self.brain.contract = None
            self.brain.decisions = []

    def ransack(self):
        message('The monster ' + self.name + ' is on the rampage!', libtcod.red, libtcod.dark_red)

        x = self.x
        y = self.y

        if map[x][y].shop:
            map[x][y].shop.base_level -= 1
            if map[x][y].shop.base_level <= 0:
                destroy_shop(x, y)
                build_shop_and_dungeon_lists()
                # self.demotivate()
        else:
            self.brain.decisions.pop(-1)  # self.demotivate()


class Personality:
    def __init__(self, markup, motivation, perk, quirk, verbosity, seeks_glory, seeks_social, seeks_balance, seeks_loot,
                 seeks_contracts, seeks_leadership, seeks_wealth,
                 seeks_knowledge):  # plenty to go at here, nothing at present ...

        self.markup = markup  # markup being the amount the hero is willing to pay more than the base value. Default 1.2.
        self.motivation = motivation  # ai hints
        self.perk = perk  # list of personality based skills obtained from levelling up etc.
        self.quirk = quirk  # personality quirks e.g. thrifty
        self.verbosity = verbosity  # stat to control amount of bilge spewed from gob
        self.seeks_glory = seeks_glory
        self.seeks_social = seeks_social
        self.seeks_balance = seeks_balance
        self.seeks_loot = seeks_loot
        self.seeks_contracts = seeks_contracts
        self.seeks_leadership = seeks_leadership
        self.seeks_wealth = seeks_wealth
        self.seeks_knowledge = seeks_knowledge

    def return_decision_personality(self):  # used for second phase of activity
        seeks_glory = self.seeks_glory
        seeks_social = self.seeks_social
        seeks_balance = self.seeks_balance
        seeks_loot = self.seeks_loot
        seeks_contracts = self.seeks_contracts
        seeks_leadership = self.seeks_leadership
        seeks_wealth = self.seeks_wealth
        seeks_knowledge = self.seeks_knowledge

        total_decision_weighting = seeks_glory + seeks_social + seeks_balance + seeks_loot + seeks_contracts + seeks_leadership + seeks_wealth + seeks_knowledge

        decision_weighting_score = libtcod.random_get_int(0, 0, total_decision_weighting)

        if decision_weighting_score < seeks_glory:
            return 'glory'
        elif decision_weighting_score < seeks_glory + seeks_social:
            return 'social'
        elif decision_weighting_score < seeks_glory + seeks_social + seeks_balance:
            return 'balance'
        elif decision_weighting_score < seeks_glory + seeks_social + seeks_balance + seeks_loot:
            return 'loot'
        elif decision_weighting_score < seeks_glory + seeks_social + seeks_balance + seeks_loot + seeks_contracts:
            return 'contracts'
        elif decision_weighting_score < seeks_glory + seeks_social + seeks_balance + seeks_loot + seeks_contracts + seeks_leadership:
            return 'leadership'
        elif decision_weighting_score < seeks_glory + seeks_social + seeks_balance + seeks_loot + seeks_contracts + seeks_leadership + seeks_wealth:
            return 'wealth'
        elif decision_weighting_score < seeks_glory + seeks_social + seeks_balance + seeks_loot + seeks_contracts + seeks_leadership + seeks_wealth + seeks_knowledge:
            return 'knowledge'
        else:
            return 'social'  # for edge cases


def blank_faction_relations():  # helper function to generate a baseline dictionary for faction relations

    faction_rep = {}

    for x in faction_list:
        faction_rep[x] = 0

    faction_rep[player_name] = 0

    return faction_rep


######################
## DEFAULT PERSONALITIES ##
######################

default_personality = {
    'Thieves':
        Personality(
            1.2,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            30,  # log chance - verbosity
            20,  # glory
            80,  # social
            0,  # balance
            120,  # loot
            60,  # contracts
            10,  # leadership
            100,  # wealth
            10,  # seeks knowledge
        ),
    'Assassins':
        Personality(
            1.2,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            20,
            10,  # glory
            0,  # social
            0,  # balance
            20,  # loot
            160,  # contracts
            0,  # leadership
            10,  # wealth
            20,  # seeks knowledge
        ),
    'Swashbucklers':
        Personality(
            1.3,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            75,
            60,  # glory
            180,  # social
            0,  # balance
            20,  # loot
            20,  # contracts
            10,  # leadership
            10,  # wealth
            10,  # seeks knowledge
        ),
    'Fighters':
        Personality(
            1.2,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            30,
            20,  # glory
            80,  # social
            0,  # balance
            20,  # loot
            60,  # contracts
            80,  # leadership
            10,  # wealth
            0,  # seeks knowledge
        ),
    'Barbarians':
        Personality(
            1.2,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            10,
            100,  # glory
            20,  # social
            0,  # balance
            10,  # loot
            30,  # contracts
            0,  # leadership
            10,  # wealth
            0,  # knowledge
        ),
    'Mages Guild':
        Personality(
            1.2,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            80,
            60,  # glory
            90,  # social
            10,  # balance
            20,  # loot
            60,  # contracts
            10,  # leadership
            80,  # wealth
            160,  # knowledge
        ),
    'Druids':
        Personality(
            1.2,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            50,
            20,  # glory
            120,  # social
            140,  # balance
            20,  # loot
            60,  # contracts
            10,  # leadership
            20,  # wealth
            20,  # knowledge
        ),
    'Summoners':
        Personality(
            1.2,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            40,
            80,  # glory
            40,  # social
            20,  # balance
            90,  # loot
            50,  # contracts
            10,  # leadership
            90,  # wealth
            180,  # knowledge
        ),
    'Necromancers':
        Personality(
            1.1,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            60,
            20,  # glory
            10,  # social
            120,  # balance
            10,  # loot
            10,  # contracts
            0,  # leadership
            60,  # wealth
            100,  # knowledge
        ),
    'Temple':
        Personality(
            1.2,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            50,
            40,  # glory
            80,  # social
            160,  # balance
            40,  # loot
            60,  # contracts
            10,  # leadership
            20,  # wealth
            80,  # knowledge
        ),
    'Church':
        Personality(
            1.2,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            70,
            20,  # glory
            80,  # social
            160,  # balance
            10,  # loot
            10,  # contracts
            20,  # leadership
            40,  # wealth
            10,  # knowledge
        ),
    'Merchants':
        Personality(
            1.1,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            70,
            0,  # glory
            80,  # social
            0,  # balance
            0,  # loot
            0,  # contracts
            0,  # leadership
            100,  # wealth
            0,  # seeks knowledge
        ),
    'Mayoress':
        Personality(
            1.2,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            50,
            40,  # glory
            40,  # social
            40,  # balance
            40,  # loot
            40,  # contracts
            40,  # leadership
            40,  # wealth
            40,  # seeks knowledge
        ),
    'Monster':
        Personality(
            1.2,  # markup
            [],  # motivation
            [],  # perk
            [],  # quirk
            50,
            40,  # glory
            40,  # social
            40,  # balance
            40,  # loot
            40,  # contracts
            40,  # leadership
            40,  # wealth
            40,  # seeks knowledge
        ),
}


####################
## MARKETING / METRICS ##
##############################################################################
## Functions used by heroes to determine where all the 'good' loot is, for instance, also sales behaviour generally ##
##############################################################################

class Metrics:
    def __init__(self, item_sold, item_bought):

        self.item_sold = item_sold
        self.item_bought = item_bought

    def log_item_sold(self, item_type, value, faction, date):
        self.item_sold[faction].append([item_type, value, date])

    def log_item_bought(self, item_type, value, faction, date):
        self.item_bought[faction].append([item_type, value, date])

    def return_sales_number(self, days=10):
        sales = self.item_sold
        sales_count = []

        for faction in active_faction_list():
            relevant_sales = 0
            for item in sales[faction]:
                if item[2] > day_count - days:
                    relevant_sales += 1
            sales_count.append([relevant_sales, faction])

        return sales_count

    def return_purchases_number(self, days=10):
        purchases = self.item_bought
        purchases_count = []

        for faction in active_faction_list():
            relevant_purchases = 0
            for item in purchases[faction]:
                if item[2] > day_count - days:
                    relevant_purchases += 1
            purchases_count.append([relevant_purchases, faction])

        return purchases_count

    def return_purchases_value(self, days=10):
        purchases = self.item_bought
        purchases_value = []

        for faction in active_faction_list():
            relevant_purchases = 0
            for item in purchases[faction]:
                if item[2] > day_count - days:
                    relevant_purchases += item[1]
            purchases_value.append([relevant_purchases, faction])

        return purchases_value

    def return_sales_value(self, days=10):
        sales = self.item_sold
        sales_value = []

        for faction in active_faction_list():
            relevant_sales = 0
            for item in sales[faction]:
                if item[2] > day_count - days:
                    relevant_sales += item[1]
            sales_value.append([relevant_sales, faction])

        return sales_value

    def return_sales_by_item_type(self, item_type, days=10):
        sales = self.item_sold
        sales_item_count = []

        for faction in active_faction_list():
            relevant_sales = 0
            for item in sales[faction]:
                if item[2] > day_count - days:
                    if item_type == item[0]:
                        relevant_sales += 1
            sales_item_count.append([relevant_sales, faction])

        return sales_item_count

    def return_purchases_by_item_type(self, item_type, days=10):
        purchases = self.item_sold  # all sales data available
        purchases_item_count = []  # create a blank list for storing data by faction

        for faction in active_faction_list():  # iterate through existing factions
            relevant_purchases = 0  # start at zero for the faction
            for item in purchases[faction]:  # loop through all the logged sale items
                if item[2] > day_count - days:  # only log recent sales, default 10 days previous
                    if item_type == item[0]:  # if item type matches
                        relevant_purchases += 1  # add one to the counter
            purchases_item_count.append([relevant_purchases,
                                         faction])  # for each faction store the total purchases by item type, for sorting elsewhere

        return purchases_item_count

    def tick(self):
        pass
        # create metrics functions to return data based on sales data.


def active_faction_list():
    active_factions = []

    for shop in shop_list_inc_player:
        active_factions.append(shop[0])

    return active_factions


def shop_count_by_item_type(item_type):  # poll the shops, find the one with the most of one particular kind of item.
    # can be e.g. modified by shop signs (elsewhere)

    shop_item_count = []

    for shops in shop_list_inc_player:
        x = shops[2]
        y = shops[3]

        item_count = 0

        for item in map[x][y].shop.inventory:
            item_index = item[0]
            real_item_type = master_item_list[item_index][9]
            if item_type == real_item_type:
                item_count += 1

        shop_item_count.append([item_count, x, y])  # return the numbers of items and the location of the shop

    return shop_item_count


################################
## Additional Shop Development Information ##
################################

class Shop_Layout:
    def __init__(self, sign, decorations, room_one, room_two):  # set up the basis of the shop layout

        self.sign = sign  # basic marketing modifier
        self.decorations = decorations  # branding modifications, allows for increased prices, perhaps marketing modifiers as well
        self.room_one = room_one  # player will be able to augment shop with additional functions e.g. smithy, brewers, library
        self.room_two = room_two


class Room:
    def __init__(self, type, base_level, resources, owner_name, progress,
                 goal):  # counters etc. for a generic functional room

        self.type = type
        self.base_level = base_level
        self.resources = resources
        self.owner_name = owner_name
        self.progress = progress
        self.goal = goal


################
## MAP FUNCTIONS ##
################

# master_item_list indices: 0_SIMPLE, 1_NAME, 2_BASE_VALUE, 3_LEVEL, 4_ALIGNMENT, 5_ORDER, 6_FACTION, 7_EFFECT, 8_DESCRIPTION, 9_TYPE

def measure_world_evil():  # Is there a neater or more intuitive way to deal with these sorts of variables? Specific class rather than global variables?
    global total_item_evil, evil_counter

    item_count = []
    average_evil = 0

    for shops in shop_list_inc_player:  # find the evilness of the shop items
        x = shops[2]
        y = shops[3]

        for items in map[x][y].shop.inventory:
            item_index = items[0]
            item_evil = master_item_list[item_index][4] * master_item_list[item_index][3]
            average_evil += 50 * master_item_list[item_index][3]
            item_count.append(item_evil)

    for heroes in town_heroes:
        for items in heroes.inventory:
            item_index = items[0]
            item_evil = master_item_list[item_index][4] * master_item_list[item_index][3]
            average_evil += 50 * master_item_list[item_index][3]
            item_count.append(item_evil)

    number_items = len(item_count)

    item_evil = 0

    for items in item_count:
        item_evil += items

    dung_evil_mod = 0

    for dungeons in dungeon_list:
        x = dungeons[2]
        y = dungeons[3]

        mod = measure_dungeon_evil_chaos(x, y)

        dung_evil_mod -= mod[0]

    if item_evil + dung_evil_mod < 1:
        item_evil = 1
    else:
        item_evil += dung_evil_mod

    total_item_evil = (
        (item_evil * 100) / (
        average_evil + item_evil))  # normalised value between 1 - 100 for the total item evil in town

    evil_measure = 50 - total_item_evil
    if evil_measure < 0:
        evil_measure = 0

    evil_counter += evil_measure

    if log_information:
        log_info('The world is ' + str(total_item_evil) + ' percent good - average evil ' + str(
            average_evil) + ' world evil = ' + str(item_evil))


def measure_dungeon_evil_chaos(x, y):
    alignment = map[x][y].dungeon.alignment
    order = map[x][y].dungeon.order

    population = map[x][y].dungeon.population

    chaos = population

    order = (population * (50 - order)) / 5

    return [chaos, order]


def measure_world_chaos():
    global total_item_chaos, chaos_counter

    item_count = []
    average_chaos = 0

    for shops in shop_list_inc_player:  # find the evilness of the shop items
        x = shops[2]
        y = shops[3]

        for items in map[x][y].shop.inventory:
            item_index = items[0]
            item_chaos = master_item_list[item_index][5] * master_item_list[item_index][3]
            average_chaos += 50 * master_item_list[item_index][3]
            item_count.append(item_chaos)

    for heroes in town_heroes:
        for items in heroes.inventory:
            item_index = items[0]
            item_chaos = master_item_list[item_index][5] * master_item_list[item_index][3]
            average_chaos += 50 * master_item_list[item_index][3]
            item_count.append(item_chaos)

    number_items = len(item_count)

    item_chaos = 0

    for items in item_count:
        item_chaos += items

        # normalised value between 1 - 100 for the total item evil in town

    dung_chaos_mod = 0

    for dungeons in dungeon_list:
        x = dungeons[2]
        y = dungeons[3]

        mod = measure_dungeon_evil_chaos(x, y)

        dung_chaos_mod -= mod[1]

    if item_chaos + dung_chaos_mod < 1:
        item_chaos = 1
    else:
        item_chaos += dung_chaos_mod

    total_item_chaos = ((item_chaos * 100) / (average_chaos + item_chaos))

    chaos_measure = 50 - total_item_chaos
    if chaos_measure < 0:
        chaos_measure = 0

    chaos_counter += chaos_measure

    if log_information:
        log_info('The world is ' + str(total_item_chaos) + ' percent lawful - average order ' + str(
            average_chaos) + ' world order = ' + str(item_chaos))


def check_world_chaos():
    global chaos_counter

    chaos_event_rate = len(dungeon_list) * base_chaos_event_rate

    if chaos_counter > chaos_event_rate:
        chaos_counter = 0

        if len(inactive_sites) > 0:
            location = extract_random_from_list(inactive_sites)

            x = location[0]
            y = location[1]

            commission_dungeon(x, y)

            message('New Dungeon! The ' + map[x][y].name + ' has arisen from the forest!', libtcod.red,
                    libtcod.dark_red)


def check_world_evil():
    global evil_counter
    if evil_counter > evil_event_rate:
        evil_counter = 0

        if len(dungeon_list) > 0:
            dungeon_spawn = pick_random_from_list(dungeon_list)
            level = dungeon_spawn[0]
            name = dungeon_spawn[1]
            x = dungeon_spawn[2]
            y = dungeon_spawn[3]

            spawn_monster(x, y, level)


def tax_man_cometh():
    img = libtcod.image_load('gfx/game_over.png')

    while not libtcod.console_is_window_closed():
        # show the background image, at twice the regular console resolution
        libtcod.image_blit_2x(img, 0, 0, 0)

        # show options and wait for the player's choice
        choice = menu('THE TAX MAN COMETH', ['exit', 'view Hi-Score'], 24)

        if choice == 0:
            break
        elif choice == 1:
            hi_score()


def end_game_monster_destruction():
    img = libtcod.image_load('gfx/monster.png')

    while not libtcod.console_is_window_closed():
        # show the background image, at twice the regular console resolution
        libtcod.image_blit_2x(img, 0, 0, 0)

        # show options and wait for the player's choice
        choice = menu('YOU ARE DESTROYED!', ['exit', 'view Hi-Score'], 24)

        if choice == 0:
            break
        elif choice == 1:
            hi_score()


def check_finances():
    if player.wealth < 0:
        tax_man_cometh()
        clear_savegame()
        sys.exit()
    else:
        pass


def set_tax_rate():
    global tax_rate
    tax_chaos_modifier = 50 - total_item_chaos

    tax_rate = 25 - tax_chaos_modifier
    if tax_rate < 1:
        tax_rate = 1


def assess_town_demand():  # used to see what items are most required

    item_split = {}
    item_count = []

    for shops in shop_list_inc_player:
        x = shops[2]
        y = shops[3]

        for items in map[x][y].shop.inventory:
            item_index = items[0]
            item_type = master_item_list[item_index][9]
            item_count.append(item_type)

    item_split = {x: item_count.count(x) for x in item_count}

    item_type_in_demand = min(item_split.iteritems(), key=operator.itemgetter(1))[0]

    if log_information:
        log_info(str(item_type_in_demand) + ' seem to be in demand in town ...')

    return item_type_in_demand


def build_ecosystems():
    global ecosystems, max_monster_level
    # 'orc': {level:1, power:2, description:'A large, green humanoid with a snarl.', population:100, align:40, order:45},
    # typical monster entry

    # this function pregenerates leveled lists of monsters, with corresponding relative chances of appearing
    # all for use by other generators

    # find out what the highest level monster is
    monster_levels = []
    for mname, mtype in master_monster_list.iteritems():
        monster_levels.append(mtype['level'])

    levels_sorted = sorted(monster_levels)

    max_monster_level = levels_sorted[-1]

    for z in range(0, max_monster_level + 1,
                   1):  # do a loop for every level of creature there is (also giving us a key for that level)
        population_distribution = []  # reset the population distribution every level
        population_range = 0  # and the range
        for x, y in master_monster_list.iteritems():
            if y['level'] == z:  # our monster is 'in level'
                population_range += y['population']  # add the relative population range on to this measure
                population_distribution.append([x, population_range])  # add key and population range to the list
        # we now have a generated list of baddies for level z, so we add this to the ecosystems
        ecosystems[
            z] = population_distribution  # so key 1:[[medium rarity, 100],[common,300],[rare,305]] or something ...
        # and we can link back to the master monster list by key quite easily ...

    if log_information:
        log_info('Ecosystem built: ' + str(ecosystems))


def decommission_dungeon(x, y):
    global map
    global inactive_sites

    name = map[x][y].name

    map[x][y].dungeon = None
    # need to also add the dungeon back in to the list of inactive sites
    inactive_sites.append([x, y])
    # set color appropriately
    map[x][y].color = [0, 85, 0, 135, 210, 90]
    # also we need to send all the heroes home
    for hero in town_heroes:
        h_x = hero.x
        h_y = hero.y

        if [h_x, h_y] == [x, y]:  # is the hero here?
            hero.in_dungeon = 0  # kick him out of the dungeon
            hero.go_home()  # send him home
            # hero.undress_thineself()

    map_dungeons()

    null_contracts = []

    for contract in the_mayoress.noticeboard.notices:
        if contract.target_name == name:
            null_contracts.append(contract)

    if len(null_contracts) > 0:
        for contract in null_contracts:
            the_mayoress.noticeboard.notices.remove(contract)


def commission_dungeon(x, y):  # new dungeon, set currently to start up a new 'starter dungeon'
    global map
    global inactive_sites

    location = [x, y]
    if ' ' not in map[x][y].name:
        # this dungeon hasn't been named previously
        dungeon_legend = map[location[0]][location[1]].legend
        dungeon_name = name_active_dungeon(location)
    else:
        dungeon_legend = map[location[0]][location[1]].legend
        dungeon_name = map[location[0]][location[1]].name

    for dtype in dungeon_type_list:
        if dtype[0] in map[location[0]][location[1]].name:
            dungeon_type = dtype[2]

    starter_dungeon = Dungeon(generate_inventory(60, 75, 1, 4), libtcod.random_get_int(0, 1000, 1600), 1,
                              Reputation(0, blank_faction_relations()),
                              libtcod.random_get_int(0, min_dungeon_pop, max_dungeon_pop), 45, 45, {}, dungeon_type)
    # build_dungeon(x, y, dungeon_name, leg, dungeon)
    build_dungeon(location[0], location[1], dungeon_name, dungeon_legend, starter_dungeon)

    # inactive_sites.remove(location) #this site is no longer inactive, but we should extract it before we enter this function

    map_dungeons()


def return_dungeon_location_by_name(dungeon_name):
    for dungeon in dungeon_list:
        if dungeon[1] == dungeon_name:
            level = dungeon[0]
            name = dungeon[1]
            x = dungeon[2]
            y = dungeon[3]
            return [level, name, x, y]


def generate_encounter(level_min, level_max, pop_low, pop_high):
    global max_monster_level
    # function to generate a population of critters to sit in a dungeon, waiting to be squashed.

    if level_max > max_monster_level:  # (trying to limit errors)
        level_max = max_monster_level

    # how many monsters in this group?
    popul = libtcod.random_get_int(0, pop_low, pop_high) + 1

    if log_information:
        log_info(str(popul) + ' monsters about to be generated.')

    encounter = []

    for n in range(popul):  # one loop for each creature
        # decide on a level for this critter:
        level = libtcod.random_get_int(0, level_min, level_max)
        tot_pop = ecosystems[level][-1][1]

        creature_selector = libtcod.random_get_int(0, 0, tot_pop)

        for z in range(len(ecosystems[level])):
            if creature_selector < ecosystems[level][z][1]:
                encounter.append(ecosystems[level][z][0])  # add the key info (creature name) to this group
                break

    if log_information:
        log_info('Logging generated encounter: ' + str(encounter))

    return encounter


def distance_measure(here_x, here_y, there_x, there_y):
    b_squared = (here_x - there_x) ** 2
    c_squared = (here_y - there_y) ** 2

    distance = (b_squared + c_squared) ** 0.5

    return distance


def new_random_map():
    global map
    global player
    global inactive_sites  # a list of x,y coordinates for inactive dungeons

    # fill map with "default" tiles - The Forest around the edge
    map = [[Tile(False, False, 'Neutral', 'Forest', '&', None, None, [0, 85, 0, 45, 125, 0], )
            for y in range(MAP_HEIGHT)]
           for x in range(MAP_WIDTH)]

    # fill inner area with 'scrubland'

    INNER_RADIUS = MAP_WIDTH / 2.5  # only works for square map ... ok for now
    INNER_START_X = MAP_WIDTH / 8
    INNER_END_X = (MAP_WIDTH / 8) * 7
    INNER_START_Y = MAP_HEIGHT / 8
    INNER_END_Y = (MAP_HEIGHT / 8) * 7

    TOWN_CENTRE_Y = 20
    TOWN_CENTRE_X = 20

    for y in range(INNER_START_Y, INNER_END_Y):
        for x in range(INNER_START_X, INNER_END_X):
            if distance_measure(x, y, TOWN_CENTRE_X, TOWN_CENTRE_Y) - 0.5 < INNER_RADIUS:
                map[x][y].blocked = False
                map[x][y].block_sight = False
                map[x][y].faction = 'Neutral'
                map[x][y].name = 'Scrub'
                map[x][y].legend = ';'
                map[x][y].shop = None
                map[x][y].dungeon = None
                map[x][y].color = [0, 115, 0, 115, 200, 0]

    # fill town area with "grass" tiles - a circular region in the middle of the map

    RADIUS = MAP_WIDTH / 4  # only works for square map ... ok for now
    TOWN_START_X = MAP_WIDTH / 4
    TOWN_END_X = MAP_WIDTH / 4 * 3
    TOWN_START_Y = MAP_HEIGHT / 4
    TOWN_END_Y = MAP_HEIGHT / 4 * 3

    TOWN_CENTRE_Y = MAP_HEIGHT / 2
    TOWN_CENTRE_X = MAP_WIDTH / 2

    for y in range(TOWN_START_Y, TOWN_END_Y):
        for x in range(TOWN_START_X, TOWN_END_X):
            if distance_measure(x, y, TOWN_CENTRE_X, TOWN_CENTRE_Y) + 0.5 < RADIUS:
                map[x][y].blocked = False
                map[x][y].block_sight = False
                map[x][y].faction = 'Neutral'
                map[x][y].name = 'Grass'
                map[x][y].legend = ','
                map[x][y].shop = None
                map[x][y].dungeon = None
                map[x][y].color = [15, 135, 15, 135, 210, 10]

    # place the main roads

    MAIN_NORTH_SOUTH = libtcod.random_get_int(0, TOWN_CENTRE_Y - 1, TOWN_CENTRE_Y + 2)
    MAIN_EAST_WEST = libtcod.random_get_int(0, TOWN_CENTRE_X - 1, TOWN_CENTRE_X + 2)

    STREET_V_LENGTH = TOWN_END_Y - TOWN_START_Y - 1
    STREET_H_LENGTH = TOWN_END_X - TOWN_START_X - 1

    create_street_v(MAIN_NORTH_SOUTH, TOWN_START_Y + 1, STREET_V_LENGTH)  # start_x, start_y, length
    create_street_h(TOWN_START_X + 1, MAIN_EAST_WEST, STREET_H_LENGTH)

    create_street_v(MAIN_NORTH_SOUTH, 0, 11, 'path')
    create_street_v(MAIN_NORTH_SOUTH, TOWN_END_Y, 10, 'path')

    create_street_h(0, MAIN_EAST_WEST, 11, 'path')
    create_street_h(TOWN_END_X, MAIN_EAST_WEST, 10, 'path')

    # including some stones at the town entrances to the town.
    build(MAIN_NORTH_SOUTH - 1, TOWN_START_Y + 1, 'Neutral', 'North Stone', '^', None)
    build(MAIN_NORTH_SOUTH + 1, TOWN_START_Y + 1, 'Neutral', 'North Stone', '^', None)
    build(MAIN_NORTH_SOUTH - 1, TOWN_END_Y - 1, 'Neutral', 'South Stone', '^', None)
    build(MAIN_NORTH_SOUTH + 1, TOWN_END_Y - 1, 'Neutral', 'South Stone', '^', None)

    build(TOWN_START_X + 1, MAIN_EAST_WEST - 1, 'Neutral', 'West Stone', '^', None)
    build(TOWN_START_X + 1, MAIN_EAST_WEST + 1, 'Neutral', 'West Stone', '^', None)
    build(TOWN_END_X - 1, MAIN_EAST_WEST - 1, 'Neutral', 'East Stone', '^', None)
    build(TOWN_END_X - 1, MAIN_EAST_WEST + 1, 'Neutral', 'East Stone', '^', None)

    # place smaller roads - 3 - 4 emanating upwards / downwards / left / right from each main road.? Settle for a circular ring of paths

    create_street_v(MAIN_NORTH_SOUTH + 4, TOWN_START_Y + 4, STREET_V_LENGTH - 6, 'path')  # start_x, start_y, length
    create_street_v(MAIN_NORTH_SOUTH - 4, TOWN_START_Y + 4, STREET_V_LENGTH - 6, 'path')
    create_street_h(TOWN_START_X + 4, MAIN_EAST_WEST + 4, STREET_H_LENGTH - 6, 'path')
    create_street_h(TOWN_START_X + 4, MAIN_EAST_WEST - 4, STREET_H_LENGTH - 6, 'path')

    # place the auction house
    location_n = libtcod.random_get_int(0, 0, 1)
    location_e = libtcod.random_get_int(0, 0, 1)

    if location_e == 0:
        ah_x = MAIN_NORTH_SOUTH + 1
    else:
        ah_x = MAIN_NORTH_SOUTH - 1

    if location_n == 0:
        ah_y = MAIN_EAST_WEST + 1
    else:
        ah_y = MAIN_EAST_WEST - 1

    empty_layout = Shop_Layout('None', [], Room('Empty', 0, 0, 'None', 0, []), Room('Empty', 0, 0, 'None', 0, []))

    auction_house_owner_name = name_actor()
    build(ah_x, ah_y, 'Merchants', 'Auction House', '$',
          Store(generate_inventory(13, 24, 1, 5), 1500, 1, Reputation(0, blank_faction_relations()),
                auction_house_owner_name, {'history': []}, empty_layout))

    # build some foundations for the shops and houses etc. to place themselves on, then add these positions to a list aftwerwards.

    # iterate across the main streets, up and down two or three times doing either above or below the street (if scrub)
    for iterate in range(2):
        for plot_x in range(TOWN_START_X, STREET_H_LENGTH + TOWN_START_X):
            plot_y_test = libtcod.random_get_int(0, 0, 1)
            if plot_y_test == 0:
                if map[plot_x][MAIN_EAST_WEST + 1].name == 'Grass':
                    map[plot_x][MAIN_EAST_WEST + 1].name = 'Foundation'
                    map[plot_x][MAIN_EAST_WEST + 1].legend = 'x'
            else:
                if map[plot_x][MAIN_EAST_WEST - 1].name == 'Grass':
                    map[plot_x][MAIN_EAST_WEST - 1].name = 'Foundation'
                    map[plot_x][MAIN_EAST_WEST - 1].legend = 'x'

    for iterate in range(2):
        for plot_y in range(TOWN_START_Y, STREET_V_LENGTH + TOWN_START_Y):
            plot_x_test = libtcod.random_get_int(0, 0, 1)
            if plot_x_test == 0:
                if map[MAIN_NORTH_SOUTH + 1][plot_y].name == 'Grass':
                    map[MAIN_NORTH_SOUTH + 1][plot_y].name = 'Foundation'
                    map[MAIN_NORTH_SOUTH + 1][plot_y].legend = 'x'
            else:
                if map[MAIN_NORTH_SOUTH - 1][plot_y].name == 'Grass':
                    map[MAIN_NORTH_SOUTH - 1][plot_y].name = 'Foundation'
                    map[MAIN_NORTH_SOUTH - 1][plot_y].legend = 'x'

    foundations = []
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if map[x][y].name == 'Foundation':
                foundations.append([x, y])

    # place the players shop
    player = Store([], 125, 1, Reputation(0, blank_faction_relations()), player_name, {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], player_name, 'Players Shop', '#', player)

    # place the shops for the rest of the guilds

    thief_store = Store(basic_inventory(), 3000, 2, Reputation(0, blank_faction_relations()), 'Kilian Derva',
                        {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], 'Thieves', 'Thief Den', '?', thief_store)

    assassin_store = Store(basic_inventory(), 10000, 8, Reputation(0, blank_faction_relations()), 'Styl Marck',
                           {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], 'Assassins', 'The Black House', '+', assassin_store)

    swashbuckler_store = Store(basic_inventory(), 1500, 2, Reputation(0, blank_faction_relations()), 'Gudrun Steiner',
                               {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], 'Swashbucklers', 'The Mermaids Wish', 'v', swashbuckler_store)

    fighter_store = Store(basic_inventory(), 1000, 1, Reputation(0, blank_faction_relations()), 'Red Dog Muldrake',
                          {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], 'Fighters', 'Guild of Tactics', 'x', fighter_store)

    barbarian_store = Store(basic_inventory(), 250, 2, Reputation(0, blank_faction_relations()), 'Oldran',
                            {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], 'Barbarians', 'Goatskin Teepee', '^', barbarian_store)

    summoner_store = Store(basic_inventory(), 1150, 3, Reputation(0, blank_faction_relations()), 'Ha-grey',
                           {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], 'Summoners', 'Altar of Hope', '}', summoner_store)

    mage_store = Store(basic_inventory(), 1100, 4, Reputation(0, blank_faction_relations()), 'Firo Gradion',
                       {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], 'Mages Guild', 'Honoured Gate', 'z', mage_store)

    temple_store = Store(basic_inventory(), 1300, 3, Reputation(0, blank_faction_relations()), 'Piotr Serviz',
                         {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], 'Temple', 'The Temple of Fred', '+', temple_store)

    church_store = Store(basic_inventory(), 1200, 2, Reputation(0, blank_faction_relations()), 'Min Bo Lim',
                         {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], 'Church', 'Unity Church', '+', church_store)

    druid_store = Store(basic_inventory(), 100, 1, Reputation(0, blank_faction_relations()), 'Fire-Tooth',
                        {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], 'Druids', 'Ever Glade', '#', druid_store)

    necromancer_store = Store(basic_inventory(), 600, 2, Reputation(0, blank_faction_relations()), 'Herbert West',
                              {'history': []}, empty_layout)
    location = extract_random_from_list(foundations)
    if location:
        build(location[0], location[1], 'Necromancers', 'Darkmere', 'K', necromancer_store)


        # put down some flavour stuff in the town
    number_buildings = len(foundations)
    for n in range(number_buildings):
        type = libtcod.random_get_int(0, 0, 1)
        if type == 0:
            location = extract_random_from_list(foundations)
            if location:
                build(location[0], location[1], 'Neutral', 'Townhouse', '*', None)
        else:
            location = extract_random_from_list(foundations)
            if location:
                build(location[0], location[1], 'Neutral', 'Shack', '/', None)

    # Place down some potential dungeons
    inactive_sites = []

    number_sites = libtcod.random_get_int(0, 18, 22)

    for iterate in range(number_sites):
        horiz_vert = libtcod.random_get_int(0, 0, 1)  # shall we go for a horizontal bit?
        this_that = libtcod.random_get_int(0, 0, 1)  # which side of the map? (top / bottom / left / right)

        if horiz_vert == 0:  # go for a horizontal bit
            x = libtcod.random_get_int(0, 1, MAP_WIDTH - 2)
            if this_that == 0:  # go for the top of the map
                y = libtcod.random_get_int(0, 1, TOWN_START_Y - 3)
                if map[x][y].name == 'Forest':
                    map[x][y].name = 'Inactive Site'
                    map[x][y].legend = 'x'
                    map[x][y].color = [0, 85, 0, 135, 210, 90]
            else:
                y = libtcod.random_get_int(0, TOWN_END_Y + 3, MAP_HEIGHT - 2)
                if map[x][y].name == 'Forest':
                    map[x][y].name = 'Inactive Site'
                    map[x][y].legend = 'x'
                    map[x][y].color = [0, 85, 0, 135, 210, 90]
        else:  # vertical slices either side
            y = libtcod.random_get_int(0, 1, MAP_HEIGHT - 2)
            if this_that == 0:  # go for the left of the map
                x = libtcod.random_get_int(0, 1, TOWN_START_X - 3)
                if map[x][y].name == 'Forest':
                    map[x][y].name = 'Inactive Site'
                    map[x][y].legend = 'x'
                    map[x][y].color = [0, 85, 0, 135, 210, 90]
            else:
                x = libtcod.random_get_int(0, TOWN_END_X + 3, MAP_WIDTH - 2)
                if map[x][y].name == 'Forest':
                    map[x][y].name = 'Inactive Site'
                    map[x][y].legend = 'x'
                    map[x][y].color = [0, 85, 0, 135, 210, 90]

    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if map[x][y].name == 'Inactive Site':
                inactive_sites.append([x, y])

    for x in inactive_sites:  # now turn the random list of sites in to keeps crypts etc.
        type = pick_random_from_list(dungeon_type_list)
        map[x[0]][x[1]].name = type[0]
        map[x[0]][x[1]].legend = type[1]
        # map[x][y].color = [ 0, 85, 0 , 135, 210, 10 ]

    # location = extract_random_from_list(inactive_sites)
    # dungeon_legend = map[location[0]][location[1]].legend
    # dungeon_name = name_active_dungeon(location)
    # starter_dungeon = Dungeon(generate_inventory(60, 75, 1, 4), 1600, 1, Reputation(0, blank_faction_relations()), libtcod.random_get_int(0, 250, 300), 45, 45)
    # build_dungeon(x, y, dungeon_name, leg, dungeon)
    # build_dungeon(location[0], location[1], dungeon_name, dungeon_legend, starter_dungeon)

    number_of_starter_dungeons = 3

    for n in range(number_of_starter_dungeons):
        location = extract_random_from_list(inactive_sites)
        commission_dungeon(location[0], location[1])

        # location = extract_random_from_list(inactive_sites)
        # dungeon_legend = map[location[0]][location[1]].legend
        # dungeon_name = name_active_dungeon(location)
        # level2_dungeon = Dungeon(generate_inventory(80, 100, 1, 5), 2400, 2, Reputation(0, blank_faction_relations()), libtcod.random_get_int(0, 400, 600), 40, 40)
        # build_dungeon(location[0], location[1], dungeon_name, dungeon_legend, level2_dungeon)

        # location = extract_random_from_list(inactive_sites)
        # dungeon_legend = map[location[0]][location[1]].legend
        # dungeon_name = name_active_dungeon(location)
        # level3_dungeon = Dungeon(generate_inventory(95, 125, 1, 6), 4000, 3, Reputation(0, blank_faction_relations()), libtcod.random_get_int(0, 550, 750), 45, 45)
        # build_dungeon(location[0], location[1], dungeon_name, dungeon_legend, level3_dungeon)


def name_active_dungeon(location):
    # dungeon_class(self, inventory, wealth, base_level, reputation, population, alignment, order):
    suf_pre = libtcod.random_get_int(0, 0, 1)
    if suf_pre == 0:
        suffix = pick_random_from_list(nasty_things_suffixes)
        dungeon_name = map[location[0]][location[1]].name + ' of ' + suffix
        return dungeon_name
    else:
        prefix = pick_random_from_list(nasty_things_prefixes)
        dungeon_name = prefix + ' ' + map[location[0]][location[1]].name
        return dungeon_name


def pick_random_from_list(list):
    list_length = len(list)

    if list_length > 0:
        item = libtcod.random_get_int(0, 0, list_length) - 1
        returned_item = list[item]
        return returned_item
    else:
        return False


def extract_random_from_list(list):
    list_length = len(list)

    if list_length > 0:
        item = libtcod.random_get_int(0, 0, list_length) - 1
        returned_item = list.pop(item)
        return returned_item
    else:
        return False


def make_map():
    global map
    global player

    new_random_map()

    twinkle(4)  # add marginal variance to the colours


def find_shop_by_faction(faction):
    x = 0
    y = 0

    # this function finds a shop, by faction, and returns the x and y locations as a two part list.
    # If there are two faction shops in the town, it returns a random one of those two.

    possible_destinations = []

    for shop in shop_list_inc_player:
        if shop[0] == faction:
            possible_destinations.append(shop)

    # now we have a list of possible venues.
    if len(possible_destinations) > 0:
        faction_destination = libtcod.random_get_int(0, 0, len(possible_destinations) - 1)

        shop = possible_destinations[faction_destination]

        x = shop[2]
        y = shop[3]
        return [x, y]
    else:
        return False


def set_glow():
    global glow_map

    glow_map = [[[0, 0, 0] for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]  # create a blank glow map

    delta_glow = 4  # brightness of glows

    for shops in shop_list_inc_player:
        x = shops[2]
        y = shops[3]

        level = map[x][y].shop.base_level + 1
        minus_level = map[x][y].shop.base_level * -1

        for glow in range(minus_level, level):
            minus_level_glow = glow * -1
            level_glow = glow
            for m in range(minus_level_glow, level_glow):
                for n in range(minus_level_glow, level_glow):
                    if x + m > 0 and x + m < VIEWPORT_WIDTH:  # valid x coord
                        if y + n > 0 and y + n < VIEWPORT_HEIGHT:  # valid y coord
                            glow_map[x + m][y + n][0] += delta_glow
                            glow_map[x + m][y + n][1] += delta_glow
                            glow_map[x + m][y + n][2] += delta_glow  # apply to glow_map
        glow_map[x][y][0] = 0
        glow_map[x][y][1] = 0
        glow_map[x][y][2] = 0

    for heroes in town_heroes:
        x = heroes.x
        y = heroes.y

        for glow in range(-2, 3):
            minus_level_glow = glow * -1
            level_glow = glow + 1
            for m in range(minus_level_glow, level_glow):
                for n in range(minus_level_glow, level_glow):
                    if x + m > 0 and x + m < VIEWPORT_WIDTH:  # valid x coord
                        if y + n > 0 and y + n < VIEWPORT_HEIGHT:  # valid y coord
                            glow_map[x + m][y + n][0] += heroes.base_level
                            glow_map[x + m][y + n][1] += heroes.base_level
                            glow_map[x + m][y + n][2] += heroes.base_level + 1
        glow_map[x][y][0] = 0
        glow_map[x][y][1] = 0
        glow_map[x][y][2] = 0

    for monster in monster_list:
        x = monster.x
        y = monster.y

        for glow in range(-2, 3):
            minus_level_glow = glow * -1
            level_glow = glow + 1
            for m in range(minus_level_glow, level_glow):
                for n in range(minus_level_glow, level_glow):
                    if x + m > 0 and x + m < VIEWPORT_WIDTH:  # valid x coord
                        if y + n > 0 and y + n < VIEWPORT_HEIGHT:  # valid y coord
                            glow_map[x + m][y + n][0] += (monster.base_level + 1) * delta_glow
                            glow_map[x + m][y + n][1] += monster.base_level * delta_glow
                            glow_map[x + m][y + n][2] += monster.base_level * delta_glow
                            # glow_map[x][y][0] = 0
                            # glow_map[x][y][1] = 0
                            # glow_map[x][y][2] = 0

    for dungeons in dungeon_list:
        x = dungeons[2]
        y = dungeons[3]

        level = map[x][y].dungeon.base_level + 1
        minus_level = map[x][y].dungeon.base_level * -1

        for glow in range(minus_level, level):  # glow based on level
            minus_level_glow = glow * -1
            level_glow = glow + 1
            for m in range(minus_level_glow, level_glow):
                for n in range(minus_level_glow, level_glow):
                    if x + m > 0 and x + m < VIEWPORT_WIDTH:  # valid x coord
                        if y + n > 0 and y + n < VIEWPORT_HEIGHT:  # valid y coord
                            glow_map[x + m][y + n][0] += delta_glow * 4
                            glow_map[x + m][y + n][1] -= delta_glow
                            glow_map[x + m][y + n][2] -= delta_glow  # apply to glow_map
        glow_map[x][y][0] = 0
        glow_map[x][y][1] = 0
        glow_map[x][y][2] = 0


def twinkle(delta):
    global map
    # causes a random fluctuation of the displayed colour of the map
    for y in range(VIEWPORT_HEIGHT):  # go through map
        for x in range(VIEWPORT_WIDTH):

            deltaminus = (delta * -1)

            dbgR = libtcod.random_get_int(0, deltaminus, delta)
            dbgG = libtcod.random_get_int(0, deltaminus, delta)
            dbgB = libtcod.random_get_int(0, deltaminus, delta)

            if map[x][y].color[0] > 5 and map[x][y].color[0] < 250:
                map[x][y].color[0] += dbgR
            if map[x][y].color[1] > 5 and map[x][y].color[0] < 250:
                map[x][y].color[1] += dbgG
            if map[x][y].color[2] > 5 and map[x][y].color[0] < 250:
                map[x][y].color[2] += dbgB

            bgR = map[x][y].color[0]
            bgG = map[x][y].color[1]
            bgB = map[x][y].color[2]

            libtcod.console_set_back(con, x, y, libtcod.Color(bgR, bgG, bgB), libtcod.BKGND_SET)


def find_shop(faction_shop):
    global shop_list

    x = 0
    y = 0

    # this function finds a shop, by name only, and returns the x and y locations as a two part list

    for shops in shop_list:
        if shops[1] == faction_shop:
            x = shops[2]
            y = shops[3]
            return [x, y]
    return False


def map_dungeons():
    global map
    global dungeon_list

    # clear the current list of dungeons
    dungeon_list = []

    # check the map for tiles that contain dungeons
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if map[x][y].dungeon:
                # add the details of level, name, and dungeon location to the list, for interrogation elsewhere
                dungeon_list.append([map[x][y].dungeon.base_level, map[x][y].name, x, y])


def map_shops():
    global map
    global shop_list

    # clear the current list of shops
    shop_list = []

    # check the map for tiles that contain shops
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if map[x][y].shop:
                # add the details of faction, name, and shop location to the list, for interrogation elsewhere
                shop_list.append([map[x][y].faction, map[x][y].name, x, y])


def create_street_h(start_x, start_y, length, type='street'):
    for x in range(start_x, start_x + length):
        if type == 'street':
            map[x][start_y].name = 'Street'
            if map[x][start_y].legend == ':':
                map[x][start_y].legend = '+'
            else:
                map[x][start_y].legend = '-'
            # color for background RGB foreground RGB
            # streets are dark grey background, light grey 'text'
            map[x][start_y].color = [45, 45, 45, 155, 155, 155]
        elif type == 'path':
            if map[x][start_y].name == 'Street':
                pass
            else:
                map[x][start_y].name = 'Path'
                if map[x][start_y].legend == ':':
                    map[x][start_y].legend = '+'
                else:
                    map[x][start_y].legend = '-'
                # color for background RGB foreground RGB
                # paths are dusky brown, light grey 'text'
                map[x][start_y].color = [115, 85, 25, 95, 95, 95]


def create_street_v(start_x, start_y, length, type='street'):
    for y in range(start_y, start_y + length):
        if type == 'street':
            map[start_x][y].name = 'Street'
            if map[start_x][y].legend == '-':
                map[start_x][y].legend = '+'
            else:
                map[start_x][y].legend = ':'
            # color for background RGB foreground RGB
            # streets are dark grey background, light grey 'text'
            map[start_x][y].color = [45, 45, 45, 155, 155, 155]
        elif type == 'path':
            if map[start_x][y].name == 'Street':
                pass
            else:
                map[start_x][y].name = 'Path'
                if map[start_x][y].legend == '-':
                    map[start_x][y].legend = '+'
                else:
                    map[start_x][y].legend = ':'
                # color for background RGB foreground RGB
                # paths are dusky brown, darker 'text'
                map[start_x][y].color = [115, 85, 25, 95, 95, 95]


def build(x, y, faction_name, shop_name, leg, shop):
    # helper function to create solid blocks to act as shops on the town map
    map[x][y].blocked = True
    map[x][y].block_sight = True
    map[x][y].faction = faction_name
    map[x][y].name = shop_name
    map[x][y].legend = leg
    map[x][y].shop = shop
    # color for background RGB foreground RGB
    # shops are blue background, grey text
    if map[x][y].shop:
        if map[x][y].faction == player_name:
            map[x][y].color = [195, 195, 25, 175, 85, 175]
        else:
            map[x][y].color = [25, 25, 135, 175, 175, 85]

    else:
        map[x][y].color = [20, 85, 65, 125, 125, 125]


def destroy_shop(x, y):
    global auction_item

    if map[x][y].shop == player:
        end_game_monster_destruction()
        clear_savegame()
        sys.exit()

    if map[x][y].name == 'Auction House':
        auction_item = None

    map[x][y].faction = 'Neutral'
    map[x][y].name = 'Rubble'
    map[x][y].legend = '%'
    map[x][y].shop = None
    map[x][y].color = [95, 25, 25, 175, 85, 85]


def build_dungeon(x, y, dungeon_name, leg, dungeon):
    # helper function to define a dungeon
    map[x][y].blocked = True
    map[x][y].block_sight = True
    map[x][y].name = dungeon_name
    map[x][y].legend = leg
    map[x][y].dungeon = dungeon
    # color for background RGB foreground RGB
    # dungeons are red background, grey text
    map[x][y].color = [135, 25, 25, 125, 125, 125]


def birth_hero(gender='m', level=1, faction='Random'):
    global hero_list

    if faction == 'Random':
        faction = get_random_faction()

    new_brain = Brain([], default_personality[faction], [], 0, 'Phase_0')

    new_hero = Hero(
        generate_inventory(1, 3 + level, 1, 2 + level, faction),
        # inventory, from 1 to 3 items, level 1 to 3, faction related.
        {'armor': 0, 'clothing': 0, 'weapon': 0},  # equipment,
        libtcod.random_get_int(0, 100, 200) + level * 75,  # wealth,
        level,  # base_level,
        Reputation(0, blank_faction_relations()),  # reputation,
        {'perceived': 0, 'real': 0, 'perceived_clothing': 0, 'perceived_weapon': 0, 'perceived_armor': 0},  # stats,
        faction,  # faction,
        1,  # x,
        1,  # y,
        -1,  # itch,
        0,  # in_dungeon,
        name_actor(gender),  # name,
        libtcod.random_get_int(0, 21, 45),  # age,
        {'current': hero_base_hp + (level * hero_base_hp_level_gain),
         'max': hero_base_hp + (level * hero_base_hp_level_gain)},
        # hp - current / max
        [],  # wounds,
        new_brain,  # brain
        50,  # alignment,
        50,  # order
        {'history': [], 'kills': [], 'visit_history': [], 'contract_cargo': []},  # activitylog
        None  # owner_name HACK SORRY
    )

    hero_list.append(new_hero)


def spawn_monster(x, y, base_level):
    if len(monster_list) < maximum_monsters:
        name = name_monster()

        new_brain = Brain([], default_personality['Monster'], [], 0, 0)

        new_monster = Hero(
            [],
            {'armor': 0, 'clothing': 0, 'weapon': 0},  # equipment,
            libtcod.random_get_int(0, 100 * base_level, 200 * base_level),  # wealth,
            1,  # base_level,
            Reputation(0, blank_faction_relations()),  # reputation,
            {'perceived': monster_base_strength * base_level, 'real': monster_base_strength * base_level},  # stats,
            'Neutral',  # faction,
            x,  # x,
            y,  # y,
            -1,  # itch,
            0,  # in_dungeon,
            name,  # name,
            libtcod.random_get_int(0, 200, 1200),  # age,
            {'current': monster_base_hp * base_level, 'max': monster_base_hp * base_level},  # hp - current / max
            [],  # wounds,
            new_brain,
            # personality, limited at the minute ... should randomise this for cool monster behaviour, tie name in to the personality
            45,  # alignment,
            45,  # order
            {'history': [], 'kills': [], 'visit_history': [], 'contract_cargo': []},  # activitylog
            None  # owner_name HACK SORRY
        )

        monster_list.append(new_monster)

        message(name + ' has spawned from the ' + map[x][y].name + '!', libtcod.red, libtcod.dark_red)


#################
## ITEM FUNCTIONS  ##
#################

def item_experience(item):
    index = item[0]
    level = master_item_list[index][3]
    quality = item[1][0]
    bonus = item[2][0]

    return level + quality + bonus


def generate_inventory(min_items, max_items, min_level, max_level,
                       faction='all'):  # note not enough items to reliably generate faction specific items yet

    items = []

    for z in range(libtcod.random_get_int(0, min_items, max_items)):
        items.append(create_item(min_level, max_level, faction))

    return items


def basic_inventory():
    items = []

    for z in range(libtcod.random_get_int(0, 6, 12)):
        items.append(create_item(1, 3, 'all'))

    return items


def create_item(level_low, level_hi, faction, type='all', alignment='all',
                order='all'):  # send level bounds and faction to this function
    # [index, quality, bonus, effect, bought_value, set_value, cursed]
    item_got = 0
    iterations = 0
    while item_got == 0:  # go through the list and find an item that matches the requirements
        iterations += 1
        index = libtcod.random_get_int(0, 0, len(master_item_list) - 1)
        if master_item_list[index][3] >= level_low and master_item_list[index][3] <= level_hi:
            if faction == 'all' or faction in master_item_list[index][6]:  # faction match
                if type == 'all' or type in master_item_list[index][9]:  # type match
                    # this function is currently alignment / order independent
                    # we have satisfied all the precursors, so lets find bonuses etc. and insert the item
                    # quality
                    value_mod = 0
                    quality = libtcod.random_get_int(0, 0, 100)
                    if quality <= 50:
                        quality = 0
                    elif quality <= 82:
                        quality = 1
                        value_mod += 5
                    elif quality <= 94:
                        quality = 2
                        value_mod += 10
                    elif quality <= 98:
                        quality = 3
                        value_mod += 25
                    else:
                        quality = 4
                        value_mod += 50

                    # calc random bonus
                    bonus = libtcod.random_get_int(0, 0, 100)
                    if bonus <= 90:
                        bonus = 0
                    elif bonus <= 94:
                        bonus = 1
                        value_mod += 25
                    elif bonus <= 97:
                        bonus = 2
                        value_mod += 50
                    elif bonus <= 99:
                        bonus = 3
                        value_mod += 100
                    else:
                        bonus = 4
                        value_mod += 200

                    cursed = 'uncursed'
                    curse_check = libtcod.random_get_int(0, 0, 100)
                    if curse_check <= 4:
                        cursed = 'cursed'
                    elif curse_check >= 96:
                        cursed = 'blessed'
                    # master_item_list indices: 0_SIMPLE, 1_NAME, 2_BASE_VALUE, 3_LEVEL, 4_ALIGNMENT, 5_ORDER, 6_FACTION, 7_EFFECT, 8_DESCRIPTION, 9_TYPE

                    item = [index, [quality, 0], [bonus, 0], [master_item_list[index][7], 0],
                            master_item_list[index][2] + value_mod, 0, cursed]
                    # 0_index, 1_quality[real, known], 2_bonus[real,known], 3_effects[rl, kn], 4_realvalue, 5_marketvalue, 6_cursedstatus
                    item_got = 1
    return item


def appraise_confidence(item, faction, level):  # how confident are we that this item is what we think it is? for NPCs

    item_level = master_item_list[item[0]][3]
    confidence = 0
    if faction in master_item_list[item[0]][6]:  # is the item related to the appraisers faction?

        if item_level + 4 <= level:  # based on level, we have more or less confidence about what the thing is. 1 to 5.
            confidence = libtcod.random_get_int(0, 3, 5)

        elif item_level + 2 <= level:
            confidence = libtcod.random_get_int(0, 2, 4)

        elif item_level + 1 <= level:
            confidence = libtcod.random_get_int(0, 1, 3)

        elif item_level <= level:
            confidence = libtcod.random_get_int(0, 0, 3)  # we can be a bit cocky if the item is 'in faction' ...

    else:  # no faction relation random number from 1 to 3, 3 if we get 'lucky' and we are high level relative

        if item_level + 4 <= level:
            confidence = libtcod.random_get_int(0, 0, 3)

        elif item_level + 2 <= level:
            confidence = libtcod.random_get_int(0, 0, 2)

        elif item_level + 1 <= level:
            confidence = libtcod.random_get_int(0, 0, 1)

    return confidence


def assess_item(item, faction, level):
    # a means for a hero to decide whether what he is wearing is any good

    item_index = item[0]
    item_level = master_item_list[item_index][3]
    range = item_level / 2
    item_bonus = item[2][0]
    item_quality = item[1][0]
    set_power = item_level

    partial_bonus = libtcod.random_get_int(0, -1, item_bonus + 1)
    partial_quality = libtcod.random_get_int(0, -1, item_quality + 1)
    range = libtcod.random_get_int(0, (range * -1), range)

    if faction in master_item_list[item_index][6]:  # if the item is faction related:
        # now appraise based on level

        if item_level + 4 <= level:
            # we know all physical things about the item
            # need to break these down in to helper functions, what do they return?
            set_power += item_quality
            set_power += item_bonus
            set_power += range

        elif item_level + 2 <= level:
            # we can deduce a bit about any enchantments and we know the quality.
            # [0_index, 1_quality, 2_bonus, 3_effect, 4_bought_value, 5_set_value, 6_cursed]
            set_power += item_quality
            set_power += partial_bonus
            set_power += range

        elif item_level + 1 <= level:
            # we can kind of detect if the quality is higher than normal, but we are still guessing.
            set_power += partial_quality
            set_power += range

        elif item_level <= level:
            # we don't know too much, but we can guess. add or take away up to 20 percent of the items base value
            set_power += range

    else:  # no faction relation

        if item_level + 4 <= level:
            # we can deduce a bit about any enchantments and we know the quality.
            # [0_index, 1_quality, 2_bonus, 3_effect, 4_bought_value, 5_set_value, 6_cursed]
            set_power += item_quality
            set_power += partial_bonus
            set_power += range

        elif item_level + 2 <= level:
            # we can detect if the quality is higher than normal, but we are still guessing.
            set_power += partial_quality
            set_power += range

        elif item_level <= level:
            # we don't know hardly anything. Add or take away some quality, relative to the base_level of the item
            set_power += range

    return set_power


def appraise_value(item, faction,
                   level):  # item, faction of item appraiser, and level of item appraiser, ostensibly for NPC shopkeepers

    set_value = 0
    item_index = item[0]
    item_level = master_item_list[item_index][3]

    if faction in master_item_list[item_index][6]:  # if the item is faction related, we have a better chance
        set_value += master_item_list[item_index][2]  # we know what the base value of this item is
        # now appraise based on level

        if item_level + 4 <= level:
            # we know all physical things about the item
            # need to break these down in to helper functions, what do they return?
            set_value += full_quality_appraise(item, set_value)
            set_value += full_bonus_appraise(item, set_value)
            set_value += guess_item_value(item, set_value)

        elif item_level + 2 <= level:
            # we can deduce a bit about any enchantments and we know the quality.
            # [0_index, 1_quality, 2_bonus, 3_effect, 4_bought_value, 5_set_value, 6_cursed]
            set_value += full_quality_appraise(item, set_value)
            set_value += part_bonus_appraise(item, set_value)
            set_value += guess_item_value(item, set_value)

        elif item_level + 1 <= level:
            # we can detect if the quality is higher than normal, but we are still guessing.
            set_value += part_quality_appraise(item, set_value)
            set_value += guess_item_value(item, set_value)

        elif item_level <= level:
            # we don't know too much, but we can guess. add or take away up to 20 percent of the items base value
            set_value += guess_item_value(item, set_value)

    else:  # no faction relation
        set_value += master_item_list[item_index][2]  # we know what the base value of this item is

        if item_level + 4 <= level:
            # we can deduce a bit about any enchantments and we know the quality.
            # [0_index, 1_quality, 2_bonus, 3_effect, 4_bought_value, 5_set_value, 6_cursed]
            set_value += full_quality_appraise(item, set_value)
            set_value += part_bonus_appraise(item, set_value)
            set_value += guess_item_value(item, set_value)

        elif item_level + 2 <= level:
            # we can detect if the quality is higher than normal, but we are still guessing.
            set_value += part_quality_appraise(item, set_value)
            set_value += guess_item_value(item, set_value)

        elif item_level <= level:
            # we don't know too much, but we can guess. add or take away up to 20 percent of the items base value
            set_value += guess_item_value(item, set_value)

    return set_value


def guess_item_value(item, set_value):  # adds or subtracts a notional amount from the set value
    # not sure this is working
    range_value = int(master_item_list[item[0]][2] * 0.2)
    # master item list base value (base item), 20% of this figure
    add_value = libtcod.random_get_int(0, (range_value * -1), range_value)
    # message(str(add_value))
    # set_value += add_value

    return add_value  # not set_value


def part_quality_appraise(item, set_value):
    item_quality = item[1][0]
    range_value = 0
    if item_quality > 0:
        range_value = libtcod.random_get_int(0, 0, 15)
        # set_value += range_value
    return range_value  # not set_value


def full_quality_appraise(item, set_value):
    item_quality = item[1][0]
    range_value = 0
    if item_quality == 0:
        range_value += 0
    elif item_quality == 1:
        range_value += 5
    elif item_quality == 2:
        range_value += 10
    elif item_quality == 3:
        range_value += 25
    else:
        range_value += 50

    return range_value


def part_bonus_appraise(item, set_value):
    item_bonus = item[2][0]
    range_value = 0
    if item_bonus > 0:
        range_value = libtcod.random_get_int(0, 0, 50)  # we know it's enchanted, but not how much
        # set_value += range_value

    return range_value


def full_bonus_appraise(item, set_value):
    item_bonus = item[2][0]
    range_value = 0
    if item_bonus == 0:
        range_value += 0
    elif item_bonus == 1:
        range_value += 25
    elif item_bonus == 2:
        range_value += 50
    elif item_bonus == 3:
        range_value += 100
    else:
        range_value += 200

    return range_value


###########################
###########################
##        GAME PLAY FUNCTIONS      ##
###########################
###########################

## GAME FLOW

def pass_turn():
    global turns, sub_turns, day_names, day, game_day, seasons, season, year, day_count  # game timing variables
    global item_examined  # gameplay variables

    sub_turns += 1
    # take object actions
    if sub_turns >= game_speed:  # hourly
        turns += 1
        sub_turns = 0
        auction_add_bidders()  # new bidders every hour
        for heroes in town_heroes:
            if heroes.hp['current'] > 0:  # is hero alive?
                if libtcod.random_get_int(0, 0, hero_base_speed) == 1:
                    heroes.hero_make_a_fucking_decision()
        set_glow()
        for monster in monster_list:
            monster.monster_decision()
        if libtcod.random_get_int(0, 0, 4) == 1:
            the_mayoress.review_town_safety()
            # hero movement
            # hero decisions purchase / sale / adventuring
            # purchases being made
            # give aways
            # dead adventurers
            # equipment being offered for sale

    if turns == 24:  # daily
        turns = 0
        day_count += 1
        day += 1
        ##twinkle(1)
        get_day = day_names.pop(0)  # cycle the days around in the week
        if get_day == "Sunday":  # end of week
            for shop in shop_list:  # stock taking exercise
                appraise_stock(shop[1])
            twinkle(1)  # slow wear to the map
        day_names.append(get_day)
        game_day = day_names[0][0]
        hero_rot()  # rot any dead heroes.
        if auction_item:
            auction_resolve()  # sort out stuff if there is an item up for auction
        auction_commence()  # start it up again
        # daily game updates
        item_examined = 0  # reset the ability to examine items
        # resolve the current auction
        # set up the next auction, if there is inventory available
        for heroes in town_heroes:
            heroes.pay_rent()
            # ~ if not heroes.in_dungeon:
            # ~ heroes.rest() #rest heroes
        for heroes in hero_list:
            heroes.world_hero_decision()
            heroes.world_wage()

        sales_metrics.tick()  # keep this alive?

        for dungeons in dungeon_list:
            x = dungeons[2]
            y = dungeons[3]
            map[x][y].dungeon.churn()

        measure_world_evil()
        measure_world_chaos()

        check_world_evil()
        check_world_chaos()
        set_tax_rate()

        end_month = seasons[0][1]
        if day + 2 >= end_month:
            alert_finance_issue()

    if day > seasons[0][
        1]:  # Monthly cycle: Taxes / Relationships - Monthly status update? Store financial information with each transaction?

        player.wealth -= tax_rate
        log_purchase('TAXES', tax_rate, 'TAX MAN')

        day = 1
        get_season = seasons.pop(0)  # cycle the seasons around
        seasons.append(get_season)
        season = seasons[0][0]

        ledger_new_month()

        # monthly status update ?
        # monthly dungeon update ?
        # generate new heroes ?
        # generate some items for the dungeons ?
        if get_season == 'December':
            year += 1

        check_finances()


def alert_finance_issue():
    if player.wealth - tax_rate < 0:
        message('CAREFUL! You are short of funds for the Tax Man, he is coming soon!', libtcod.red, libtcod.red)


## AI HELPER FUNCTIONS

def appraise_stock(shop_name):
    loc = find_shop(shop_name)
    x = loc[0]
    y = loc[1]

    inventory = map[x][y].shop.inventory
    faction = map[x][y].faction
    level = map[x][y].shop.base_level

    for n in range(len(inventory)):
        set_value = appraise_value(inventory[n], faction, level)
        inventory[n][5] = set_value
        # message(str(set_value)) #used to debug output


## INTERACTION FUNCTIONS

def examine_item(item):
    global player, item_examined
    pass

    # player_item_knowledge_list - structure:
    # [0_Index_known, 1_Known_name, 2_Known_reason, 3_Known_description, 4_Known_level, 5_Known_alignment, 6_Known_order, 7_Known_faction, 8_Known_effect]

    # Item - structure
    # [ 0_index, 1_quality[real, known], 2_bonus[real,known], 3_effects[rl, kn], 4_realvalue, 5_marketvalue, 6_cursedstatus ]

    # master_item_list - structure
    # 0_SIMPLE_NAME, 1_NAME, 2_BASE_VALUE, 3_LEVEL, 4_ALIGNMENT, 5_ORDER, 6_FACTION, 7_EFFECT, 8_DESCRIPTION, 9_TYPE

    # item specific information
    item_index = item[0]
    item_set_value = item[5]
    item_real_value = item[4]
    item_known_quality = item[1][1]
    item_real_quality = item[1][0]
    item_known_bonus = item[2][1]
    item_real_bonus = item[2][0]
    item_curse_status = item[6]

    # check out what we know about the item type:
    known_item = player_item_knowledge_list[item_index]

    # known_index = known_item[0] #fucker is not used!!!
    known_name = known_item[0]
    known_reason = known_item[1]
    known_description = known_item[2]
    known_level = known_item[3]
    known_align = known_item[4]
    known_order = known_item[5]
    known_faction = known_item[6]
    known_effect = known_item[7]

    # collect the factual information about the item
    real_item = master_item_list[item_index]

    real_name_simple = real_item[0]
    real_name = real_item[1]
    real_base_value = real_item[2]
    real_level = real_item[3]
    real_alignment = real_item[4]
    real_order = real_item[5]
    real_faction = real_item[6]
    real_effect = real_item[7]
    real_description = real_item[8]
    real_type = real_item[9]

    # step by step identification process, by item.
    # First iteration of this game mechanic, we'll have three tiers for each item type.
    # Each one based on level.
    # Step one: Item real name, and description, and base value reported to us - if we have passed this point.
    # Step two: Item level, order and alignment.
    # Step three: Factions. ???

    # On level up we get the ability to specialise in item types, revealing more about the quality and bonus of these things ... ?

    # pop up giving information about the item ... at this stage we get to formally examine the item

    real_factor = float(real_level)
    player_factor = float(player.base_level)

    success_chance = int((player_factor / real_factor) * 100)
    # message(str(success_chance))

    success_test = libtcod.random_get_int(0, 0, 100)
    # message(str(success_test))
    # examine_success = 0

    if success_test <= success_chance:
        examine_success = 1
        player.gain_experience(real_level * 2)
    else:
        examine_success = 0
        player.gain_experience(1)
        message('You fail to deduce any more about the item', libtcod.light_red, libtcod.dark_red)

    if examine_success:
        if known_name == real_name:  # we have already passed the first stage
            # if real_type == 'scroll':
            #    message('We already know that this ' + real_name + ' is a scroll of ' + known_name)
            # else:
            #    message('We already know that this ' + real_name + ' is a ' + known_name)
            if known_level == real_level:  # And the second, previously
                # message('And it is a level ' + str(known_level) + ' item.')
                if known_faction == real_faction:  # we already know everything about the item anyway ...
                    message('We know all there is to deduce, by investigation alone.', libtcod.light_grey,
                            libtcod.light_blue)
                    pass  # need to feed back whats going on ...
                else:  # ok, so we don't know everything, we can stand to learn a bit more. These tests are weak, in the presence of other mechanisms ...
                    message('Excellent. We now know who tends to be associated with the ' + player_item_display(item),
                            libtcod.light_grey, libtcod.light_blue)
                    player_item_knowledge_list[item_index][6] = real_faction  # need to feed back
            else:  # we only know a little bit, lets learn some more
                message('We now know the alignment, order and the level of the item.', libtcod.light_grey,
                        libtcod.light_blue)
                player_item_knowledge_list[item_index][3] = real_level
                player_item_knowledge_list[item_index][5] = real_order
                player_item_knowledge_list[item_index][4] = real_alignment
        else:  # we have barely picked this thing up
            if real_type == 'scroll':
                message('Ok, this ' + known_name + ' is actually a scroll of ' + real_name + '.', libtcod.light_grey,
                        libtcod.light_blue)
            else:
                message('Ok, this ' + known_name + ' is actually a ' + real_name + '.', libtcod.light_grey,
                        libtcod.light_blue)
            message(real_description, libtcod.light_grey, libtcod.light_blue)
            player_item_knowledge_list[item_index][
                0] = real_name  # these aren't reassigning the original information ...
            known_description = real_description



            # item_examined = 1 - take this out of the function (can happen other ways?)

            # else:
            #    message('You pick up a bit more information about the item')


## AUCTION HOUSE FUNCTIONS

def level_display(known_level):
    if known_level == 0:
        return 'Unknown'
    else:
        return str(known_level)


def align_display(known_align):
    if known_align == 0:
        return 'Unknown'
    elif known_align < 50:
        return 'Evil'
    elif known_align > 50:
        return 'Good'
    else:
        return 'Neutral'


def order_display(known_order):
    if known_order == 0:
        return 'Unknown'
    elif known_order < 50:
        return 'Chaotic'
    elif known_order > 50:
        return 'Lawful'
    else:
        return 'Neutral'


def item_quality_display(known_item_quality):
    if known_item_quality == 0:
        return 'Normal'
    elif known_item_quality == 1:
        return 'Good'
    elif known_item_quality == 2:
        return 'Fine'
    elif known_item_quality == 3:
        return 'Master'
    else:
        return 'Unknown'


def item_bonus_display(known_item_bonus):
    if known_item_bonus == 0:
        return 'Normal'
    elif known_item_bonus == 1:
        return '+1'
    elif known_item_bonus == 2:
        return '+2'
    elif known_item_bonus == 3:
        return '+3'
    elif known_item_bonus == 4:
        return '+4'
    else:
        return 'Unknown'


def auction_add_bidders():
    global bidders
    # creates a list if 0 to 1 random bidders with a faction and a level, add them to the list.
    if auction_item:
        bidder_chance = 25  # chance of new bidder per hour, in percentage

        add_bidder = libtcod.random_get_int(0, 0, 100)

        if add_bidder <= bidder_chance:
            num_bidders = libtcod.random_get_int(0, 1, 1)  # random number from 1 to 1 (for tweaking ... ?)
        else:
            num_bidders = 0

        for x in range(num_bidders):
            level = libtcod.random_get_int(0, 1, 3)
            bidders.append([get_random_faction(), level])  # this wont let a hero have a go ... ???

    invalid_bids = []  # now iterate through the bidders to ensure that if a shop is destroyed, they can't buy owt
    for bidder in bidders:
        valid_bid = 0

        for shop in shop_list:
            if shop[0] == bidder[0]:
                valid_bid = 1

        if not valid_bid:
            invalid_bids.append(bidder)

    for invalid_bid in invalid_bids:
        bidders.remove(invalid_bid)


def auction_commence():
    global bidders, player_bid, bid_placed, auction_item

    # find a shop
    if find_shop('Auction House'):
        shop_location = find_shop('Auction House')
        x = shop_location[0]
        y = shop_location[1]

        # see if the auction house has an item to put up for auction
        if map[x][y].shop.inventory:
            auction_item = map[x][y].shop.inventory[0]
        else:
            auction_item = None


def auction_resolve():
    global bidders, player_bid, bid_placed, auction_item

    loc = find_shop('Auction House')  # x and y coords of the auction house
    x = loc[0]
    y = loc[1]

    # find bidders bids
    all_bids = []

    real_item = master_item_list[auction_item[0]]
    real_item_basevalue = real_item[2]
    real_item_faction = real_item[6]

    for m in range(len(bidders)):
        bidder_faction = bidders[m][0]
        bidder_level = bidders[m][1]

        if appraise_confidence(auction_item, bidder_faction,
                               bidder_level):  # appraise_confidence(item, bidder_faction, bidder_level)
            all_bids.append([appraise_value(auction_item, bidder_faction, bidder_level), bidder_faction])
        elif bidder_faction in real_item_faction:  # if confidence doesn't return positive, let's have a flyer, from 1 to the base value of the item IN FACTION ONLY
            all_bids.append([libtcod.random_get_int(0, 1, real_item_basevalue), bidder_faction])
    bid_count = len(all_bids)

    item_bought = 0

    if player_bid:  # the player has put in a bid.
        if bid_count == 0:  # no-one else has bid

            sell_shop = map[x][y].shop
            buy_shop = player

            if auction_buy_item(buy_shop, sell_shop, 0,
                                player_bid):  # index is the item sitting in the sell shop, zero for all auction house activity so far
                message('You won an item at auction, for $' + str(player_bid) + ', submitting the only bid',
                        libtcod.light_green, libtcod.dark_green)
                item_bought = 1
                buy_shop.gain_experience(item_experience(auction_item))  # add the level of the item in experience
                log_purchase(player_item_display(auction_item), player_bid, 'by Auction')
                sales_metrics.log_item_bought(real_item[9], player_bid, player_name, day_count)
                # perhaps we should send the item, and enumerate the experience based on its quality / bonus
            else:
                map[x][y].shop.inventory.pop(
                    0)  # no bids on the item. Remove the item from AH inventory, lost to the ether.
                message('You won the auction today with the only bid, but you can not afford it. Item fed to Dragons.',
                        libtcod.light_red, libtcod.dark_red)
                item_bought = 1

        else:  # player has bid, in competition with other factions

            all_bids.append([player_bid, player_name])  # now add player bid to mix
            bids_in_order = sorted(all_bids, reverse=True)
            # sort the bids, compare this against the player bid, and then give the item to the winner.

            for confirm_win in range(
                    len(bids_in_order)):  # iterate through the bids, and give the item to the first valid bid

                win_faction = bids_in_order[confirm_win][1]
                win_price = bids_in_order[confirm_win][0]

                if not find_shop_by_faction(
                        win_faction):  # the faction doesn't have representation on the map, it returns false
                    map[x][y].shop.inventory.pop(
                        0)  # no bids on the item. Remove the item from AH inventory, lost to the ether.
                    message(str(win_faction) + ' wins an item at auction, for $' + str(
                        win_price) + ' and takes it out of town.', libtcod.light_yellow, libtcod.dark_yellow)
                    map[x][y].wealth += win_price  # pay the auction house
                    item_bought = 1
                else:
                    [xx, yy] = find_shop_by_faction(win_faction)
                    buy_shop = map[xx][yy].shop  # winning faction premises
                    sell_shop = map[x][y].shop  # auction house
                    if auction_buy_item(buy_shop, sell_shop, 0, win_price):  # can they make the transaction?
                        if win_faction == player_name:
                            message('You won an item at auction, for $' + str(player_bid) + ', beating the competition',
                                    libtcod.light_green, libtcod.dark_green)
                            log_purchase(player_item_display(auction_item), player_bid, 'by Auction')
                            sales_metrics.log_item_bought(real_item[9], win_price, player_name, day_count)
                        else:
                            message(
                                str(win_faction) + ' won an item at auction, with a winning bid of $' + str(win_price),
                                libtcod.light_yellow, libtcod.dark_yellow)
                            sales_metrics.log_item_bought(real_item[9], win_price, win_faction, day_count)
                        item_bought = 1
                        break  # stop iterating through bids, item has been won

    else:  # player didn't bother
        if bid_count == 0:  # neither did anyone else ...
            map[x][y].shop.inventory.pop(
                0)  # no bids on the item. Remove the item from AH inventory, lost to the ether.
            message('An Auction closes, and the item is not won. It is fed to the Dragons.', libtcod.light_red,
                    libtcod.dark_red)
            item_bought = 1
        else:  # at least somebody did ...

            bids_in_order = sorted(all_bids, reverse=True)

            for confirm_win in range(
                    len(bids_in_order)):  # iterate through the bids, and give the item to the first valid bid

                win_faction = bids_in_order[confirm_win][1]
                win_price = bids_in_order[confirm_win][0]

                if not find_shop_by_faction(
                        win_faction):  # the faction doesn't have representation on the map, it returns false
                    map[x][y].shop.inventory.pop(
                        0)  # no bids on the item. Remove the item from AH inventory, lost to the ether.
                    message(str(win_faction) + ' wins an item at auction, for $' + str(
                        win_price) + ' and takes it out of town.', libtcod.light_yellow, libtcod.dark_yellow)
                    item_bought = 1
                else:
                    [xx, yy] = find_shop_by_faction(win_faction)
                    buy_shop = map[xx][yy].shop  # winning faction premises
                    sell_shop = map[x][y].shop  # auction house
                    if auction_buy_item(buy_shop, sell_shop, 0, win_price):  # can they make the transaction?
                        message(str(win_faction) + ' won an item at auction, with a winning bid of $' + str(win_price),
                                libtcod.light_green, libtcod.dark_green)
                        sales_metrics.log_item_bought(real_item[9], win_price, win_faction, day_count)
                        item_bought = 1
                        break  # stop iterating through bids, item has been won

    if item_bought == 0:  # bids might have come in, but they didn't lead to a sale
        message('No bids were received today at the auction. More Dragon food.', libtcod.light_red, libtcod.dark_red)
        map[x][y].shop.inventory.pop(0)  # no bids on the item. Remove the item from AH inventory, lost to the ether.

    bid_placed = 0  # resolved the auction, bid cleared
    bidders = []  # no more bidders
    player_bid = 0  # player has no valid bid left bid, so no value


#####################
## INTERFACE FUNCTIONS  ##
#####################

def hi_score():
    popup_width = 78
    popup_height = 41

    popup_xoffset = 1
    popup_yoffset = 1

    try:
        file = shelve.open('highscores', 'r')
        highscores = file['highscores']
        file.close()
    except:
        highscores = []

    no_items_sold = 0
    no_items_bought = 0
    item_sold_value = 0
    item_bought_value = 0
    no_contracts_let = 0
    contract_value = 0
    taxes_paid = 0

    datestamp = game_day + ' ' + str(day)

    player = player_name

    for month in the_ledger:
        for item in month:
            if item[2] == 'CONTRACT':
                no_contracts_let += 1
                contract_value += int(item[5])
            elif item[2] == 'TAXES':
                taxes_paid += int(item[5])
            elif item[3] == 'Bought':
                no_items_bought += 1
                try:
                    item_bought_value += int(item[5])
                except:
                    pass
            elif item[3] == 'Sold  ':
                no_items_sold += 1
                item_sold_value += int(item[4])

    total_cash_moved = contract_value + taxes_paid + item_bought_value + item_sold_value
    cash_points = int(total_cash_moved / 10)

    total_items_moved = no_contracts_let + no_items_bought + no_items_sold
    item_points = total_items_moved

    score = item_points + cash_points
    # record = [ season, datestamp, item_name, 'Bought', '-', str(amount), seller ]

    this_highscore = [
        score,
        season,
        datestamp,
        no_items_sold,
        item_sold_value,
        no_items_bought,
        item_bought_value,
        no_contracts_let,
        contract_value,
        taxes_paid,
        player,
    ]

    highscores.append(this_highscore)

    top_highscores = sorted(highscores)
    top_highscores.reverse()

    try:
        file = shelve.open('highscores', 'n')
        file['highscores'] = highscores
        file.close()
    except:
        pass

    hiscore_popup = libtcod.console_new(popup_width, popup_height)

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(hiscore_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
    libtcod.console_blit(hiscore_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1, popup_yoffset - 1, 0.4,
                         0.4)

    key = libtcod.console_check_for_keypress()

    while not key.vk == libtcod.KEY_ENTER:
        libtcod.console_set_foreground_color(hiscore_popup, libtcod.light_green)
        for clearx in range(popup_width):  # draw a box, clear text
            for cleary in range(popup_height):
                libtcod.console_set_back(hiscore_popup, clearx, cleary, libtcod.Color(35, 35, 55), libtcod.BKGND_SET)
                libtcod.console_print_left(hiscore_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

        libtcod.console_print_left(hiscore_popup, 1, 1, libtcod.BKGND_NONE,
                                   '1 0 0    H E R O E S   -   H I   S C O R E ! ! !   press enter')

        for line in range(popup_width):
            libtcod.console_put_char(hiscore_popup, line, 3, '=', libtcod.BKGND_NONE)

        libtcod.console_set_foreground_color(hiscore_popup, libtcod.light_blue)
        libtcod.console_print_left(hiscore_popup, 1, 5, libtcod.BKGND_NONE, player)
        libtcod.console_set_foreground_color(hiscore_popup, libtcod.light_green)
        libtcod.console_print_left(hiscore_popup, 1, 6, libtcod.BKGND_NONE, 'NO. ITEMS SOLD: ' + str(no_items_sold))
        libtcod.console_print_left(hiscore_popup, 25, 6, libtcod.BKGND_NONE,
                                   'AT A COMBINED VALUE OF $' + str(item_sold_value))
        libtcod.console_print_left(hiscore_popup, 1, 7, libtcod.BKGND_NONE, 'NO. ITEMS BOUGHT: ' + str(no_items_bought))
        libtcod.console_print_left(hiscore_popup, 25, 7, libtcod.BKGND_NONE,
                                   'AT A COMBINED VALUE OF $' + str(item_bought_value))
        libtcod.console_print_left(hiscore_popup, 1, 8, libtcod.BKGND_NONE,
                                   'NO. CONTRACTS LET: ' + str(no_contracts_let))
        libtcod.console_print_left(hiscore_popup, 25, 8, libtcod.BKGND_NONE,
                                   'AT A COMBINED VALUE OF $' + str(contract_value))
        libtcod.console_print_left(hiscore_popup, 3, 9, libtcod.BKGND_NONE, 'TAXES PAID:' + str(taxes_paid))
        libtcod.console_set_foreground_color(hiscore_popup, libtcod.light_red)
        libtcod.console_print_left(hiscore_popup, 5, 10, libtcod.BKGND_NONE,
                                   'STOPPED TRADING ON: ' + datestamp + ' ' + season)
        libtcod.console_set_foreground_color(hiscore_popup, libtcod.green)

        libtcod.console_print_left(hiscore_popup, 1, 12, libtcod.BKGND_NONE, 'Your Score is:' + str(score))

        if len(top_highscores) > 3:
            number_entries = 3
        else:
            number_entries = len(top_highscores)

        for n in range(number_entries):

            previous_highscore = top_highscores[n]

            x_score = previous_highscore[0]
            x_season = previous_highscore[1]
            x_datestamp = previous_highscore[2]
            x_no_items_sold = previous_highscore[3]
            x_item_sold_value = previous_highscore[4]
            x_no_items_bought = previous_highscore[5]
            x_item_bought_value = previous_highscore[6]
            x_no_contracts_let = previous_highscore[7]
            x_contract_value = previous_highscore[8]
            x_taxes_paid = previous_highscore[9]
            x_player = previous_highscore[10]

            if this_highscore == previous_highscore:
                libtcod.console_set_foreground_color(hiscore_popup, libtcod.light_blue)
            else:
                libtcod.console_set_foreground_color(hiscore_popup, libtcod.light_grey)

            libtcod.console_print_left(hiscore_popup, 2 + n, (n * 9) + 14, libtcod.BKGND_NONE,
                                       'HIGHSCORE #' + str(n + 1) + ' - ' + x_player)
            libtcod.console_print_left(hiscore_popup, 2 + n, (n * 9) + 15, libtcod.BKGND_NONE,
                                       'NO. ITEMS SOLD: ' + str(x_no_items_sold))
            libtcod.console_print_left(hiscore_popup, 27 + n, (n * 9) + 15, libtcod.BKGND_NONE,
                                       'AT A COMBINED VALUE OF $' + str(x_item_sold_value))
            libtcod.console_print_left(hiscore_popup, 2 + n, (n * 9) + 16, libtcod.BKGND_NONE,
                                       'NO. ITEMS BOUGHT: ' + str(x_no_items_bought))
            libtcod.console_print_left(hiscore_popup, 27 + n, (n * 9) + 16, libtcod.BKGND_NONE,
                                       'AT A COMBINED VALUE OF $' + str(x_item_bought_value))
            libtcod.console_print_left(hiscore_popup, 2 + n, (n * 9) + 17, libtcod.BKGND_NONE,
                                       'NO. CONTRACTS LET: ' + str(x_no_contracts_let))
            libtcod.console_print_left(hiscore_popup, 27 + n, (n * 9) + 17, libtcod.BKGND_NONE,
                                       'AT A COMBINED VALUE OF $' + str(x_contract_value))
            libtcod.console_print_left(hiscore_popup, 4 + n, (n * 9) + 18, libtcod.BKGND_NONE,
                                       'TAXES PAID:' + str(x_taxes_paid))
            libtcod.console_print_left(hiscore_popup, 6 + n, (n * 9) + 19, libtcod.BKGND_NONE,
                                       'STOPPED TRADING ON: ' + x_datestamp + ' ' + x_season)

            libtcod.console_print_left(hiscore_popup, 2 + n, (n * 9) + 21, libtcod.BKGND_NONE,
                                       'A score of:' + str(x_score))

        libtcod.console_blit(hiscore_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
        libtcod.console_flush()

        key = libtcod.console_check_for_keypress()


def help():
    popup_width = 78
    popup_height = 46

    popup_xoffset = 1
    popup_yoffset = 1

    help_popup = libtcod.console_new(popup_width, popup_height)

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(help_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
    libtcod.console_blit(help_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1, popup_yoffset - 1, 0.4, 0.4)

    key = libtcod.console_check_for_keypress()

    while not key.vk == libtcod.KEY_ENTER:
        libtcod.console_set_foreground_color(help_popup, libtcod.light_green)
        for clearx in range(popup_width):  # draw a box, clear text
            for cleary in range(popup_height):
                libtcod.console_set_back(help_popup, clearx, cleary, libtcod.Color(35, 35, 55), libtcod.BKGND_SET)
                libtcod.console_print_left(help_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

        libtcod.console_print_left(help_popup, 1, 1, libtcod.BKGND_NONE,
                                   '1 0 0    H E R O E S   -   H E L P   S C R E E N  /  K E Y   C O M M A N D S')

        for line in range(popup_width):
            libtcod.console_put_char(help_popup, line, 3, '=', libtcod.BKGND_NONE)

        libtcod.console_print_left(help_popup, 1, 5, libtcod.BKGND_NONE,
                                   'Welcome to 100 Heroes, a Roguelike game for the IBM PC investigating the ')
        libtcod.console_print_left(help_popup, 1, 6, libtcod.BKGND_NONE,
                                   'moral dilemmas of a practical capitalist in generic-fantasy-land.')
        libtcod.console_print_left(help_popup, 1, 8, libtcod.BKGND_NONE,
                                   'You are the Player, a new boy in Retail in the town of <random_town_name>')
        libtcod.console_print_left(help_popup, 1, 9, libtcod.BKGND_NONE,
                                   'and through a keen eye for a bargain, and better knowledge than the comp-')
        libtcod.console_print_left(help_popup, 1, 10, libtcod.BKGND_NONE,
                                   'etition, can you improve turnover sufficiently before the Balrog attacks?')
        libtcod.console_print_left(help_popup, 1, 12, libtcod.BKGND_NONE, 'There are three parts to the screen:')
        libtcod.console_print_left(help_popup, 1, 13, libtcod.BKGND_NONE,
                                   '  a) The Town Plan, with surrounding countryside (on the left)')
        libtcod.console_print_left(help_popup, 1, 14, libtcod.BKGND_NONE, '  b) The Info Bar (on the right)')
        libtcod.console_print_left(help_popup, 1, 15, libtcod.BKGND_NONE,
                                   '  c) The message bars (on the bottom, and bottom right)')
        libtcod.console_print_left(help_popup, 1, 17, libtcod.BKGND_NONE,
                                   'Start by mousing over the blue buildings in the Town Plan. These are shops.')
        libtcod.console_print_left(help_popup, 1, 18, libtcod.BKGND_NONE,
                                   'Click on any shop to enter, although some people might not like you enough')
        libtcod.console_print_left(help_popup, 1, 19, libtcod.BKGND_NONE,
                                   'just yet. Although with time, and an increase in your reputation, you will')
        libtcod.console_print_left(help_popup, 1, 20, libtcod.BKGND_NONE,
                                   'soon have them banging down your door asking for a cup of sugar or an')
        libtcod.console_print_left(help_popup, 1, 21, libtcod.BKGND_NONE, 'emergency loan.')
        libtcod.console_print_left(help_popup, 1, 23, libtcod.BKGND_NONE,
                                   'Find the Auction House, to place bids on todays Auction (see info bar) or')
        libtcod.console_print_left(help_popup, 1, 24, libtcod.BKGND_NONE,
                                   'find your own shop (Player) to see your own stock. Interact with items by')
        libtcod.console_print_left(help_popup, 1, 25, libtcod.BKGND_NONE,
                                   'pressing the number keys in shops, you can buy from other people and examine')
        libtcod.console_print_left(help_popup, 1, 26, libtcod.BKGND_NONE,
                                   'your own stock. Your shop is a bright yellow.')
        libtcod.console_print_left(help_popup, 1, 28, libtcod.BKGND_NONE,
                                   'The current status of the world (order-chaos, good-evil) is shown by the')
        libtcod.console_print_left(help_popup, 1, 29, libtcod.BKGND_NONE,
                                   'two bars within the info bar. A more chaotic world means more dungeons.')
        libtcod.console_print_left(help_popup, 1, 31, libtcod.BKGND_NONE,
                                   'Most keys should hopefully be clear in each screen, but there are a number')
        libtcod.console_print_left(help_popup, 1, 32, libtcod.BKGND_NONE,
                                   'of important ones only accessible from the Town Map:')
        libtcod.console_print_left(help_popup, 1, 34, libtcod.BKGND_NONE,
                                   '      l: Show Fiscal Ledger             h: Show Heroes (h again to cycle)')  # l,L = 108, 76 h,H = 104, 72
        libtcod.console_print_left(help_popup, 1, 35, libtcod.BKGND_NONE,
                                   '      c: Show Contract information    1/H: Indiv. Town Hero Information')
        libtcod.console_print_left(help_popup, 1, 36, libtcod.BKGND_NONE,
                                   '      d: Show Dungeon Roster            ?: Help Screen')  # d = 100, D = 68, ?=63
        libtcod.console_print_left(help_popup, 1, 37, libtcod.BKGND_NONE,
                                   '      5: Speed up time                  6: Slow down time')
        libtcod.console_print_left(help_popup, 1, 38, libtcod.BKGND_NONE,
                                   '(space): Pause / Unpause      (backspace): Save and exit Game')
        libtcod.console_print_left(help_popup, 1, 39, libtcod.BKGND_NONE,
                                   '      i: View your shop                 a: Show Auction House')
        libtcod.console_print_left(help_popup, 1, 40, libtcod.BKGND_NONE,
                                   'Now have a play around, and wait for your first hero to come to town!')
        libtcod.console_set_foreground_color(help_popup, libtcod.light_red)
        libtcod.console_print_left(help_popup, 1, 42, libtcod.BKGND_NONE, '  (press enter to return to game)')
        libtcod.console_set_foreground_color(help_popup, libtcod.light_yellow)
        libtcod.console_print_left(help_popup, 1, 44, libtcod.BKGND_NONE,
                                   '  This game is in development, apologies for any bugs.')

        libtcod.console_blit(help_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
        libtcod.console_flush()

        key = libtcod.console_check_for_keypress()


def show_ledger():
    popup_width = 76
    popup_height = 36

    popup_xoffset = 3
    popup_yoffset = 3

    ledger_popup = libtcod.console_new(popup_width, popup_height)

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(ledger_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
    libtcod.console_blit(ledger_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1, popup_yoffset - 1, 0.6,
                         0.6)

    # set up screen scrolling
    offset = 0

    num_months = len(the_ledger)

    current_month_index = num_months - 1  # pick the current month as the one for display
    # message('number of months = ' + str(num_months) + ' current month index = ' + str(current_month_index) )
    key = libtcod.console_check_for_keypress()

    while not key.vk == libtcod.KEY_ENTER:

        if key.c == 122:  # z
            offset -= 1
        elif key.c == 120:  # x
            offset += 1
        elif key.c == 97:  # a
            if current_month_index > 0:
                current_month_index -= 1
                offset = 0
        elif key.c == 115:  # s
            if not current_month_index + 1 >= num_months:
                current_month_index += 1
                offset = 0

        num_transactions = len(the_ledger[current_month_index])

        if num_transactions > 20:
            ledger_display = 20
        else:
            ledger_display = num_transactions


        # and the month by month change?

        for clearx in range(popup_width):  # draw a box, clear text
            for cleary in range(popup_height):
                libtcod.console_set_back(ledger_popup, clearx, cleary, libtcod.Color(195, 195, 145), libtcod.BKGND_SET)
                libtcod.console_print_left(ledger_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

        libtcod.console_set_foreground_color(ledger_popup, libtcod.red)
        libtcod.console_print_left(ledger_popup, 1, 1, libtcod.BKGND_NONE, 'F I S C A L   L E D G E R')
        libtcod.console_set_foreground_color(ledger_popup, libtcod.dark_red)
        libtcod.console_print_left(ledger_popup, 32, 1, libtcod.BKGND_NONE, 'z/x to scroll - enter to exit')
        libtcod.console_print_left(ledger_popup, 32, 2, libtcod.BKGND_NONE, 'a/s to change month')

        for line in range(popup_width):
            libtcod.console_put_char(ledger_popup, line, 4, '=', libtcod.BKGND_NONE)

        current_offset = offset

        if offset < 1:
            offset = 0

        if offset >= 1:
            libtcod.console_set_foreground_color(ledger_popup, libtcod.gray)
            libtcod.console_print_left(ledger_popup, 3, 4, libtcod.BKGND_NONE, '*more*')

        if ledger_display + offset < num_transactions:
            libtcod.console_set_foreground_color(ledger_popup, libtcod.gray)
            libtcod.console_print_left(ledger_popup, 3, 34, libtcod.BKGND_NONE, '*more*')

        if offset + ledger_display > num_transactions:
            offset -= 1

        # write the information to screen

        for transaction in range(ledger_display):
            item = the_ledger[current_month_index][transaction + offset]
            libtcod.console_set_foreground_color(ledger_popup, libtcod.dark_gray)
            libtcod.console_print_left(ledger_popup, 1, 3, libtcod.BKGND_NONE, the_ledger[current_month_index][0][0])
            libtcod.console_print_left(ledger_popup, 1, 5 + transaction, libtcod.BKGND_NONE, item[1])  # datestamp
            libtcod.console_print_left(ledger_popup, 13, 5 + transaction, libtcod.BKGND_NONE, '| ' + item[2])  # item
            libtcod.console_print_left(ledger_popup, 36, 5 + transaction, libtcod.BKGND_NONE,
                                       '| ' + item[3])  # bought/sold
            libtcod.console_print_left(ledger_popup, 44, 5 + transaction, libtcod.BKGND_NONE,
                                       '| ' + item[4])  # in money
            libtcod.console_print_left(ledger_popup, 49, 5 + transaction, libtcod.BKGND_NONE, '|')
            libtcod.console_set_foreground_color(ledger_popup, libtcod.red)
            libtcod.console_print_left(ledger_popup, 51, 5 + transaction, libtcod.BKGND_NONE, item[5])  # out money
            libtcod.console_set_foreground_color(ledger_popup, libtcod.dark_gray)
            libtcod.console_print_left(ledger_popup, 54, 5 + transaction, libtcod.BKGND_NONE,
                                       '| ' + item[6])  # other person / faction

        # message('number of months = ' + str(num_months) + ' current month index = ' + str(current_month_index) + ' offset ' + str(offset))

        libtcod.console_blit(ledger_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
        libtcod.console_flush()

        key = libtcod.console_wait_for_keypress(True)


def individual_hero_interface(index):
    popup_width = 60
    popup_height = 36

    numberheroes = len(town_heroes) - 1

    popup_xoffset = 2
    popup_yoffset = 2

    indiv_hero_popup = libtcod.console_new(popup_width, popup_height)

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(indiv_hero_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
    libtcod.console_blit(indiv_hero_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1, popup_yoffset - 1,
                         0.75, 0.75)

    # set up offset
    offset = index

    key = libtcod.console_check_for_keypress()

    while not key.vk == libtcod.KEY_ENTER:

        hero = town_heroes[offset]

        for clearx in range(popup_width):  # draw a box, clear text
            for cleary in range(popup_height):
                libtcod.console_set_back(indiv_hero_popup, clearx, cleary, libtcod.Color(15, 35, 45), libtcod.BKGND_SET)
                libtcod.console_print_left(indiv_hero_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.red)
        libtcod.console_print_left(indiv_hero_popup, 1, 1, libtcod.BKGND_NONE, 'H E R O   I N F O R M A T I O N')
        # libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.yellow)
        # libtcod.console_print_left(indiv_hero_popup, 26, 1, libtcod.BKGND_NONE, hero.name)
        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.dark_red)
        libtcod.console_print_left(indiv_hero_popup, 26, 2, libtcod.BKGND_NONE, 'z/x to scroll - enter to exit')
        for line in range(popup_width):
            libtcod.console_put_char(indiv_hero_popup, line, 3, '=', libtcod.BKGND_NONE)

        # write the information to screen

        if len(hero.brain.decisions) > 0:
            hero_motive = hero.brain.decisions[-1]
        else:
            hero_motive = 'none'

        if hero_motive == 'move_shop':
            motive_text = 'shopping'
        elif hero_motive == 'buy' or hero_motive == 'buy_scrolls' or hero_motive == 'buy_cargo':
            motive_text = 'shopping'
        elif hero_motive == 'sell' or hero_motive == 'sell_scrolls' or hero_motive == 'sell_cargo':
            motive_text = 'selling'
        elif hero.in_dungeon:
            motive_text = 'delving'
        elif hero_motive == 'descend':
            motive_text = 'preparing'
        elif hero_motive == 'socialise':
            motive_text = 'social'
        elif hero_motive == 'duel':
            motive_text = 'DUEL!'
        elif hero.hp['current'] < hero.hp['max']:
            motive_text = 'resting'
        else:
            motive_text = 'loitering'

        hp_float = float(hero.hp['current'])
        maxhp_float = float(hero.hp['max'])

        hero_health_percent = hp_float / maxhp_float

        if hero_health_percent <= 0:
            hero_health = ['Deceased', libtcod.red]
        elif hero_health_percent <= 0.4:
            hero_health = ['Wounded', libtcod.dark_red]
        elif hero_health_percent <= 0.8:
            hero_health = ['Bruised', libtcod.light_blue]
        else:
            hero_health = ['Healthy', libtcod.dark_green]

        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.dark_gray)
        libtcod.console_print_left(indiv_hero_popup, 1, 5, libtcod.BKGND_NONE,
                                   '------------------------------------------------------')
        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.light_yellow)
        libtcod.console_print_left(indiv_hero_popup, 1, 5, libtcod.BKGND_NONE,
                                   hero.name + ' of the ' + hero.faction + '.')
        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.dark_green)
        libtcod.console_print_left(indiv_hero_popup, 1, 6, libtcod.BKGND_NONE, 'LVL' + str(hero.base_level))
        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.light_green)
        libtcod.console_print_left(indiv_hero_popup, 20, 6, libtcod.BKGND_NONE, motive_text)
        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.green)
        libtcod.console_print_left(indiv_hero_popup, 30, 6, libtcod.BKGND_NONE, '$' + str(hero.wealth))
        libtcod.console_print_right(indiv_hero_popup, 58, 6, libtcod.BKGND_NONE, map[hero.x][hero.y].name)
        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.green)
        libtcod.console_print_left(indiv_hero_popup, 4, 6, libtcod.BKGND_NONE, str(hero.base_level))
        libtcod.console_set_foreground_color(indiv_hero_popup, hero_health[1])
        libtcod.console_print_left(indiv_hero_popup, 10, 6, libtcod.BKGND_NONE, hero_health[0])

        toutable = 0
        if motive_text == 'selling' or motive_text == 'shopping':
            # the hero can be 'touted'
            libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.yellow)
            libtcod.console_print_right(indiv_hero_popup, 58, 4, libtcod.BKGND_NONE, '(C)all over')
            toutable = 1

        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.dark_yellow)
        if len(hero.inventory) > 0:

            has_armor = 0
            has_weapon = 0
            has_clothing = 0
            scrolls_held = 0

            for item in hero.inventory:
                item_type = master_item_list[item[0]][9]
                if item_type == 'armor':
                    has_armor += 1

                if item_type == 'weapon':
                    has_weapon += 1

                if item_type == 'clothing':
                    has_clothing += 1

                if item_type == 'scroll':
                    scrolls_held += 1

            libtcod.console_print_left(indiv_hero_popup, 2, 7, libtcod.BKGND_NONE,
                                       'Carrying ' + str(has_armor) + ' suit(s) of armor, ' + str(
                                           has_weapon) + ' weapon(s),')
            libtcod.console_print_left(indiv_hero_popup, 2, 8, libtcod.BKGND_NONE,
                                       str(has_clothing) + ' item(s) of clothing and ' + str(
                                           scrolls_held) + ' scroll(s).')

        if hero.equipment['clothing'] == 0 or hero_health_percent <= 0:
            clothing = 'Nothing'
        else:
            clothing = player_item_display(hero.equipment['clothing'])

        if hero.equipment['armor'] == 0 or hero_health_percent <= 0:
            armor = 'Nothing'
        else:
            armor = player_item_display(hero.equipment['armor'])

        if hero.equipment['weapon'] == 0 or hero_health_percent <= 0:
            weapon = 'Nothing'
        else:
            weapon = player_item_display(hero.equipment['weapon'])

        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.gray)
        libtcod.console_print_left(indiv_hero_popup, 1, 10, libtcod.BKGND_NONE, 'Wearing:')
        libtcod.console_print_left(indiv_hero_popup, 1, 11, libtcod.BKGND_NONE, 'Wielding:')
        libtcod.console_print_left(indiv_hero_popup, 1, 12, libtcod.BKGND_NONE, 'Armored:')

        libtcod.console_print_left(indiv_hero_popup, 36, 9, libtcod.BKGND_NONE, 'Has recently killed:')
        libtcod.console_print_left(indiv_hero_popup, 2, 14, libtcod.BKGND_NONE, 'Personal log:')

        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.yellow)
        libtcod.console_print_left(indiv_hero_popup, 11, 10, libtcod.BKGND_NONE, clothing)
        libtcod.console_print_left(indiv_hero_popup, 11, 11, libtcod.BKGND_NONE, weapon)
        libtcod.console_print_left(indiv_hero_popup, 11, 12, libtcod.BKGND_NONE, armor)

        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.red)
        if hero.in_dungeon:
            libtcod.console_print_right(indiv_hero_popup, 58, 5, libtcod.BKGND_NONE,
                                        'IN DUNGEON lvl ' + str(hero.in_dungeon))
        else:
            libtcod.console_print_right(indiv_hero_popup, 58, 5, libtcod.BKGND_NONE, 'IN TOWN')
        number_kills = len(hero.activitylog['kills'])

        murderlist = hero.activitylog['kills'][:]

        murderlist.reverse()

        if log_information:
            log_info(str(murderlist))

        if number_kills > 4:
            number_kills = 4

        for n in range(number_kills):
            libtcod.console_print_left(indiv_hero_popup, 36, 10 + n, libtcod.BKGND_NONE, murderlist[n])

        activitylist = hero.activitylog['history'][:]

        activitylist.reverse()

        if log_information:
            log_info(str(activitylist))

        number_activity = len(hero.activitylog['history'])

        if number_activity > 18:
            number_activity = 18

        libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.light_red)
        for n in range(number_activity):
            libtcod.console_print_left(indiv_hero_popup, 2, 15 + number_activity - n, libtcod.BKGND_NONE,
                                       activitylist[n])
            libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.red)

        if debug_mode:
            libtcod.console_set_foreground_color(indiv_hero_popup, libtcod.light_gray)
            if hero.brain.contract:
                libtcod.console_print_left(indiv_hero_popup, 40, 14, libtcod.BKGND_NONE,
                                           "TGT:" + str(hero.brain.contract.target_name))
                libtcod.console_print_left(indiv_hero_popup, 40, 15, libtcod.BKGND_NONE,
                                           "CTY:" + str(hero.brain.contract.contract_type))
                libtcod.console_print_left(indiv_hero_popup, 40, 16, libtcod.BKGND_NONE,
                                           "MTY:" + str(hero.brain.contract.mission_type))
            m = len(hero.brain.decisions)
            for n in range(m):
                libtcod.console_print_left(indiv_hero_popup, 40, 17 + n, libtcod.BKGND_NONE,
                                           "DEC:" + str(hero.brain.decisions[n]))

            perceived_power = hero.stats['perceived']
            real_power = hero.stats['real']

            libtcod.console_print_left(indiv_hero_popup, 5, 35, libtcod.BKGND_NONE,
                                       "PERCEIVED POWER: " + str(perceived_power))
            libtcod.console_print_left(indiv_hero_popup, 30, 35, libtcod.BKGND_NONE, "REAL POWER: " + str(real_power))

        libtcod.console_blit(indiv_hero_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
        libtcod.console_flush()

        key = libtcod.console_wait_for_keypress(True)

        if key.c == 122:  # z
            offset -= 1
        elif key.c == 120:  # x
            offset += 1
        elif toutable == 1 and key.c == 67:  # C
            hero.tout(player_name)
            break

        if offset > numberheroes:
            offset -= 1
        if offset < 0:
            offset = 0


def hero_interface():
    popup_width = 60
    popup_height = 36

    popup_xoffset = 3
    popup_yoffset = 3

    hero_popup = libtcod.console_new(popup_width, popup_height)

    hero_mode = 1

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(hero_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
    libtcod.console_blit(hero_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1, popup_yoffset - 1, 0.75,
                         0.75)

    # set up screen scrolling
    offset = 0

    key = libtcod.console_check_for_keypress()

    while not key.vk == libtcod.KEY_ENTER:

        if hero_mode == 1:

            numberheroes = len(town_heroes)

            if numberheroes > 10:
                hero_display = 10
            else:
                hero_display = len(town_heroes)

            for clearx in range(popup_width):  # draw a box, clear text
                for cleary in range(popup_height):
                    libtcod.console_set_back(hero_popup, clearx, cleary, libtcod.Color(15, 35, 45), libtcod.BKGND_SET)
                    libtcod.console_print_left(hero_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

            libtcod.console_set_foreground_color(hero_popup, libtcod.red)
            libtcod.console_print_left(hero_popup, 1, 1, libtcod.BKGND_NONE, 'H E R O   R O S T E R')
            libtcod.console_set_foreground_color(hero_popup, libtcod.yellow)
            libtcod.console_print_left(hero_popup, 26, 1, libtcod.BKGND_NONE, 'Town Heroes')
            libtcod.console_set_foreground_color(hero_popup, libtcod.dark_red)
            libtcod.console_print_left(hero_popup, 26, 2, libtcod.BKGND_NONE, 'z/x to scroll - enter to exit')
            for line in range(popup_width):
                libtcod.console_put_char(hero_popup, line, 3, '=', libtcod.BKGND_NONE)

            current_offset = offset

            # write the information to screen
            for hero_view in range(hero_display):
                hero = town_heroes[hero_view + offset]

                if len(hero.brain.decisions) > 0:
                    motive = hero.brain.decisions[-1]
                else:
                    motive = 0

                if motive == 'move_shop':
                    motive_text = 'moving on'
                elif motive == 'buy' or motive == 'buy_scrolls' or motive == 'buy_cargo':
                    motive_text = 'shopping'
                elif motive == 'sell' or motive == 'sell_scrolls' or motive == 'sell_cargo':
                    motive_text = 'selling'
                elif motive == 'descend':
                    motive_text = 'preparing'
                elif motive == 'resolve_contract':
                    motive_text = 'moving on'
                elif motive == 'socialise':
                    motive_text = 'socialising'
                elif motive == 'duel':
                    motive_text = 'DUEL!'
                elif motive == 'rest':
                    motive_text = 'resting'
                else:
                    motive_text = 'loitering'

                hp_float = float(hero.hp['current'])
                maxhp_float = float(hero.hp['max'])

                hero_health_percent = hp_float / maxhp_float

                if hero_health_percent <= 0:
                    hero_health = ['Deceased', libtcod.red]
                elif hero_health_percent <= 0.4:
                    hero_health = ['Wounded', libtcod.dark_red]
                elif hero_health_percent <= 0.8:
                    hero_health = ['Bruised', libtcod.light_blue]
                else:
                    hero_health = ['Healthy', libtcod.dark_green]

                items_held = len(hero.inventory) + len(hero.activitylog['contract_cargo'])

                libtcod.console_set_foreground_color(hero_popup, libtcod.dark_gray)
                libtcod.console_print_left(hero_popup, 1, (hero_view * 3) + 5, libtcod.BKGND_NONE,
                                           '------------------------------------------------------')
                libtcod.console_set_foreground_color(hero_popup, libtcod.light_blue)
                libtcod.console_print_left(hero_popup, 1, (hero_view * 3) + 5, libtcod.BKGND_NONE,
                                           hero.name + ' of the ' + hero.faction + '.')
                libtcod.console_set_foreground_color(hero_popup, libtcod.dark_green)
                libtcod.console_print_left(hero_popup, 1, (hero_view * 3) + 6, libtcod.BKGND_NONE,
                                           'LVL' + str(hero.base_level))
                libtcod.console_set_foreground_color(hero_popup, libtcod.green)
                libtcod.console_print_left(hero_popup, 4, (hero_view * 3) + 6, libtcod.BKGND_NONE, str(hero.base_level))
                libtcod.console_set_foreground_color(hero_popup, libtcod.dark_yellow)
                libtcod.console_print_left(hero_popup, 7, (hero_view * 3) + 6, libtcod.BKGND_NONE,
                                           'Carrying ' + str(items_held) + ' items and $' + str(
                                               hero.wealth) + ', with ' + str(
                                               len(hero.activitylog['kills'])) + ' kills.')

                libtcod.console_set_foreground_color(hero_popup, hero_health[1])
                libtcod.console_print_right(hero_popup, 58, (hero_view * 3) + 6, libtcod.BKGND_NONE, hero_health[0])
                # str(hero.hp['current']) + '/' + str(hero.hp['max']) + ' ' +  leaving out explicit hit point display ...
                if hero.in_dungeon:
                    libtcod.console_set_foreground_color(hero_popup, libtcod.red)
                    libtcod.console_print_right(hero_popup, 58, (hero_view * 3) + 5, libtcod.BKGND_NONE,
                                                'IN DUNGEON lvl ' + str(hero.in_dungeon))
                elif not hero.in_dungeon:
                    libtcod.console_set_foreground_color(hero_popup, libtcod.yellow)
                    libtcod.console_print_right(hero_popup, 58, (hero_view * 3) + 5, libtcod.BKGND_NONE,
                                                motive_text + ' IN TOWN')

            libtcod.console_blit(hero_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
            libtcod.console_flush()

            key = libtcod.console_wait_for_keypress(True)

            if key.c == 122:  # z
                offset -= 1
            elif key.c == 120:  # x
                offset += 1
            elif key.c == 104:  # h
                hero_mode = 2
                offset = 0

            if offset < 1:
                offset = 0

            if offset >= 1:
                libtcod.console_set_foreground_color(hero_popup, libtcod.gray)
                libtcod.console_print_left(hero_popup, 3, 4, libtcod.BKGND_NONE, '*more*')

            if hero_display + offset < numberheroes:
                libtcod.console_set_foreground_color(hero_popup, libtcod.gray)
                libtcod.console_print_left(hero_popup, 3, 34, libtcod.BKGND_NONE, '*more*')

            if offset + hero_display > numberheroes:
                offset -= 1

        elif hero_mode == 2:

            dungeon_dwellers = []

            for dungeoneers in town_heroes:
                if dungeoneers.in_dungeon:
                    dungeon_dwellers.append(dungeoneers)

            numberheroes = len(dungeon_dwellers)

            if numberheroes > 3:
                hero_display = 3
            else:
                hero_display = len(dungeon_dwellers)

            for clearx in range(popup_width):  # draw a box, clear text
                for cleary in range(popup_height):
                    libtcod.console_set_back(hero_popup, clearx, cleary, libtcod.Color(15, 35, 45), libtcod.BKGND_SET)
                    libtcod.console_print_left(hero_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

            libtcod.console_set_foreground_color(hero_popup, libtcod.red)
            libtcod.console_print_left(hero_popup, 1, 1, libtcod.BKGND_NONE, 'H E R O   R O S T E R')
            libtcod.console_set_foreground_color(hero_popup, libtcod.yellow)
            libtcod.console_print_left(hero_popup, 26, 1, libtcod.BKGND_NONE, 'Dungeoneers')
            libtcod.console_set_foreground_color(hero_popup, libtcod.dark_red)
            libtcod.console_print_left(hero_popup, 26, 2, libtcod.BKGND_NONE, 'z/x to scroll - enter to exit')
            for line in range(popup_width):
                libtcod.console_put_char(hero_popup, line, 3, '=', libtcod.BKGND_NONE)

            current_offset = offset

            # write the information to screen
            for hero_view in range(hero_display):
                hero = dungeon_dwellers[hero_view + offset]

                hp_float = float(hero.hp['current'])
                maxhp_float = float(hero.hp['max'])

                hero_health_percent = hp_float / maxhp_float

                if hero_health_percent <= 0:
                    hero_health = ['Deceased', libtcod.red]
                elif hero_health_percent <= 0.4:
                    hero_health = ['Wounded', libtcod.dark_red]
                elif hero_health_percent <= 0.8:
                    hero_health = ['Bruised', libtcod.light_blue]
                else:
                    hero_health = ['Healthy', libtcod.dark_green]

                libtcod.console_set_foreground_color(hero_popup, libtcod.dark_gray)
                libtcod.console_print_left(hero_popup, 1, (hero_view * 10) + 5, libtcod.BKGND_NONE,
                                           '------------------------------------------------------')
                libtcod.console_set_foreground_color(hero_popup, libtcod.light_yellow)
                libtcod.console_print_left(hero_popup, 1, (hero_view * 10) + 5, libtcod.BKGND_NONE,
                                           hero.name + ' of the ' + hero.faction + '.')
                libtcod.console_set_foreground_color(hero_popup, libtcod.dark_green)
                libtcod.console_print_left(hero_popup, 1, (hero_view * 10) + 6, libtcod.BKGND_NONE,
                                           'LVL' + str(hero.base_level))
                libtcod.console_print_right(hero_popup, 58, (hero_view * 10) + 6, libtcod.BKGND_NONE,
                                            map[hero.x][hero.y].name)
                libtcod.console_set_foreground_color(hero_popup, libtcod.green)
                libtcod.console_print_left(hero_popup, 4, (hero_view * 10) + 6, libtcod.BKGND_NONE,
                                           str(hero.base_level))
                libtcod.console_set_foreground_color(hero_popup, hero_health[1])
                libtcod.console_print_left(hero_popup, 10, (hero_view * 10) + 6, libtcod.BKGND_NONE, hero_health[0])

                libtcod.console_set_foreground_color(hero_popup, libtcod.dark_yellow)
                if len(hero.inventory) > 0:

                    has_armor = 0
                    has_weapon = 0
                    has_clothing = 0
                    scrolls_held = 0

                    for item in hero.inventory:
                        item_type = master_item_list[item[0]][9]
                        if item_type == 'armor':
                            has_armor += 1

                        if item_type == 'weapon':
                            has_weapon += 1

                        if item_type == 'clothing':
                            has_clothing += 1

                        if item_type == 'scroll':
                            scrolls_held += 1

                    libtcod.console_print_left(hero_popup, 2, (hero_view * 10) + 7, libtcod.BKGND_NONE,
                                               'Carrying ' + str(has_armor) + ' suit(s) of armor, ' + str(
                                                   has_weapon) + ' weapon(s),')
                    libtcod.console_print_left(hero_popup, 2, (hero_view * 10) + 8, libtcod.BKGND_NONE,
                                               str(has_clothing) + ' item(s) of clothing and ' + str(
                                                   scrolls_held) + ' scroll(s).')

                if hero.equipment['clothing'] == 0 or hero_health_percent <= 0:
                    clothing = 'Nothing'
                else:
                    clothing = player_item_display(hero.equipment['clothing'])

                if hero.equipment['armor'] == 0 or hero_health_percent <= 0:
                    armor = 'Nothing'
                else:
                    armor = player_item_display(hero.equipment['armor'])

                if hero.equipment['weapon'] == 0 or hero_health_percent <= 0:
                    weapon = 'Nothing'
                else:
                    weapon = player_item_display(hero.equipment['weapon'])

                libtcod.console_set_foreground_color(hero_popup, libtcod.gray)
                libtcod.console_print_left(hero_popup, 1, (hero_view * 10) + 10, libtcod.BKGND_NONE, 'Wearing:')
                libtcod.console_print_left(hero_popup, 1, (hero_view * 10) + 11, libtcod.BKGND_NONE, 'Wielding:')
                libtcod.console_print_left(hero_popup, 1, (hero_view * 10) + 12, libtcod.BKGND_NONE, 'Armored:')

                libtcod.console_print_left(hero_popup, 36, (hero_view * 10) + 9, libtcod.BKGND_NONE,
                                           'Has recently killed:')

                libtcod.console_set_foreground_color(hero_popup, libtcod.yellow)
                libtcod.console_print_left(hero_popup, 11, (hero_view * 10) + 10, libtcod.BKGND_NONE, clothing)
                libtcod.console_print_left(hero_popup, 11, (hero_view * 10) + 11, libtcod.BKGND_NONE, weapon)
                libtcod.console_print_left(hero_popup, 11, (hero_view * 10) + 12, libtcod.BKGND_NONE, armor)

                libtcod.console_set_foreground_color(hero_popup, libtcod.red)
                libtcod.console_print_right(hero_popup, 58, (hero_view * 10) + 5, libtcod.BKGND_NONE,
                                            'IN DUNGEON lvl ' + str(hero.in_dungeon))

                number_kills = len(hero.activitylog['kills'])

                murderlist = hero.activitylog['kills'][:]

                murderlist.reverse()

                if log_information:
                    log_info(str(murderlist))

                if number_kills > 4:
                    number_kills = 4

                for n in range(number_kills):
                    libtcod.console_print_left(hero_popup, 36, (hero_view * 10) + 10 + n, libtcod.BKGND_NONE,
                                               murderlist[n])

            libtcod.console_blit(hero_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
            libtcod.console_flush()

            key = libtcod.console_wait_for_keypress(True)

            if key.c == 122:  # z
                offset -= 1
            elif key.c == 120:  # x
                offset += 1
            elif key.c == 104:  # h
                hero_mode = 3
                offset = 0

            if offset < 1:
                offset = 0

            if offset >= 1:
                libtcod.console_set_foreground_color(hero_popup, libtcod.gray)
                libtcod.console_print_left(hero_popup, 3, 4, libtcod.BKGND_NONE, '*more*')

            if hero_display + offset < numberheroes:
                libtcod.console_set_foreground_color(hero_popup, libtcod.gray)
                libtcod.console_print_left(hero_popup, 3, 34, libtcod.BKGND_NONE, '*more*')

            if offset + hero_display > numberheroes:
                offset -= 1

        elif hero_mode == 3:

            numberheroes = len(hero_list)

            if numberheroes > 30:
                hero_display = 30
            else:
                hero_display = len(hero_list)

            for clearx in range(popup_width):  # draw a box, clear text
                for cleary in range(popup_height):
                    libtcod.console_set_back(hero_popup, clearx, cleary, libtcod.Color(15, 35, 45), libtcod.BKGND_SET)
                    libtcod.console_print_left(hero_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

            libtcod.console_set_foreground_color(hero_popup, libtcod.red)
            libtcod.console_print_left(hero_popup, 1, 1, libtcod.BKGND_NONE, 'H E R O   R O S T E R')
            libtcod.console_set_foreground_color(hero_popup, libtcod.yellow)
            libtcod.console_print_left(hero_popup, 26, 1, libtcod.BKGND_NONE, 'Other Heroes')
            libtcod.console_set_foreground_color(hero_popup, libtcod.dark_red)
            libtcod.console_print_left(hero_popup, 26, 2, libtcod.BKGND_NONE, 'z/x to scroll - enter to exit')
            for line in range(popup_width):
                libtcod.console_put_char(hero_popup, line, 3, '=', libtcod.BKGND_NONE)

            current_offset = offset

            namecolor = libtcod.light_blue

            # write the information to screen
            for hero_view in range(hero_display):
                hero = hero_list[hero_view + offset]

                libtcod.console_set_foreground_color(hero_popup, libtcod.dark_gray)
                libtcod.console_print_left(hero_popup, 1, hero_view + 5, libtcod.BKGND_NONE,
                                           '------------------------------------------------------')
                if namecolor == libtcod.light_blue:
                    namecolor = libtcod.light_yellow
                    moneycolor = libtcod.yellow
                    levelcolor = libtcod.green
                else:
                    namecolor = libtcod.light_blue
                    moneycolor = libtcod.dark_yellow
                    levelcolor = libtcod.dark_green
                libtcod.console_set_foreground_color(hero_popup, namecolor)
                libtcod.console_print_left(hero_popup, 1, hero_view + 5, libtcod.BKGND_NONE,
                                           hero.name + ' of the ' + hero.faction + '.')
                libtcod.console_set_foreground_color(hero_popup, levelcolor)
                libtcod.console_print_right(hero_popup, 58, hero_view + 5, libtcod.BKGND_NONE,
                                            'LVL' + str(hero.base_level))
                libtcod.console_set_foreground_color(hero_popup, moneycolor)
                libtcod.console_print_right(hero_popup, 52, hero_view + 5, libtcod.BKGND_NONE, '$' + str(hero.wealth))

            libtcod.console_blit(hero_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
            libtcod.console_flush()

            key = libtcod.console_wait_for_keypress(True)

            if key.c == 122:  # z
                offset -= 1
            elif key.c == 120:  # x
                offset += 1
            elif key.c == 104:  # h
                hero_mode = 1
                offset = 0

            if offset < 1:
                offset = 0

            if offset >= 1:
                libtcod.console_set_foreground_color(hero_popup, libtcod.gray)
                libtcod.console_print_left(hero_popup, 3, 4, libtcod.BKGND_NONE, '*more*')

            if hero_display + offset < numberheroes:
                libtcod.console_set_foreground_color(hero_popup, libtcod.gray)
                libtcod.console_print_left(hero_popup, 3, 34, libtcod.BKGND_NONE, '*more*')

            if offset + hero_display > numberheroes:
                offset -= 1


def contract_interface():
    popup_width = 60
    popup_height = 36

    popup_xoffset = 3
    popup_yoffset = 3

    contract_popup = libtcod.console_new(popup_width, popup_height)

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(contract_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
    libtcod.console_blit(contract_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1, popup_yoffset - 1, 0.75,
                         0.75)

    # set up screen scrolling
    offset = 0

    contracts_full = the_mayoress.noticeboard.notices
    contracts = []

    for this_contract in contracts_full:
        if this_contract.visible:
            contracts.append(this_contract)

    key = libtcod.console_check_for_keypress()

    while not key.vk == libtcod.KEY_ENTER:

        numbercontracts = len(contracts)

        if numbercontracts > 10:
            contract_display = 10
        else:
            contract_display = len(contracts)

        for clearx in range(popup_width):  # draw a box, clear text
            for cleary in range(popup_height):
                libtcod.console_set_back(contract_popup, clearx, cleary, libtcod.Color(45, 35, 15), libtcod.BKGND_SET)
                libtcod.console_print_left(contract_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

        libtcod.console_set_foreground_color(contract_popup, libtcod.light_yellow)
        libtcod.console_print_left(contract_popup, 1, 1, libtcod.BKGND_NONE, 'C O N T R A C T S')
        libtcod.console_set_foreground_color(contract_popup, libtcod.gray)
        libtcod.console_print_left(contract_popup, 1, 2, libtcod.BKGND_NONE, 'C to offer new contract')
        libtcod.console_set_foreground_color(contract_popup, libtcod.yellow)
        libtcod.console_print_left(contract_popup, 26, 1, libtcod.BKGND_NONE, 'Town Noticeboard')
        libtcod.console_set_foreground_color(contract_popup, libtcod.light_blue)
        libtcod.console_print_left(contract_popup, 26, 2, libtcod.BKGND_NONE, 'z/x to scroll - enter to exit')

        for line in range(popup_width):
            libtcod.console_put_char(contract_popup, line, 3, '=', libtcod.BKGND_NONE)

        current_offset = offset

        # write the information to screen
        for contract_view in range(contract_display):
            contract = contracts[contract_view + offset]

            # CONTRACT STRUCTURE['dungeon', 'dungeon_name', 'item_fetch', COST, 'faction', 'assigned' ]
            asking_price = contract.asking_price
            mission_type = contract.mission_type
            target_name = contract.target_name
            contract_type = contract.contract_type
            asking_faction = contract.asking_faction
            assigned = contract.accepted
            paid = contract.paid

            libtcod.console_set_foreground_color(contract_popup, libtcod.dark_gray)
            libtcod.console_print_left(contract_popup, 1, (contract_view * 3) + 5, libtcod.BKGND_NONE,
                                       '------------------------------------------------------')

            # check the type of the current contract
            if assigned:
                libtcod.console_set_foreground_color(contract_popup, libtcod.dark_blue)
            else:
                libtcod.console_set_foreground_color(contract_popup, libtcod.light_blue)
            if contract_type == 'dungeon':
                if mission_type == 'default':
                    libtcod.console_print_left(contract_popup, 1, (contract_view * 3) + 5, libtcod.BKGND_NONE,
                                               'Dungeon Delve')
                elif mission_type == 'item_hunt':
                    libtcod.console_print_left(contract_popup, 1, (contract_view * 3) + 5, libtcod.BKGND_NONE,
                                               'Item Hunt    ')
            elif contract_type == 'monster':
                libtcod.console_print_left(contract_popup, 1, (contract_view * 3) + 5, libtcod.BKGND_NONE,
                                           'Monster Hunt ')
            elif mission_type == 'raise_dead':
                libtcod.console_print_left(contract_popup, 1, (contract_view * 3) + 5, libtcod.BKGND_NONE,
                                           'Rescue Corpse')

            # show the target of the contract
            libtcod.console_set_foreground_color(contract_popup, libtcod.dark_green)
            libtcod.console_print_left(contract_popup, 1, (contract_view * 3) + 6, libtcod.BKGND_NONE, target_name)

            if paid:
                libtcod.console_set_foreground_color(contract_popup, libtcod.light_green)
            else:
                libtcod.console_set_foreground_color(contract_popup, libtcod.light_red)
            libtcod.console_print_left(contract_popup, 2 + len(target_name), (contract_view * 3) + 6,
                                       libtcod.BKGND_NONE, '$' + str(asking_price))

            if assigned:
                libtcod.console_set_foreground_color(contract_popup, libtcod.light_red)
                libtcod.console_print_right(contract_popup, 58, (contract_view * 3) + 6, libtcod.BKGND_NONE, assigned)
            else:
                libtcod.console_set_foreground_color(contract_popup, libtcod.light_gray)
                libtcod.console_print_right(contract_popup, 58, (contract_view * 3) + 6, libtcod.BKGND_NONE,
                                            'not assigned')

            libtcod.console_set_foreground_color(contract_popup, libtcod.yellow)
            libtcod.console_print_right(contract_popup, 58, (contract_view * 3) + 5, libtcod.BKGND_NONE,
                                        'offered by ' + asking_faction)

        libtcod.console_blit(contract_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
        libtcod.console_flush()

        key = libtcod.console_wait_for_keypress(True)

        if key.c == 122:  # z
            offset -= 1
        elif key.c == 120:  # x
            offset += 1
        elif key.c == 67:  # big C
            create_contract_interface()
            contracts_full = the_mayoress.noticeboard.notices
            contracts = []

            for this_contract in contracts_full:
                if this_contract.visible:
                    contracts.append(this_contract)

        if offset < 1:
            offset = 0

        if offset + contract_display > numbercontracts:
            offset -= 1

        if offset >= 1:
            libtcod.console_set_foreground_color(contract_popup, libtcod.gray)
            libtcod.console_print_left(contract_popup, 3, 4, libtcod.BKGND_NONE, '*more*')

        if contract_display + offset < numbercontracts:
            libtcod.console_set_foreground_color(contract_popup, libtcod.gray)
            libtcod.console_print_left(contract_popup, 3, 34, libtcod.BKGND_NONE, '*more*')


def create_contract_interface():
    global contract_list

    popup_width = 27
    popup_height = 23

    popup_xoffset = 5
    popup_yoffset = 15

    # CONTRACT STRUCTURE['dungeon', 'dungeon_name', 'item_fetch', COST, 'faction', 'assigned' ]

    contract_price = contract_base_price  # set this to default acceptance value - for ease of new players
    contract_type = 'item_hunt'
    number_contract_types = len(contract_types)

    number_monsters = len(monster_list)
    monster_index = 0

    number_dungeons = len(dungeon_list)
    dungeon_index = 0

    contract_bid_popup = libtcod.console_new(popup_width, popup_height)

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(contract_bid_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
    libtcod.console_blit(contract_bid_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1, popup_yoffset - 1,
                         0.5, 0.5)
    libtcod.console_flush()

    key = libtcod.console_check_for_keypress()

    while not key.vk == libtcod.KEY_ENTER:

        libtcod.console_set_foreground_color(contract_bid_popup, libtcod.white)
        libtcod.console_print_left(contract_bid_popup, 1, 1, libtcod.BKGND_NONE, 'OFFER NEW CONTRACT')
        libtcod.console_set_foreground_color(contract_bid_popup, libtcod.gray)
        libtcod.console_print_left(contract_bid_popup, 1, 2, libtcod.BKGND_NONE, 'Use the keys to set the')
        libtcod.console_print_left(contract_bid_popup, 1, 3, libtcod.BKGND_NONE, 'terms of the contract. ')
        libtcod.console_print_left(contract_bid_popup, 1, 6, libtcod.BKGND_NONE, 'z/x -/+ 1, a/s -/+ 10  ')
        libtcod.console_print_left(contract_bid_popup, 1, 7, libtcod.BKGND_NONE, 'MODIFY CONTRACT VALUE  ')
        libtcod.console_set_foreground_color(contract_bid_popup, libtcod.light_red)
        libtcod.console_print_left(contract_bid_popup, 5, 5, libtcod.BKGND_NONE, '                        ')
        libtcod.console_print_left(contract_bid_popup, 5, 4, libtcod.BKGND_NONE,
                                   '$' + str(contract_price) + '            ')

        libtcod.console_set_foreground_color(contract_bid_popup, libtcod.light_red)
        if contract_type == 'dungeon':
            libtcod.console_print_left(contract_bid_popup, 1, 9, libtcod.BKGND_NONE, 'Dungeon Delve    ')
        elif contract_type == 'monster':
            libtcod.console_print_left(contract_bid_popup, 1, 9, libtcod.BKGND_NONE, 'Monster Hunt     ')
        elif contract_type == 'item_hunt':
            libtcod.console_print_left(contract_bid_popup, 1, 9, libtcod.BKGND_NONE, 'Item Hunt        ')
        elif contract_type == 'cancel':
            libtcod.console_print_left(contract_bid_popup, 1, 9, libtcod.BKGND_NONE, 'CANCEL CONTRACT  ')
        libtcod.console_set_foreground_color(contract_bid_popup, libtcod.gray)
        libtcod.console_print_left(contract_bid_popup, 2, 10, libtcod.BKGND_NONE, 'e to')
        libtcod.console_print_left(contract_bid_popup, 1, 11, libtcod.BKGND_NONE, 'MODIFY CONTRACT TYPE')

        if contract_type == 'dungeon':
            libtcod.console_set_foreground_color(contract_bid_popup, libtcod.gray)
            libtcod.console_print_left(contract_bid_popup, 1, 17, libtcod.BKGND_NONE, 'Dungeon Delve offers a   ')
            libtcod.console_print_left(contract_bid_popup, 1, 18, libtcod.BKGND_NONE, 'fixed price for a hero to')
            libtcod.console_print_left(contract_bid_popup, 1, 19, libtcod.BKGND_NONE, 'adventure on your behalf.')
            libtcod.console_print_left(contract_bid_popup, 1, 20, libtcod.BKGND_NONE, '                         ')
            libtcod.console_print_left(contract_bid_popup, 1, 21, libtcod.BKGND_NONE, '                         ')
            if number_dungeons == 0:
                libtcod.console_set_foreground_color(contract_bid_popup, libtcod.gray)
                libtcod.console_print_left(contract_bid_popup, 1, 13, libtcod.BKGND_NONE, 'No Dungeons               ')
            else:
                libtcod.console_set_foreground_color(contract_bid_popup, libtcod.light_red)
                libtcod.console_print_left(contract_bid_popup, 1, 13, libtcod.BKGND_NONE, '                          ')
                libtcod.console_print_left(contract_bid_popup, 1, 13, libtcod.BKGND_NONE,
                                           '(' + str(dungeon_list[dungeon_index][0]) + ')' + str(
                                               dungeon_list[dungeon_index][1]))

        elif contract_type == 'item_hunt':
            libtcod.console_set_foreground_color(contract_bid_popup, libtcod.gray)
            libtcod.console_print_left(contract_bid_popup, 1, 17, libtcod.BKGND_NONE, 'Item Hunt offers a fixed ')
            libtcod.console_print_left(contract_bid_popup, 1, 18, libtcod.BKGND_NONE, 'price for a hero to loot ')
            libtcod.console_print_left(contract_bid_popup, 1, 19, libtcod.BKGND_NONE, 'an item out of a dungeon ')
            libtcod.console_print_left(contract_bid_popup, 1, 20, libtcod.BKGND_NONE, 'on your behalf.          ')
            libtcod.console_print_left(contract_bid_popup, 1, 21, libtcod.BKGND_NONE, '                         ')
            if number_dungeons == 0:
                libtcod.console_set_foreground_color(contract_bid_popup, libtcod.gray)
                libtcod.console_print_left(contract_bid_popup, 1, 13, libtcod.BKGND_NONE, 'No Dungeons               ')
            else:
                libtcod.console_set_foreground_color(contract_bid_popup, libtcod.light_red)
                libtcod.console_print_left(contract_bid_popup, 1, 13, libtcod.BKGND_NONE, '                          ')
                libtcod.console_print_left(contract_bid_popup, 1, 13, libtcod.BKGND_NONE,
                                           '(' + str(dungeon_list[dungeon_index][0]) + ')' + str(
                                               dungeon_list[dungeon_index][1]))

        elif contract_type == 'cancel':
            libtcod.console_set_foreground_color(contract_bid_popup, libtcod.gray)
            libtcod.console_print_left(contract_bid_popup, 1, 17, libtcod.BKGND_NONE, 'Cancel the contract      ')
            libtcod.console_print_left(contract_bid_popup, 1, 18, libtcod.BKGND_NONE, 'creation process         ')
            libtcod.console_print_left(contract_bid_popup, 1, 19, libtcod.BKGND_NONE, '                         ')
            libtcod.console_print_left(contract_bid_popup, 1, 20, libtcod.BKGND_NONE, '                         ')
            libtcod.console_print_left(contract_bid_popup, 1, 21, libtcod.BKGND_NONE, '                         ')
            libtcod.console_print_left(contract_bid_popup, 1, 13, libtcod.BKGND_NONE, '            ')

        elif contract_type == 'monster':
            libtcod.console_set_foreground_color(contract_bid_popup, libtcod.gray)
            libtcod.console_print_left(contract_bid_popup, 1, 17, libtcod.BKGND_NONE, 'Monster Hunt offers a    ')
            libtcod.console_print_left(contract_bid_popup, 1, 18, libtcod.BKGND_NONE, 'fixed price for a hero to')
            libtcod.console_print_left(contract_bid_popup, 1, 19, libtcod.BKGND_NONE, 'engage a monster on the  ')
            libtcod.console_print_left(contract_bid_popup, 1, 20, libtcod.BKGND_NONE, 'rampage.                 ')
            libtcod.console_print_left(contract_bid_popup, 1, 21, libtcod.BKGND_NONE, 'Protect the town!        ')
            if number_monsters == 0:
                libtcod.console_set_foreground_color(contract_bid_popup, libtcod.gray)
                libtcod.console_print_left(contract_bid_popup, 1, 13, libtcod.BKGND_NONE, '                        ')
                libtcod.console_print_left(contract_bid_popup, 1, 13, libtcod.BKGND_NONE, 'No Monsters   ')
            else:
                libtcod.console_set_foreground_color(contract_bid_popup, libtcod.light_red)
                libtcod.console_print_left(contract_bid_popup, 1, 13, libtcod.BKGND_NONE, '                        ')
                libtcod.console_print_left(contract_bid_popup, 1, 13, libtcod.BKGND_NONE,
                                           '(' + str(monster_list[monster_index].base_level) + ')' + monster_list[
                                               monster_index].name)

        libtcod.console_set_foreground_color(contract_bid_popup, libtcod.gray)
        libtcod.console_print_left(contract_bid_popup, 2, 14, libtcod.BKGND_NONE, 'd/f to')
        libtcod.console_print_left(contract_bid_popup, 1, 15, libtcod.BKGND_NONE, 'MODIFY CONTRACT TARGET')

        # print result of change in contract
        libtcod.console_blit(contract_bid_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset, 1)
        libtcod.console_flush()
        # wait for key to modify bid, or submit
        key = libtcod.console_wait_for_keypress(True)

        if key.c == 122:  # z
            contract_price -= 1
        elif key.c == 120:  # x
            contract_price += 1
        elif key.c == 97:  # a
            contract_price -= 10
        elif key.c == 115:  # s
            contract_price += 10

        elif key.c == 101:  # e
            if contract_type == 'item_hunt':
                contract_type = 'monster'
            elif contract_type == 'dungeon':
                contract_type = 'item_hunt'
            elif contract_type == 'monster':
                contract_type = 'cancel'
            else:
                contract_type = 'dungeon'

        elif key.c == 100:  # d
            monster_index -= 1
            dungeon_index -= 1

        elif key.c == 102:  # f
            monster_index += 1
            dungeon_index += 1

        if contract_price < 10:
            contract_price = 10

        if dungeon_index > number_dungeons - 1:
            dungeon_index = 0
        if dungeon_index < 0:
            dungeon_index = number_dungeons - 1

        if monster_index > number_monsters - 1:
            monster_index = 0
        if monster_index < 0:
            monster_index = number_monsters - 1

    if contract_type == 'monster':
        if player.wealth < contract_price:
            message('Insufficient funds to honour the contract! Contract not offered.', libtcod.light_red,
                    libtcod.dark_red)
        elif number_monsters == 0:
            message('There are no monsters to attack! Contract not offered.', libtcod.light_red, libtcod.dark_red)
        else:
            target_name = monster_list[monster_index].name
            generate_contract(contract_price, 'monster_hunt', target_name, 'monster', player_name,
                              ['glory', 'contracts'], True, False, False)
            message('Contract generated. Offering $' + str(contract_price) + ' for the head of ' + monster_list[
                monster_index].name + '!', libtcod.light_yellow, libtcod.dark_yellow)

    elif contract_type == 'dungeon':
        if number_dungeons == 0:
            message('There are no dungeons present in the region! Contract not offered.', libtcod.light_red,
                    libtcod.dark_red)
        else:
            target_name = dungeon_list[dungeon_index][1]
            generate_contract(contract_price, 'default', target_name, 'dungeon', player_name,
                              ['glory', 'leadership', 'contracts'], True, False, False)
            message('Contract generated. Offering $' + str(contract_price) + ' for assaulting the ' +
                    dungeon_list[dungeon_index][1] + '!', libtcod.light_yellow, libtcod.dark_yellow)

    elif contract_type == 'item_hunt':
        if number_dungeons == 0:
            message('There are no dungeons present in the region! Contract not offered.', libtcod.light_red,
                    libtcod.dark_red)
        else:
            target_name = dungeon_list[dungeon_index][1]
            generate_contract(contract_price, 'item_hunt', target_name, 'dungeon', player_name, ['loot'], True, False,
                              False)
            message('Contract generated. Offering $' + str(contract_price) + ' for plunder from the ' +
                    dungeon_list[dungeon_index][1] + '!', libtcod.light_yellow, libtcod.dark_yellow)

    elif contract_type == 'cancel':
        message('Contract not offered.', libtcod.light_red, libtcod.dark_red)


def discuss_contract(contract_index, hero):
    contract = the_mayoress.noticeboard.notices[contract_index]

    popup_width = 24
    popup_height = 20

    popup_xoffset = 5
    popup_yoffset = 15

    contract_type = contract.contract_type
    target_name = contract.target_name
    mission_type = contract.mission_type
    asking_price = contract.asking_price
    asking_faction = contract.asking_faction
    assigned = contract.accepted

    hero_name = hero.name
    hero_faction = hero.faction
    hero_level = hero.base_level

    contract_accept = 0

    discuss_contract_popup = libtcod.console_new(popup_width, popup_height)

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(discuss_contract_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
    libtcod.console_blit(discuss_contract_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1,
                         popup_yoffset - 1, 0.5, 0.5)
    libtcod.console_flush()

    key = libtcod.console_check_for_keypress()

    while not key.vk == libtcod.KEY_ENTER:

        libtcod.console_set_foreground_color(discuss_contract_popup, libtcod.gray)
        if mission_type == 'item_hunt':
            libtcod.console_print_left(discuss_contract_popup, 1, 1, libtcod.BKGND_NONE, ' Hero takes cash on   ')
            libtcod.console_print_left(discuss_contract_popup, 1, 2, libtcod.BKGND_NONE, ' delivery of item(s): ')

        else:
            libtcod.console_print_left(discuss_contract_popup, 1, 1, libtcod.BKGND_NONE, ' Hero is looking for  ')
            libtcod.console_print_left(discuss_contract_popup, 1, 2, libtcod.BKGND_NONE, '   payment upfront:   ')

        libtcod.console_print_left(discuss_contract_popup, 1, 7, libtcod.BKGND_NONE, 'of the                 ')
        libtcod.console_print_left(discuss_contract_popup, 1, 10, libtcod.BKGND_NONE, 'CONTRACT DETAILS:  ')

        libtcod.console_set_foreground_color(discuss_contract_popup, libtcod.light_green)
        libtcod.console_print_left(discuss_contract_popup, 1, 4, libtcod.BKGND_NONE, '$' + str(asking_price))
        libtcod.console_set_foreground_color(discuss_contract_popup, libtcod.light_red)
        libtcod.console_print_left(discuss_contract_popup, 1, 6, libtcod.BKGND_NONE, hero_name)
        libtcod.console_print_left(discuss_contract_popup, 8, 7, libtcod.BKGND_NONE, hero_faction)
        libtcod.console_print_left(discuss_contract_popup, 1, 8, libtcod.BKGND_NONE, '(Level ' + str(hero_level) + ')')

        libtcod.console_set_foreground_color(discuss_contract_popup, libtcod.light_red)
        if contract_type == 'dungeon':
            if mission_type == 'default':
                libtcod.console_print_left(discuss_contract_popup, 2, 11, libtcod.BKGND_NONE, 'Dungeon Delve    ')
            elif mission_type == 'item_hunt':
                libtcod.console_print_left(discuss_contract_popup, 2, 11, libtcod.BKGND_NONE, 'Item Hunt        ')
        elif contract_type == 'monster':
            libtcod.console_print_left(discuss_contract_popup, 2, 11, libtcod.BKGND_NONE, 'Monster Hunt     ')
        libtcod.console_set_foreground_color(discuss_contract_popup, libtcod.red)
        libtcod.console_print_left(discuss_contract_popup, 3, 12, libtcod.BKGND_NONE, target_name)

        if contract_accept == 1:
            libtcod.console_set_foreground_color(discuss_contract_popup, libtcod.light_green)
            libtcod.console_print_left(discuss_contract_popup, 5, 14, libtcod.BKGND_NONE, 'y to accept')
            libtcod.console_set_foreground_color(discuss_contract_popup, libtcod.gray)
            libtcod.console_print_left(discuss_contract_popup, 5, 15, libtcod.BKGND_NONE, 'n to reject')
        else:
            libtcod.console_set_foreground_color(discuss_contract_popup, libtcod.gray)
            libtcod.console_print_left(discuss_contract_popup, 5, 14, libtcod.BKGND_NONE, 'y to accept')
            libtcod.console_set_foreground_color(discuss_contract_popup, libtcod.light_red)
            libtcod.console_print_left(discuss_contract_popup, 5, 15, libtcod.BKGND_NONE, 'n to reject')

        libtcod.console_set_foreground_color(discuss_contract_popup, libtcod.gray)
        libtcod.console_print_left(discuss_contract_popup, 2, 17, libtcod.BKGND_NONE, 'Enter to confirm')

        # print result of change in contract
        libtcod.console_blit(discuss_contract_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset,
                             1)
        libtcod.console_flush()
        # wait for key to modify bid, or submit
        key = libtcod.console_wait_for_keypress(True)

        if key.c == 121:  # y
            contract_accept = 1
        elif key.c == 110:  # n
            contract_accept = 0

    if contract_accept == 1:
        return True
    else:
        return False


def generate_contract(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive, visible,
                      paid, accepted):
    new_contract = Contract(asking_price, mission_type, target_name, contract_type, asking_faction, defining_motive,
                            visible, paid, accepted)
    the_mayoress.noticeboard.notices.append(new_contract)


def dungeon_interface():
    popup_width = 60
    popup_height = 36

    popup_xoffset = 3
    popup_yoffset = 3

    dungeon_popup = libtcod.console_new(popup_width, popup_height)

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(dungeon_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
    libtcod.console_blit(dungeon_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1, popup_yoffset - 1, 0.5,
                         0.5)


    # set up screen scrolling
    offset = 0

    numberdungeons = len(dungeon_list)

    if numberdungeons > 10:
        dungeon_display = 10
    else:
        dungeon_display = len(dungeon_list)

    key = libtcod.console_check_for_keypress()
    while not key.vk == libtcod.KEY_ENTER:

        for clearx in range(popup_width):  # draw a box, clear text
            for cleary in range(popup_height):
                libtcod.console_set_back(dungeon_popup, clearx, cleary, libtcod.Color(25, 15, 15), libtcod.BKGND_SET)
                libtcod.console_print_left(dungeon_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

        libtcod.console_set_foreground_color(dungeon_popup, libtcod.red)
        libtcod.console_print_left(dungeon_popup, 1, 1, libtcod.BKGND_NONE, 'D U N G E O N  R O S T E R')
        libtcod.console_set_foreground_color(dungeon_popup, libtcod.dark_red)
        libtcod.console_print_left(dungeon_popup, 30, 1, libtcod.BKGND_NONE, 'z/x to scroll - enter to exit')
        for line in range(popup_width):
            libtcod.console_put_char(dungeon_popup, line, 3, '=', libtcod.BKGND_NONE)

        current_offset = offset

        if key.c == 122:  # z
            offset -= 1
        elif key.c == 120:  # x
            offset += 1

        if offset < 1:
            offset = 0

        if offset >= 1:
            libtcod.console_set_foreground_color(dungeon_popup, libtcod.gray)
            libtcod.console_print_left(dungeon_popup, 3, 4, libtcod.BKGND_NONE, '*more*')

        if dungeon_display + offset < numberdungeons:
            libtcod.console_set_foreground_color(dungeon_popup, libtcod.gray)
            libtcod.console_print_left(dungeon_popup, 3, 34, libtcod.BKGND_NONE, '*more*')

        if offset + dungeon_display > numberdungeons:
            offset = current_offset

        # write the information to screen
        for dungeon_view in range(dungeon_display):
            dungeon = dungeon_list[dungeon_view + offset]

            dun_x = dungeon[2]
            dun_y = dungeon[3]

            dungeon_map = map[dun_x][dun_y]

            libtcod.console_set_foreground_color(dungeon_popup, libtcod.dark_gray)
            libtcod.console_print_left(dungeon_popup, 1, (dungeon_view * 3) + 5, libtcod.BKGND_NONE,
                                       '------------------------------------------------------')
            libtcod.console_set_foreground_color(dungeon_popup, libtcod.light_yellow)
            libtcod.console_print_left(dungeon_popup, 1, (dungeon_view * 3) + 5, libtcod.BKGND_NONE, dungeon[1])
            libtcod.console_set_foreground_color(dungeon_popup, libtcod.dark_green)
            libtcod.console_print_left(dungeon_popup, 1, (dungeon_view * 3) + 6, libtcod.BKGND_NONE,
                                       'LVL' + str(dungeon_map.dungeon.base_level))
            libtcod.console_set_foreground_color(dungeon_popup, libtcod.dark_yellow)
            libtcod.console_print_left(dungeon_popup, 10, (dungeon_view * 3) + 6, libtcod.BKGND_NONE,
                                       '$' + str(dungeon_map.dungeon.wealth))
            libtcod.console_set_foreground_color(dungeon_popup, libtcod.dark_yellow)
            libtcod.console_print_left(dungeon_popup, 17, (dungeon_view * 3) + 6, libtcod.BKGND_NONE,
                                       str(len(dungeon_map.dungeon.inventory)) + ' items')
            libtcod.console_set_foreground_color(dungeon_popup, libtcod.dark_yellow)
            libtcod.console_print_left(dungeon_popup, 30, (dungeon_view * 3) + 6, libtcod.BKGND_NONE,
                                       str(dungeon_map.dungeon.population) + ' monsters')
        libtcod.console_blit(dungeon_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
        libtcod.console_flush()

        key = libtcod.console_wait_for_keypress(True)


def player_item_edit_value(index):
    popup_width = 22
    popup_height = 12

    popup_xoffset = 4
    popup_yoffset = 24

    set_value = player.inventory[index][5]
    value_popup = libtcod.console_new(popup_width, popup_height)

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(value_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
    libtcod.console_blit(value_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1, popup_yoffset - 1, 0.75,
                         0.75)

    for clearx in range(popup_width):  # draw a box, clear text
        for cleary in range(popup_height):
            libtcod.console_set_back(value_popup, clearx, cleary, libtcod.Color(10, 15, 45), libtcod.BKGND_SET)
            libtcod.console_print_left(value_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

    libtcod.console_print_left(value_popup, 1, 1, libtcod.BKGND_NONE, 'Changing item value.')
    libtcod.console_print_left(value_popup, 5, 3, libtcod.BKGND_NONE, str(set_value) + '    ')
    libtcod.console_print_left(value_popup, 1, 5, libtcod.BKGND_NONE, 'z/x -/+ 1, a/s -/+ 5')
    libtcod.console_print_left(value_popup, 1, 6, libtcod.BKGND_NONE, 'ENTER when happy')

    libtcod.console_blit(value_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset, 1, 1)
    libtcod.console_flush()

    key = libtcod.console_wait_for_keypress(True)

    while not key.vk == libtcod.KEY_ENTER:
        if key.c == 122:  # z
            set_value -= 1
        elif key.c == 120:  # x
            set_value += 1
        elif key.c == 97:  # a
            set_value -= 5
        elif key.c == 115:  # s
            set_value += 5

        if set_value < 1:
            set_value = 1

        libtcod.console_print_left(value_popup, 1, 1, libtcod.BKGND_NONE, 'Changing item value.')
        libtcod.console_print_left(value_popup, 5, 4, libtcod.BKGND_NONE, '                      ')
        libtcod.console_print_left(value_popup, 5, 3, libtcod.BKGND_NONE, str(set_value) + '    ')
        libtcod.console_print_left(value_popup, 1, 5, libtcod.BKGND_NONE, 'z/x -/+ 1, a/s -/+ 5')
        libtcod.console_print_left(value_popup, 1, 6, libtcod.BKGND_NONE, 'ENTER when happy')

        # print result of change in value
        libtcod.console_blit(value_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset, 1, 1)
        libtcod.console_flush()
        # wait for key to modify bid, or submit
        key = libtcod.console_wait_for_keypress(True)

    player.inventory[index][5] = set_value
    message('Item value changed for ' + player_item_display(player.inventory[index]), libtcod.light_yellow,
            libtcod.dark_yellow)
    # feed back in the message screen


def item_interact(x, y, index):
    global item_examined, debug_mode

    popup_width = 30
    popup_height = 29

    popup_xoffset, popup_yoffset = 5, 10

    popup = libtcod.console_new(popup_width, popup_height)  # item interface pop-up

    inventory = map[x][y].shop.inventory
    faction = map[x][y].faction

    testlength = len(inventory)

    if index < testlength:

        # get the relevant item information
        item = inventory[index]
        item_set_value = item[5]
        item_real_value = item[4]
        item_known_quality = item[1][1]
        item_real_quality = item[1][0]
        item_known_bonus = item[2][1]
        item_real_bonus = item[2][0]
        item_curse_status = item[6]

        # check out what we know about the item type:
        known_item = player_item_knowledge_list[item[0]]

        # known_index = known_item[0] #fucker is not used!!!
        known_name = known_item[0]
        known_reason = known_item[1]
        known_description = known_item[2]
        known_level = known_item[3]
        known_align = known_item[4]
        known_order = known_item[5]
        known_faction = known_item[6]
        known_effect = known_item[7]

        # collect the factual information about the item
        real_item = master_item_list[item[0]]

        real_name_simple = real_item[0]
        real_name = real_item[1]
        real_base_value = real_item[2]
        real_level = real_item[3]
        real_alignment = real_item[4]
        real_order = real_item[5]
        real_faction = real_item[6]
        real_effect = real_item[7]
        real_description = real_item[8]
        real_type = real_item[9]

        for clearx in range(popup_width):  # draw a shadow behind the popup
            for cleary in range(popup_height):
                libtcod.console_set_back(popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
        libtcod.console_blit(popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1, popup_yoffset - 1, 0.75,
                             0.75)

        for clearx in range(popup_width):  # draw a box, clear text
            for cleary in range(popup_height):
                libtcod.console_set_back(popup, clearx, cleary, libtcod.Color(45, 15, 10), libtcod.BKGND_SET)
                libtcod.console_print_left(popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

        # show the relevant item information
        libtcod.console_set_foreground_color(popup, libtcod.white)
        libtcod.console_print_left(popup, 7, 3, libtcod.BKGND_NONE, str(item_set_value))
        libtcod.console_print_left(popup, 7, 4, libtcod.BKGND_NONE, item_quality_display(item_known_quality))
        libtcod.console_print_left(popup, 7, 5, libtcod.BKGND_NONE, item_bonus_display(item_known_bonus))

        libtcod.console_print_left(popup, 7, 12, libtcod.BKGND_NONE, real_type)
        libtcod.console_print_left(popup, 7, 13, libtcod.BKGND_NONE, level_display(known_level))
        libtcod.console_print_left(popup, 7, 14, libtcod.BKGND_NONE, align_display(known_align))
        libtcod.console_print_left(popup, 7, 15, libtcod.BKGND_NONE, order_display(known_order))

        if known_name == real_name:
            libtcod.console_print_left(popup, 7, 17, libtcod.BKGND_NONE, str(real_base_value))
        else:
            libtcod.console_print_left(popup, 7, 17, libtcod.BKGND_NONE, 'Unknown')

        if known_faction == real_faction:
            number_factions = len(known_faction)
            for ppp in range(number_factions):
                libtcod.console_print_left(popup, 7, 19 + ppp, libtcod.BKGND_NONE, known_faction[ppp])
        else:
            libtcod.console_print_left(popup, 7, 19, libtcod.BKGND_NONE, 'Unknown')

        libtcod.console_set_foreground_color(popup,
                                             libtcod.yellow)  # item display, consider changing colour based on item?
        libtcod.console_print_left(popup, 1, 1, libtcod.BKGND_NONE, player_item_display(item))

        libtcod.console_set_foreground_color(popup, libtcod.gray)  # titles and real (hidden) information
        libtcod.console_print_left(popup, 1, 3, libtcod.BKGND_NONE, 'value:')
        libtcod.console_print_left(popup, 1, 4, libtcod.BKGND_NONE, 'qulty:')
        libtcod.console_print_left(popup, 1, 5, libtcod.BKGND_NONE, 'bonus:')

        # message(str(debug_mode))

        if debug_mode == 1:
            libtcod.console_print_left(popup, 1, 6, libtcod.BKGND_NONE, 'curse:')  # debug
            libtcod.console_print_left(popup, 15, 5, libtcod.BKGND_NONE, str(item_real_bonus))  # debug
            libtcod.console_print_left(popup, 7, 6, libtcod.BKGND_NONE, str(item_curse_status))  # debug
            libtcod.console_print_left(popup, 15, 4, libtcod.BKGND_NONE, str(item_real_quality))  # debug
            libtcod.console_print_left(popup, 15, 3, libtcod.BKGND_NONE, str(item_real_value))  # debug

        libtcod.console_print_left(popup, 1, 12, libtcod.BKGND_NONE, 'type :')
        libtcod.console_print_left(popup, 1, 13, libtcod.BKGND_NONE, 'level:')
        libtcod.console_print_left(popup, 1, 14, libtcod.BKGND_NONE, 'align:')
        libtcod.console_print_left(popup, 1, 15, libtcod.BKGND_NONE, 'order:')
        libtcod.console_print_left(popup, 1, 16, libtcod.BKGND_NONE, 'item base value:')
        libtcod.console_print_left(popup, 1, 18, libtcod.BKGND_NONE, 'associated factions:')

        if debug_mode == 1:
            libtcod.console_print_left(popup, 15, 12, libtcod.BKGND_NONE, real_name)  # debug
            libtcod.console_print_left(popup, 15, 13, libtcod.BKGND_NONE, str(real_level))  # debug
            libtcod.console_print_left(popup, 15, 14, libtcod.BKGND_NONE, str(real_alignment))  # debug
            libtcod.console_print_left(popup, 15, 15, libtcod.BKGND_NONE, str(real_order))  # debug
            libtcod.console_print_left(popup, 15, 17, libtcod.BKGND_NONE, str(real_base_value))  # debug

        # now look for a keypress to interact
        # EXAMINE, if the object belongs to a player
        # OFFER, if the object belongs to another, so we can buy it

        if faction == player_name:
            if known_name == real_name:
                pawn_value = real_base_value / 2
            else:
                pawn_value = real_level * 5
            if item_examined:
                libtcod.console_set_foreground_color(popup, libtcod.gray)
                libtcod.console_print_left(popup, 2, 8, libtcod.BKGND_NONE, 'E(x)amine Item')
            else:
                libtcod.console_set_foreground_color(popup, libtcod.yellow)
                libtcod.console_print_left(popup, 2, 8, libtcod.BKGND_NONE, 'E(x)amine Item')
            libtcod.console_set_foreground_color(popup, libtcod.yellow)
            libtcod.console_print_left(popup, 2, 9, libtcod.BKGND_NONE, 'Set (V)alue')
            libtcod.console_set_foreground_color(popup, libtcod.chartreuse)
            libtcod.console_print_left(popup, 21, 3, libtcod.BKGND_NONE, '(P)awn')
            libtcod.console_print_left(popup, 21, 4, libtcod.BKGND_NONE, 'to A.H.')
            libtcod.console_set_foreground_color(popup, libtcod.gray)
            libtcod.console_print_left(popup, 21, 5, libtcod.BKGND_NONE, 'for $')
            libtcod.console_set_foreground_color(popup, libtcod.light_chartreuse)
            libtcod.console_print_left(popup, 26, 5, libtcod.BKGND_NONE, str(pawn_value))
            libtcod.console_set_foreground_color(popup, libtcod.gray)
            libtcod.console_print_left(popup, 2, 10, libtcod.BKGND_NONE, 'Any other key to return')
            libtcod.console_blit(popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
            libtcod.console_flush()
            # watch for player appropriate keypresses
            key = libtcod.console_wait_for_keypress(True)

            if key.c == 118:
                player_item_edit_value(index)
            elif key.c == 120:
                if not item_examined:
                    examine_item(item)
                    item_examined = 1
                    update_info_bar()
                else:
                    pass
            elif key.c == 112:  # p for pawn
                pawn(item, pawn_value)
            else:
                pass

        else:
            libtcod.console_set_foreground_color(popup, libtcod.yellow)
            libtcod.console_print_left(popup, 2, 8, libtcod.BKGND_NONE, '(B)uy Item for listed price')
            libtcod.console_set_foreground_color(popup, libtcod.gray)
            libtcod.console_print_left(popup, 2, 10, libtcod.BKGND_NONE, 'Any other key to return')
            libtcod.console_blit(popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
            libtcod.console_flush()
            # watch for enemy appropriate keypresses
            key = libtcod.console_wait_for_keypress(True)

            if key.c == 98:  # b, for buy
                if buy_item(player, map[x][y].shop, index):
                    player.gain_experience(item_experience(item))
                    sales_metrics.log_item_bought(real_type, item_set_value, player_name, day_count)
                    sales_metrics.log_item_sold(real_type, item_set_value, map[x][y].faction, day_count)
                print_status(x, y)

            else:
                pass

    else:
        pass


    # libtcod.console_clear(popup)
    # for clearx in range(INFO_BAR_WIDTH): #empty out previous text (if indeed it was there ...)
    #    for cleary in range(14, 23):
    #        libtcod.console_print_left(inf, clearx, cleary, libtcod.BKGND_NONE, ' ')
    libtcod.console_blit(popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
    libtcod.console_flush()


def pawn(item, value):
    transaction = 'no'

    if find_shop('Auction House'):
        auction_house_location = find_shop('Auction House')
        ax = auction_house_location[0]
        ay = auction_house_location[1]
        if map[ax][ay].shop.wealth >= value:
            player.wealth += value
            player.inventory.remove(item)
            map[ax][ay].shop.inventory.append(item)
            map[ax][ay].shop.wealth -= value
            transaction = 'yes'
    else:
        transaction = 'no_ah'

    if transaction == 'yes':
        log_sale(player_item_display(item), price, 'PAWNED')
        message('Item pawned for $' + str(value), libtcod.light_chartreuse, libtcod.dark_chartreuse)
    elif transaction == 'no':
        message('Auction House low on funds - item not pawned.', libtcod.light_chartreuse, libtcod.dark_chartreuse)
    elif transaction == 'no_ah':
        message('No Auction House - Item not pawned!', libtcod.light_chartreuse, libtcod.dark_chartreuse)


def choose_upgrade():
    global player_specialisms


    # player_specialisms = {'weapon':0,'armor':0,'clothing':0,'scroll':0}

    popup_width = 35
    popup_height = 11

    popup_xoffset, popup_yoffset = 2, 10

    upgrade_popup = libtcod.console_new(popup_width, popup_height)

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(upgrade_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)

    libtcod.console_set_foreground_color(upgrade_popup, libtcod.white)

    n = 0
    libtcod.console_set_foreground_color(upgrade_popup, libtcod.light_yellow)
    libtcod.console_print_left(upgrade_popup, 2, 1, libtcod.BKGND_NONE, 'LEVEL UP,')
    libtcod.console_set_foreground_color(upgrade_popup, libtcod.light_green)
    libtcod.console_print_left(upgrade_popup, 2, 2, libtcod.BKGND_NONE, 'CHOOSE A SPECIALISM:')
    libtcod.console_set_foreground_color(upgrade_popup, libtcod.white)
    for type, value in player_specialisms.iteritems():
        libtcod.console_print_left(upgrade_popup, 1, 4 + n, libtcod.BKGND_NONE, str(n) + ' ' + type + ':')
        libtcod.console_print_left(upgrade_popup, 18, 4 + n, libtcod.BKGND_NONE, str(value))
        n += 1

    libtcod.console_blit(upgrade_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
    libtcod.console_flush()

    chosen = 0

    entering_player_specialisms = player_specialisms

    key = libtcod.console_check_for_keypress()

    while key.vk != libtcod.KEY_ENTER:

        if key.vk == libtcod.KEY_0 or key.vk == libtcod.KEY_KP0:  # choose armor
            chosen = 'armor'
        elif key.vk == libtcod.KEY_1 or key.vk == libtcod.KEY_KP1:  # etc
            chosen = 'weapon'
        elif key.vk == libtcod.KEY_2 or key.vk == libtcod.KEY_KP2:
            chosen = 'clothing'
        elif key.vk == libtcod.KEY_3 or key.vk == libtcod.KEY_KP3:
            chosen = 'scroll'

        n = 0
        for type, value in player_specialisms.iteritems():
            if chosen == type:
                libtcod.console_set_foreground_color(upgrade_popup, libtcod.green)
            else:
                libtcod.console_set_foreground_color(upgrade_popup, libtcod.white)
            libtcod.console_print_left(upgrade_popup, 1, 4 + n, libtcod.BKGND_NONE, str(n) + ' ' + type + ':')
            libtcod.console_print_left(upgrade_popup, 18, 4 + n, libtcod.BKGND_NONE, str(value))
            n += 1

        libtcod.console_blit(upgrade_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
        libtcod.console_flush()

        key = libtcod.console_check_for_keypress()

    if chosen == 0:
        chosen = 'armor'  # default
        player_specialisms['armor'] = entering_player_specialisms['armor'] + 1
    else:
        player_specialisms[chosen] = entering_player_specialisms[chosen] + 1

    n = 0
    for type, value in player_specialisms.iteritems():
        if chosen == type:
            libtcod.console_set_foreground_color(upgrade_popup, libtcod.green)
        else:
            libtcod.console_set_foreground_color(upgrade_popup, libtcod.white)
        libtcod.console_print_left(upgrade_popup, 1, 4 + n, libtcod.BKGND_NONE, str(n) + ' ' + type + ':')
        libtcod.console_print_left(upgrade_popup, 18, 4 + n, libtcod.BKGND_NONE, str(value))
        n += 1

    libtcod.console_set_foreground_color(upgrade_popup, libtcod.white)
    libtcod.console_print_left(upgrade_popup, 1, 9, libtcod.BKGND_NONE, 'You gain experience in ' + chosen + '!')
    libtcod.console_print_left(upgrade_popup, 1, 10, libtcod.BKGND_NONE, '(press enter)')
    libtcod.console_blit(upgrade_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
    libtcod.console_flush()

    key = libtcod.console_wait_for_keypress(True)
    # feedback to the player here ...


def hero_sale(x, y, buy_shop, sell_shop,
              index):  # hero trying to palm off their wares, index given as the hero inventory index

    popup_width = 30
    popup_height = 29

    popup_xoffset, popup_yoffset = 5, 10

    herosale_popup = libtcod.console_new(popup_width, popup_height)  # hero_sale interface pop-up

    inventory = sell_shop.inventory

    faction = map[x][y].faction

    testlength = len(inventory)

    item = inventory[index]

    # collect the factual information about the item
    real_item = master_item_list[item[0]]

    real_name_simple = real_item[0]
    real_name = real_item[1]
    real_base_value = real_item[2]
    real_level = real_item[3]
    real_alignment = real_item[4]
    real_order = real_item[5]
    real_faction = real_item[6]
    real_effect = real_item[7]
    real_description = real_item[8]
    real_type = real_item[9]

    if faction == player_name:  # are we dealing with the player?

        if index < testlength:  # is there an item available?

            key = libtcod.console_check_for_keypress()
            resolved = False
            while not resolved:
                # get the relevant item information
                item_set_value = item[5]
                item_real_value = item[4]
                item_known_quality = item[1][1]
                item_real_quality = item[1][0]
                item_known_bonus = item[2][1]
                item_real_bonus = item[2][0]
                item_curse_status = item[6]

                # check out what we know about the item type:
                known_item = player_item_knowledge_list[item[0]]

                known_name = known_item[0]
                known_reason = known_item[1]
                known_description = known_item[2]
                known_level = known_item[3]
                known_align = known_item[4]
                known_order = known_item[5]
                known_faction = known_item[6]
                known_effect = known_item[7]

                for clearx in range(popup_width):  # draw a shadow behind the popup
                    for cleary in range(popup_height):
                        libtcod.console_set_back(herosale_popup, clearx, cleary, libtcod.Color(0, 0, 0),
                                                 libtcod.BKGND_SET)
                libtcod.console_blit(herosale_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1,
                                     popup_yoffset - 1, 0.75, 0.75)

                for clearx in range(popup_width):  # draw a box, clear text
                    for cleary in range(popup_height):
                        libtcod.console_set_back(herosale_popup, clearx, cleary, libtcod.Color(15, 35, 5),
                                                 libtcod.BKGND_SET)
                        libtcod.console_print_left(herosale_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

                # show the relevant, known item information
                libtcod.console_set_foreground_color(herosale_popup, libtcod.white)
                libtcod.console_print_left(herosale_popup, 7, 3, libtcod.BKGND_NONE, str(item_set_value))
                libtcod.console_print_left(herosale_popup, 7, 4, libtcod.BKGND_NONE,
                                           item_quality_display(item_known_quality))
                libtcod.console_print_left(herosale_popup, 7, 5, libtcod.BKGND_NONE,
                                           item_bonus_display(item_known_bonus))

                libtcod.console_print_left(herosale_popup, 7, 12, libtcod.BKGND_NONE, real_type)
                libtcod.console_print_left(herosale_popup, 7, 13, libtcod.BKGND_NONE, level_display(known_level))
                libtcod.console_print_left(herosale_popup, 7, 14, libtcod.BKGND_NONE, align_display(known_align))
                libtcod.console_print_left(herosale_popup, 7, 15, libtcod.BKGND_NONE, order_display(known_order))

                if known_name == real_name:
                    libtcod.console_print_left(herosale_popup, 7, 17, libtcod.BKGND_NONE, str(real_base_value))
                else:
                    libtcod.console_print_left(herosale_popup, 7, 17, libtcod.BKGND_NONE, 'Unknown')

                if known_faction == real_faction:
                    number_factions = len(known_faction)
                    for ppp in range(number_factions):
                        libtcod.console_print_left(herosale_popup, 7, 19 + ppp, libtcod.BKGND_NONE, known_faction[ppp])
                else:
                    libtcod.console_print_left(herosale_popup, 7, 19, libtcod.BKGND_NONE, 'Unknown')

                libtcod.console_set_foreground_color(herosale_popup,
                                                     libtcod.yellow)  # item display, consider changing colour based on item?
                libtcod.console_print_left(herosale_popup, 2, 2, libtcod.BKGND_NONE,
                                           player_item_display(item) + ' for sale.')
                libtcod.console_print_left(herosale_popup, 1, 1, libtcod.BKGND_NONE, sell_shop.name + ' offers:')
                libtcod.console_set_foreground_color(herosale_popup, libtcod.gray)  # titles
                libtcod.console_print_left(herosale_popup, 1, 3, libtcod.BKGND_NONE, 'value:')
                libtcod.console_print_left(herosale_popup, 1, 4, libtcod.BKGND_NONE, 'qulty:')
                libtcod.console_print_left(herosale_popup, 1, 5, libtcod.BKGND_NONE, 'bonus:')

                libtcod.console_print_left(herosale_popup, 1, 12, libtcod.BKGND_NONE, 'type :')
                libtcod.console_print_left(herosale_popup, 1, 13, libtcod.BKGND_NONE, 'level:')
                libtcod.console_print_left(herosale_popup, 1, 14, libtcod.BKGND_NONE, 'align:')
                libtcod.console_print_left(herosale_popup, 1, 15, libtcod.BKGND_NONE, 'order:')
                libtcod.console_print_left(herosale_popup, 1, 16, libtcod.BKGND_NONE, 'item base value:')
                libtcod.console_print_left(herosale_popup, 1, 18, libtcod.BKGND_NONE, 'associated factions:')

                libtcod.console_set_foreground_color(herosale_popup, libtcod.yellow)
                libtcod.console_print_left(herosale_popup, 2, 8, libtcod.BKGND_NONE, '(B)uy Item for listed price')
                libtcod.console_set_foreground_color(herosale_popup, libtcod.gray)
                libtcod.console_print_left(herosale_popup, 2, 10, libtcod.BKGND_NONE, 'Enter Key rejects.')
                libtcod.console_blit(herosale_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
                libtcod.console_flush()
                # watch for B?

                if key.c == 98:  # b?
                    price = item[5]
                    if buy_item(buy_shop, sell_shop, index):
                        hero_message(sell_shop.name + ' sold ' + real_type + ' to Player!', libtcod.light_green,
                                     libtcod.dark_green)
                        player.gain_experience(item_experience(item))
                        if real_type == 'scroll' or real_type == 'weapon':
                            sell_shop.activitylog['history'].append('I sold a ' + real_type + ' to ' + faction + '.')
                        else:
                            sell_shop.activitylog['history'].append('I sold some ' + real_type + ' to ' + faction + '.')
                        if libtcod.random_get_int(0, 0, 3) == 3:
                            sell_shop.activitylog['history'].append(pick_random_from_list(event_item_sold))
                        resolved = True
                        # opportunity for further flavour text
                        # log_purchase(player_item_display(item), price, sell_shop.name) #note already in buy_item function
                elif key.vk == libtcod.KEY_ENTER:
                    hero_message('You decline the offer from ' + sell_shop.name, libtcod.light_yellow,
                                 libtcod.dark_yellow)
                    player.gain_experience(1)
                    resolved = True
                else:
                    pass

                key = libtcod.console_check_for_keypress()
        # libtcod.console_clear(popup)
        # for clearx in range(INFO_BAR_WIDTH): #empty out previous text (if indeed it was there ...)
        #    for cleary in range(14, 23):
        #        libtcod.console_print_left(inf, clearx, cleary, libtcod.BKGND_NONE, ' ')
        libtcod.console_blit(herosale_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
        libtcod.console_flush()

    else:  # or not the player?
        sell_appraisal = appraise_value(item, faction, buy_shop.base_level)  # shop has a look at the item, checks value

        if item[5] <= sell_appraisal:
            if buy_item(buy_shop, sell_shop, index):
                # hero_message(sell_shop.name + ' sold ' + master_item_list[item[0]][9] + ' to ' + faction)
                # hero.gain_experience? Probably not from mercantile acts ...
                buy_shop.gain_experience(item_experience(item))  # the shop gets some experience ...
                if real_type == 'scroll' or real_type == 'weapon':
                    sell_shop.activitylog['history'].append('I sold a ' + real_type + ' to ' + faction + '.')
                else:
                    sell_shop.activitylog['history'].append('I sold some ' + real_type + ' to ' + faction + '.')
        else:
            pass


def auction_buy_item(buy_shop, sell_shop, index, buy_price):  # index is the item sitting in the sell_shop

    # same as normal buy function, but buy price set externally ... and messages disabled

    if buy_shop.wealth >= buy_price:
        buy_shop.wealth -= buy_price
        sell_shop.wealth += buy_price
        trade_item = sell_shop.inventory.pop(index)
        new_item_value = int(
            buy_price * 1.2)  # set the new value to match what it was bought for ... 1.2 value is the margin
        trade_item[5] = new_item_value  # apply the markup
        buy_shop.inventory.append(trade_item)

        update_info_bar()
        return True

    else:
        update_info_bar()
        return False


def buy_item(buy_shop, sell_shop, index):  # index is the item sitting in the sell_shop

    # move items from a faction to the player
    # x and y are the faction shop location

    buy_price = sell_shop.inventory[index][5]

    if buy_shop.wealth >= buy_price:
        buy_shop.wealth -= buy_price
        sell_shop.wealth += buy_price
        trade_item = sell_shop.inventory.pop(index)
        new_item_value = int(
            buy_price * 1.2)  # set the new value to match what it was bought for ... 1.2 value is the margin
        trade_item[5] = new_item_value  # apply the markup
        buy_shop.inventory.append(trade_item)

        if player == buy_shop:  # if the player is doing stuff, lets tell everyone
            message('Item bought', libtcod.light_yellow, libtcod.dark_yellow)
            if sell_shop.owner_name:  # grrrrrr. Can't do it straight up ...
                log_purchase(player_item_display(trade_item), buy_price, sell_shop.owner_name)
            elif sell_shop.name:
                log_purchase(player_item_display(trade_item), buy_price, sell_shop.name)
            else:
                log_purchase(player_item_display(trade_item), buy_price, 'Unknown')

        update_info_bar()
        return True

    else:
        if player == buy_shop:
            message('You cant afford the item', libtcod.light_red, libtcod.dark_red)
        else:
            pass
        update_info_bar()
        return False


def auction_house_welcome(x, y):
    ##global pop_up

    ##pop_up = 1

    wel = libtcod.console_new(VIEWPORT_WIDTH, WELCOME_SCREEN_HEIGHT)  # welcome screen before enter any shop

    for a in range(VIEWPORT_WIDTH):  # clear welcome screen, colour dark grey
        for b in range(WELCOME_SCREEN_HEIGHT):
            libtcod.console_set_back(wel, a, b, libtcod.Color(25, 25, 25), libtcod.BKGND_SET)
            libtcod.console_put_char(wel, a, b, ' ', libtcod.BKGND_NONE)

    # write info to welcome screen, intro to shop.

    libtcod.console_set_foreground_color(wel, libtcod.white)
    libtcod.console_print_left(wel, 1, 1, libtcod.BKGND_NONE, 'Welcome to ' + map[x][y].name + '.')
    libtcod.console_print_left(wel, 1, 2, libtcod.BKGND_NONE, 'I am ' + map[x][y].shop.owner_name + '.')
    # if auction in progress - all the time for now, no means of altering inventories with time just yet
    if auction_item:
        libtcod.console_print_left(wel, 1, 4, libtcod.BKGND_NONE, 'An auction is in progress, ')
    else:
        libtcod.console_print_left(wel, 1, 4, libtcod.BKGND_NONE, 'No auction today, ')

    libtcod.console_print_left(wel, 1, 5, libtcod.BKGND_NONE, 'do you want to come in?')
    libtcod.console_print_left(wel, 1, 6, libtcod.BKGND_NONE, 'y/n?')

    libtcod.console_blit(wel, 0, 0, VIEWPORT_WIDTH, WELCOME_SCREEN_HEIGHT, 0, 0, VIEWPORT_HEIGHT / 2, 1.0, 0.7)
    libtcod.console_flush()

    # key = libtcod.console_wait_for_keypress(True)

    test = yes_no_prompt()

    if test:
        auction_house_interface(x, y)
        ##pop_up = 0
    else:
        ##pop_up = 0
        pass


def faction_house_welcome(x, y):
    ##global pop_up

    ##pop_up = 1

    wel = libtcod.console_new(VIEWPORT_WIDTH, WELCOME_SCREEN_HEIGHT)  # welcome screen before enter any shop

    for a in range(VIEWPORT_WIDTH):  # clear welcome screen, colour dark grey
        for b in range(WELCOME_SCREEN_HEIGHT):
            libtcod.console_set_back(wel, a, b, libtcod.Color(25, 25, 25), libtcod.BKGND_SET)
            libtcod.console_put_char(wel, a, b, ' ', libtcod.BKGND_NONE)

    # write info to welcome screen, intro to shop.

    libtcod.console_set_foreground_color(wel, libtcod.white)

    if map[x][y].shop == player:
        libtcod.console_print_left(wel, 1, 1, libtcod.BKGND_NONE, 'This is your shop. Your helpful')
        libtcod.console_print_left(wel, 1, 2, libtcod.BKGND_NONE, 'assistant is standing at the door.')
    else:
        libtcod.console_print_left(wel, 1, 1, libtcod.BKGND_NONE, 'Welcome to ' + map[x][y].name + '.')
        libtcod.console_print_left(wel, 1, 2, libtcod.BKGND_NONE, 'I am ' + map[x][y].shop.owner_name + '.')

    # Lets decide whether we want to engage with the player
    if not player_relationship_test(x, y):
        libtcod.console_print_left(wel, 1, 4, libtcod.BKGND_NONE, 'Who are you again? Get lost.')
        libtcod.console_print_left(wel, 1, 5, libtcod.BKGND_NONE, 'Press a key')

        libtcod.console_blit(wel, 0, 0, VIEWPORT_WIDTH, WELCOME_SCREEN_HEIGHT, 0, 0, VIEWPORT_HEIGHT / 2, 1.0, 0.7)
        libtcod.console_flush()

        test = yes_no_prompt()

    elif map[x][y].shop == player:
        libtcod.console_print_left(wel, 1, 4, libtcod.BKGND_NONE, 'Hi Boss!')
        libtcod.console_print_left(wel, 1, 5, libtcod.BKGND_NONE, 'Are you coming in?')
        libtcod.console_print_left(wel, 1, 6, libtcod.BKGND_NONE, 'y/n?')

        libtcod.console_blit(wel, 0, 0, VIEWPORT_WIDTH, WELCOME_SCREEN_HEIGHT, 0, 0, VIEWPORT_HEIGHT / 2, 1.0, 0.7)
        libtcod.console_flush()

        # key = libtcod.console_wait_for_keypress(True)

        test = yes_no_prompt()

        if test:
            faction_house_interface(x, y)
            ##pop_up = 0
        else:
            ##pop_up = 0
            pass

    else:
        libtcod.console_print_left(wel, 1, 4, libtcod.BKGND_NONE, 'Nice to meet a fellow entrepeneur.')
        libtcod.console_print_left(wel, 1, 5, libtcod.BKGND_NONE, 'do you want to come in?')
        libtcod.console_print_left(wel, 1, 6, libtcod.BKGND_NONE, 'y/n?')

        libtcod.console_blit(wel, 0, 0, VIEWPORT_WIDTH, WELCOME_SCREEN_HEIGHT, 0, 0, VIEWPORT_HEIGHT / 2, 1.0, 0.7)
        libtcod.console_flush()

        # key = libtcod.console_wait_for_keypress(True)

        test = yes_no_prompt()

        if test:
            faction_house_interface(x, y)
            ##pop_up = 0
        else:
            ##pop_up = 0
            pass


def faction_house_interface(x, y):
    ##global pop_up
    global player

    ##pop_up = 1
    shp = libtcod.console_new(VIEWPORT_WIDTH - 2,
                              VIEWPORT_HEIGHT - 2)  # shop interface screen, nearly as big as normal town view console

    ##render_all() #display standard game state in background (for alpha channels benefit)

    print_status(x, y)

    for a in range(VIEWPORT_WIDTH - 2):  # clear screen, colour dark grey
        for b in range(VIEWPORT_HEIGHT - 2):
            libtcod.console_set_back(shp, a, b, libtcod.Color(25, 25, 25), libtcod.BKGND_SET)
            libtcod.console_put_char(shp, a, b, ' ', libtcod.BKGND_NONE)

    libtcod.console_set_foreground_color(shp, libtcod.white)

    libtcod.console_set_foreground_color(inf, libtcod.white)

    if map[x][y].shop == player:
        libtcod.console_print_left(shp, 1, 1, libtcod.BKGND_NONE, 'This is your shop.')
        libtcod.console_print_left(shp, 1, 2, libtcod.BKGND_NONE, 'You can smell success in the air.')
    else:
        libtcod.console_print_left(shp, 1, 1, libtcod.BKGND_NONE, 'Welcome to ' + map[x][y].name + '.')
        libtcod.console_print_left(shp, 3, 2, libtcod.BKGND_NONE, 'Owned by ' + map[x][y].shop.owner_name + '.')
        libtcod.console_print_left(shp, 5, 3, libtcod.BKGND_NONE, 'of the ' + map[x][y].faction + '.')

    libtcod.console_print_left(shp, 1, 5, libtcod.BKGND_NONE, 'We have the following in stock:')

    # print the item name according to the player of ten items at a time

    stock_level = len(map[x][y].shop.inventory)

    if not stock_level:
        libtcod.console_print_left(shp, 1, 8, libtcod.BKGND_NONE, 'Currently nothing')
        libtcod.console_print_left(shp, 1, 10, libtcod.BKGND_NONE, '(press enter to exit)')

        print_status(x, y)

        libtcod.console_blit(shp, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
        libtcod.console_flush()

        key = libtcod.console_wait_for_keypress(True)

    else:
        no_items = stock_level  # set the number of items to the same as the stock level
        if no_items > 10:
            no_items = 10
        # limit the no_items shown to ten

        # draw out all the items in the inventory, to the screen
        for z in range(no_items):
            item = map[x][y].shop.inventory[z]
            libtcod.console_set_foreground_color(shp, libtcod.dark_gray)
            libtcod.console_print_left(shp, 1, 8 + z, libtcod.BKGND_NONE, '----------------------------------')
            libtcod.console_set_foreground_color(shp, libtcod.white)
            libtcod.console_print_left(shp, 1, 8 + z, libtcod.BKGND_NONE, str(z) + " " + player_item_display(item))
            libtcod.console_set_foreground_color(shp, libtcod.dark_yellow)
            libtcod.console_print_left(shp, 35, 8 + z, libtcod.BKGND_NONE, str(item[5]))
        if stock_level > no_items:
            libtcod.console_set_foreground_color(shp, libtcod.white)
            libtcod.console_print_left(shp, 1, 18, libtcod.BKGND_NONE, '*more*')
        libtcod.console_set_foreground_color(shp, libtcod.white)
        libtcod.console_print_left(shp, 1, 21, libtcod.BKGND_NONE, '(z and x to scroll)')
        libtcod.console_print_left(shp, 1, 22, libtcod.BKGND_NONE, '(enter to leave)')
        libtcod.console_print_left(shp, 1, 23, libtcod.BKGND_NONE, '(number to interact)')
        # draws out all the inventory items and

        offset = 0  # set the offset for a scrollable screen
        libtcod.console_blit(shp, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
        libtcod.console_flush()

        key = libtcod.console_wait_for_keypress(True)
        while not key.vk == libtcod.KEY_ENTER:
            current_offset = offset

            # libtcod.console_clear(shp)
            for a in range(VIEWPORT_WIDTH - 2):  # clear screen, colour dark grey, every cycle
                for b in range(VIEWPORT_HEIGHT - 2):
                    libtcod.console_set_back(shp, a, b, libtcod.Color(25, 25, 25), libtcod.BKGND_SET)
                    libtcod.console_put_char(shp, a, b, ' ', libtcod.BKGND_NONE)

            if key.c == 122:  # z
                offset -= 1
            elif key.c == 120:  # x
                offset += 1
            elif key.vk == libtcod.KEY_1 or key.vk == libtcod.KEY_KP1:
                if stock_level > 0:
                    item_interact(x, y, 1 + offset)
                    # I want to interact with the item in the '1' slot in the interface
            elif key.vk == libtcod.KEY_2 or key.vk == libtcod.KEY_KP2:
                if stock_level > 1:
                    item_interact(x, y, 2 + offset)
            elif key.vk == libtcod.KEY_3 or key.vk == libtcod.KEY_KP3:
                if stock_level > 2:
                    item_interact(x, y, 3 + offset)
            elif key.vk == libtcod.KEY_4 or key.vk == libtcod.KEY_KP4:
                if stock_level > 3:
                    item_interact(x, y, 4 + offset)
            elif key.vk == libtcod.KEY_5 or key.vk == libtcod.KEY_KP5:
                if stock_level > 4:
                    item_interact(x, y, 5 + offset)
            elif key.vk == libtcod.KEY_6 or key.vk == libtcod.KEY_KP6:
                if stock_level > 5:
                    item_interact(x, y, 6 + offset)
            elif key.vk == libtcod.KEY_7 or key.vk == libtcod.KEY_KP7:
                if stock_level > 6:
                    item_interact(x, y, 7 + offset)
            elif key.vk == libtcod.KEY_8 or key.vk == libtcod.KEY_KP8:
                if stock_level > 7:
                    item_interact(x, y, 8 + offset)
            elif key.vk == libtcod.KEY_9 or key.vk == libtcod.KEY_KP9:
                if stock_level > 8:
                    item_interact(x, y, 9 + offset)
            elif key.vk == libtcod.KEY_0 or key.vk == libtcod.KEY_KP0:
                item_interact(x, y, offset)
            else:
                pass

            stock_level = len(map[x][y].shop.inventory)
            libtcod.console_set_foreground_color(shp, libtcod.white)

            if map[x][y].shop == player:
                libtcod.console_print_left(shp, 1, 1, libtcod.BKGND_NONE, 'This is your shop.')
                libtcod.console_print_left(shp, 1, 2, libtcod.BKGND_NONE, 'You can smell success in the air.')
            else:
                libtcod.console_print_left(shp, 1, 1, libtcod.BKGND_NONE, 'Welcome to ' + map[x][y].name + '.')
                libtcod.console_print_left(shp, 3, 2, libtcod.BKGND_NONE, 'Owned by ' + map[x][y].shop.owner_name + '.')
                libtcod.console_print_left(shp, 5, 3, libtcod.BKGND_NONE, 'of the ' + map[x][y].faction + '.')

            libtcod.console_print_left(shp, 1, 5, libtcod.BKGND_NONE, 'We have the following in stock:')

            if not stock_level:
                libtcod.console_print_left(shp, 1, 8, libtcod.BKGND_NONE, 'Currently nothing')
                libtcod.console_print_left(shp, 1, 10, libtcod.BKGND_NONE, '(press enter to exit)')

                update_info_bar()

                print_status(x, y)

                libtcod.console_blit(shp, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
                libtcod.console_flush()

                key = libtcod.console_wait_for_keypress(True)

            else:
                no_items = stock_level  # set the number of items to the same as the stock level
                if no_items > 10:
                    no_items = 10
                # limit the no_items shown to ten

                if offset < 0:
                    offset = 0
                if offset + no_items > stock_level:
                    offset -= 1

                for z in range(offset, no_items + offset):
                    item = map[x][y].shop.inventory[z]
                    libtcod.console_set_foreground_color(shp, libtcod.dark_gray)
                    libtcod.console_print_left(shp, 1, 8 + z - offset, libtcod.BKGND_NONE,
                                               '----------------------------------')
                    libtcod.console_set_foreground_color(shp, libtcod.white)
                    libtcod.console_print_left(shp, 1, 8 + z - offset, libtcod.BKGND_NONE,
                                               str(z - offset) + " " + player_item_display(item))
                    libtcod.console_set_foreground_color(shp, libtcod.dark_yellow)
                    libtcod.console_print_left(shp, 35, 8 + z - offset, libtcod.BKGND_NONE, str(item[5]))

                libtcod.console_set_foreground_color(shp, libtcod.white)

                if stock_level > no_items:
                    if offset + no_items < stock_level:
                        libtcod.console_print_left(shp, 1, 18, libtcod.BKGND_NONE, '*more*')

                if offset > 0:
                    libtcod.console_print_left(shp, 1, 7, libtcod.BKGND_NONE, '*more*')

                update_info_bar()

                print_status(x, y)

                libtcod.console_print_left(shp, 1, 21, libtcod.BKGND_NONE, '(z and x to scroll)')
                libtcod.console_print_left(shp, 1, 22, libtcod.BKGND_NONE, '(enter to leave)')
                libtcod.console_print_left(shp, 1, 23, libtcod.BKGND_NONE, '(number to interact)')

                # update, including scrolling
                libtcod.console_blit(shp, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
                libtcod.console_flush()
                # wait for key to exit
                key = libtcod.console_wait_for_keypress(True)


def enter_name():
    global player_name

    popup_width = 30
    popup_height = 4

    popup_xoffset = 20
    popup_yoffset = 20

    enter_name = libtcod.console_new(popup_width, popup_height)

    libtcod.console_set_foreground_color(enter_name, libtcod.light_red)
    libtcod.console_print_left(enter_name, 1, 1, libtcod.BKGND_NONE, 'ENTER YOUR NAME:')

    for m in range(popup_width):
        for n in range(popup_height):
            if m == 0 or m == popup_width - 1 or n == 0 or n == popup_height - 1:
                libtcod.console_set_char(enter_name, m, n, '#')  # print new character at appropriate position on screen
                libtcod.console_set_fore(enter_name, m, n, libtcod.dark_red)  # make it white or something

    player_name = 'Player'

    key = libtcod.console_check_for_keypress()
    letter = 0
    while key.vk != libtcod.KEY_ENTER:
        libtcod.console_set_foreground_color(enter_name, libtcod.white)

        x = len(player_name)

        if key.vk == libtcod.KEY_BACKSPACE:
            if x > 0:
                player_name = player_name[:-1]
            else:
                player_name = ''
        elif key.c:
            try:
                player_name += letter  # add to the string
            except:
                pass

        libtcod.console_print_left(enter_name, 1, 2, libtcod.BKGND_NONE, player_name + ' ')

        libtcod.console_blit(enter_name, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
        libtcod.console_flush()

        key = libtcod.console_wait_for_keypress(True)
        letter = chr(key.c)

    if player_name == '':
        player_name = 'Player'


def show_heroes(heroes_present):
    length = len(heroes_present)

    if length > 7:
        length = 7
        libtcod.console_set_foreground_color(inf, libtcod.light_blue)
        libtcod.console_print_left(inf, 16, 29, libtcod.BKGND_NONE, ' ... Plus others! ...')

    for zzz in range(length):
        libtcod.console_set_foreground_color(inf, libtcod.light_blue)
        libtcod.console_print_left(inf, 16, 22 + zzz, libtcod.BKGND_NONE,
                                   heroes_present[zzz].name + ', ' + heroes_present[zzz].faction)

    libtcod.console_set_foreground_color(inf, libtcod.dark_gray)
    libtcod.console_print_left(inf, 16, 21, libtcod.BKGND_NONE, 'Heroes present:')


def show_monsters(monsters):
    length = len(monsters)

    if length > 3:
        length = 3
        libtcod.console_set_foreground_color(inf, libtcod.light_red)
        libtcod.console_print_left(inf, 2, 29, libtcod.BKGND_NONE, ' ... Plus others! ...')

    for zzz in range(length):
        libtcod.console_set_foreground_color(inf, libtcod.light_red)
        libtcod.console_print_left(inf, 2, 26 + zzz, libtcod.BKGND_NONE, monsters[zzz].name)

    libtcod.console_set_foreground_color(inf, libtcod.red)
    libtcod.console_print_left(inf, 2, 25, libtcod.BKGND_NONE, 'Monsters here:')


def print_status(x, y):
    heroes_present = []

    for hero in town_heroes:
        if (hero.x, hero.y) == (x, y):
            heroes_present.append(hero)

    show_heroes(heroes_present)

    if not map[x][y].shop == player:
        xp_float = float(map[x][y].shop.reputation.xp)
        nextlevel = float(map[x][y].shop.base_level * store_base_level_exp)

        rep_bar = int((xp_float / nextlevel) * 6)  # number from 1 to 6

        libtcod.console_set_foreground_color(inf, libtcod.white)
        libtcod.console_print_left(inf, 7, 23, libtcod.BKGND_NONE, str(map[x][y].shop.wealth))
        libtcod.console_print_left(inf, 7, 24, libtcod.BKGND_NONE, str(map[x][y].shop.base_level))

        libtcod.console_set_foreground_color(inf, libtcod.gray)
        libtcod.console_print_left(inf, 7, 25, libtcod.BKGND_NONE, '------')
        libtcod.console_set_foreground_color(inf, libtcod.light_red)
        for p in range(rep_bar):
            libtcod.console_print_left(inf, 7 + p, 25, libtcod.BKGND_NONE, '#')

        libtcod.console_set_foreground_color(inf, libtcod.gray)
        libtcod.console_print_left(inf, 1, 22, libtcod.BKGND_NONE, '-THEIR STATUS-')
        libtcod.console_print_left(inf, 3, 23, libtcod.BKGND_NONE, '$$$:')
        libtcod.console_print_left(inf, 3, 24, libtcod.BKGND_NONE, 'LVL:')
        libtcod.console_print_left(inf, 3, 25, libtcod.BKGND_NONE, 'REP:')

    libtcod.console_blit(inf, 0, 0, INFO_BAR_WIDTH, VIEWPORT_HEIGHT - 10, 0, VIEWPORT_WIDTH, 0)
    libtcod.console_flush()


def auction_house_interface(x, y):
    ##global pop_up
    global player
    global bidders, player_bid, bid_placed, auction_item

    ##pop_up = 1
    shp = libtcod.console_new(VIEWPORT_WIDTH - 2,
                              VIEWPORT_HEIGHT - 2)  # shop interface screen, nearly as big as normal town view console

    ##render_all() #display standard game state in background (for alpha channels benefit)

    print_status(x, y)  # show the status of the auction house

    for a in range(VIEWPORT_WIDTH - 2):  # clear screen, colour dark grey
        for b in range(VIEWPORT_HEIGHT - 2):
            libtcod.console_set_back(shp, a, b, libtcod.Color(25, 25, 25), libtcod.BKGND_SET)
            libtcod.console_put_char(shp, a, b, ' ', libtcod.BKGND_NONE)

    libtcod.console_set_foreground_color(shp, libtcod.white)
    libtcod.console_set_foreground_color(inf, libtcod.white)
    libtcod.console_print_left(shp, 1, 1, libtcod.BKGND_NONE, 'Welcome to ' + map[x][y].name + '.')
    libtcod.console_print_left(shp, 3, 2, libtcod.BKGND_NONE, 'Owned by ' + map[x][y].shop.owner_name + '.')
    libtcod.console_print_left(shp, 5, 3, libtcod.BKGND_NONE, 'of the ' + map[x][y].faction + '.')

    if not auction_item:
        libtcod.console_print_left(shp, 1, 5, libtcod.BKGND_NONE, 'Nothing for sale.')

    else:
        libtcod.console_set_foreground_color(shp, libtcod.white)
        libtcod.console_print_left(shp, 1, 5, libtcod.BKGND_NONE, 'Currently under the hammer:')

        # map[x][y].shop.inventory.append(create_item(1, 4, 'all')) #add a random item to auction house inventory
        # message('item created')
        item = auction_item  # define item as the first item
        item_index = item[0]
        # set the name of the item to be as the players knowledge
        libtcod.console_set_foreground_color(shp, libtcod.yellow)
        libtcod.console_print_left(shp, 1, 6, libtcod.BKGND_NONE, player_item_display(item))
        libtcod.console_set_foreground_color(shp, libtcod.white)
        # message('item knowledge displayed')

        item_set_value = item[5]
        item_known_quality = item[1][1]
        item_known_bonus = item[2][1]

        known_item = player_item_knowledge_list[item[0]]

        known_level = known_item[3]
        known_align = known_item[4]
        known_order = known_item[5]
        known_name = known_item[0]
        known_faction = known_item[6]

        real_item = master_item_list[item[0]]
        real_name = real_item[1]
        real_type = real_item[9]
        real_base_value = real_item[2]
        real_faction = real_item[6]

        # show the relevant item information
        libtcod.console_set_foreground_color(shp, libtcod.white)
        # libtcod.console_print_left(shp, 7, 8, libtcod.BKGND_NONE, str(item_set_value)) not relevant for something to bid on
        libtcod.console_print_left(shp, 7, 8, libtcod.BKGND_NONE, item_quality_display(item_known_quality))
        libtcod.console_print_left(shp, 7, 9, libtcod.BKGND_NONE, item_bonus_display(item_known_bonus))

        libtcod.console_print_left(shp, 7, 10, libtcod.BKGND_NONE, real_type)
        libtcod.console_print_left(shp, 7, 11, libtcod.BKGND_NONE, level_display(known_level))
        libtcod.console_print_left(shp, 7, 12, libtcod.BKGND_NONE, align_display(known_align))
        libtcod.console_print_left(shp, 7, 13, libtcod.BKGND_NONE, order_display(known_order))

        if known_name == real_name:
            libtcod.console_print_left(shp, 7, 15, libtcod.BKGND_NONE, str(real_base_value))
        else:
            libtcod.console_print_left(shp, 7, 15, libtcod.BKGND_NONE, 'Unknown')

        if known_faction == real_faction:
            number_factions = len(known_faction)
            for ppp in range(number_factions):
                libtcod.console_print_left(shp, 7, 17 + ppp, libtcod.BKGND_NONE, known_faction[ppp])
        else:
            libtcod.console_print_left(shp, 7, 17, libtcod.BKGND_NONE, 'Unknown')

        libtcod.console_set_foreground_color(shp, libtcod.gray)  # titles
        # libtcod.console_print_left(shp, 1, 8, libtcod.BKGND_NONE, 'value:') not relevant for something to bid on
        libtcod.console_print_left(shp, 1, 8, libtcod.BKGND_NONE, 'qulty:')
        libtcod.console_print_left(shp, 1, 9, libtcod.BKGND_NONE, 'bonus:')

        libtcod.console_print_left(shp, 1, 10, libtcod.BKGND_NONE, 'type :')
        libtcod.console_print_left(shp, 1, 11, libtcod.BKGND_NONE, 'level:')
        libtcod.console_print_left(shp, 1, 12, libtcod.BKGND_NONE, 'align:')
        libtcod.console_print_left(shp, 1, 13, libtcod.BKGND_NONE, 'order:')
        libtcod.console_print_left(shp, 1, 14, libtcod.BKGND_NONE, 'item base value:')
        libtcod.console_print_left(shp, 1, 16, libtcod.BKGND_NONE, 'associated factions:')

    reserve_price = 1
    # reserve value?
    libtcod.console_set_foreground_color(shp, libtcod.gray)
    libtcod.console_print_left(shp, 1, 32, libtcod.BKGND_NONE, 'Please make a choice:')
    libtcod.console_set_foreground_color(shp, libtcod.white)
    if bid_placed:
        libtcod.console_set_foreground_color(shp, libtcod.yellow)
        libtcod.console_print_left(shp, 1, 33, libtcod.BKGND_NONE, 'bid of $' + str(player_bid) + ' placed')
        libtcod.console_set_foreground_color(shp, libtcod.white)
    else:
        libtcod.console_print_left(shp, 1, 33, libtcod.BKGND_NONE, '(p)lace bid')
    libtcod.console_print_left(shp, 1, 34, libtcod.BKGND_NONE, 'check (o)ther bidders')
    libtcod.console_print_left(shp, 1, 35, libtcod.BKGND_NONE, 'check out (f)uture auctions ...')
    libtcod.console_print_left(shp, 1, 36, libtcod.BKGND_NONE, '(Enter) key to leave ' + map[x][y].name)

    libtcod.console_blit(shp, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
    libtcod.console_flush()

    key = libtcod.console_wait_for_keypress(True)

    while not key.vk == libtcod.KEY_ENTER:

        # message('decision on bidding made')
        if key.c == 112:  # p
            if bid_placed:
                pass
            else:
                if auction_item:
                    auction_player_bid(item, reserve_price)
                    # function to place a bid
                    update_info_bar()  # feed back new bid to info bar

                else:
                    message('Cannot bid - no item at auction', libtcod.light_red, libtcod.dark_red)

        elif key.c == 111:  # o, for other bidders
            show_bidders(x, y)

        elif key.c == 102:  # f, for future lots
            show_future_auctions(x, y)

        if bid_placed:
            libtcod.console_set_foreground_color(shp, libtcod.yellow)
            libtcod.console_print_left(shp, 1, 33, libtcod.BKGND_NONE, 'bid of $' + str(player_bid) + ' placed')
            libtcod.console_set_foreground_color(shp, libtcod.white)
        else:
            libtcod.console_print_left(shp, 1, 33, libtcod.BKGND_NONE, '(p)lace bid')

        libtcod.console_blit(shp, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)


def auction_player_bid(item, reserve_price):
    global player_bid, bid_placed

    popup_width = 26
    popup_height = 12

    popup_xoffset = 4
    popup_yoffset = 24

    bid_amount = reserve_price
    bid_popup = libtcod.console_new(popup_width, popup_height)

    for clearx in range(popup_width):  # draw a shadow behind the popup
        for cleary in range(popup_height):
            libtcod.console_set_back(bid_popup, clearx, cleary, libtcod.Color(0, 0, 0), libtcod.BKGND_SET)
    libtcod.console_blit(bid_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset - 1, popup_yoffset - 1, 0.5, 0.5)

    for clearx in range(popup_width):  # draw a box, clear text
        for cleary in range(popup_height):
            libtcod.console_set_back(bid_popup, clearx, cleary, libtcod.Color(45, 45, 10), libtcod.BKGND_SET)
            libtcod.console_print_left(bid_popup, clearx, cleary, libtcod.BKGND_NONE, ' ')

    libtcod.console_print_left(bid_popup, 1, 1, libtcod.BKGND_NONE, 'This is a sealed bid.')
    libtcod.console_print_left(bid_popup, 1, 2, libtcod.BKGND_NONE, 'How much do you offer?')

    libtcod.console_print_left(bid_popup, 5, 4, libtcod.BKGND_NONE, str(bid_amount) + '    ')
    libtcod.console_print_left(bid_popup, 1, 6, libtcod.BKGND_NONE, 'z/x -/+ 1, a/s -/+ 5')
    libtcod.console_print_left(bid_popup, 1, 7, libtcod.BKGND_NONE, 'ENTER to submit bid')

    libtcod.console_blit(bid_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset)
    libtcod.console_flush()

    key = libtcod.console_wait_for_keypress(True)

    while not key.vk == libtcod.KEY_ENTER:
        if key.c == 122:  # z
            bid_amount -= 1
        elif key.c == 120:  # x
            bid_amount += 1
        elif key.c == 97:  # a
            bid_amount -= 5
        elif key.c == 115:  # s
            bid_amount += 5

        if bid_amount < 1:
            bid_amount = 1

        libtcod.console_print_left(bid_popup, 1, 1, libtcod.BKGND_NONE, 'This is a sealed bid.')
        libtcod.console_print_left(bid_popup, 1, 2, libtcod.BKGND_NONE, 'How much do you offer?')
        libtcod.console_print_left(bid_popup, 5, 4, libtcod.BKGND_NONE, '                      ')
        libtcod.console_print_left(bid_popup, 5, 4, libtcod.BKGND_NONE, str(bid_amount) + '    ')
        libtcod.console_print_left(bid_popup, 1, 6, libtcod.BKGND_NONE, 'z/x -/+ 1, a/s -/+ 5')
        libtcod.console_print_left(bid_popup, 1, 7, libtcod.BKGND_NONE, 'ENTER to submit bid')
        # print result of change in bid
        libtcod.console_blit(bid_popup, 0, 0, popup_width, popup_height, 0, popup_xoffset, popup_yoffset, 1)
        libtcod.console_flush()
        # wait for key to modify bid, or submit
        key = libtcod.console_wait_for_keypress(True)

    player_bid = bid_amount
    bid_placed = 1  # set variables
    message('Bid of $' + str(player_bid) + ' placed on ' + player_item_display(item), libtcod.light_yellow,
            libtcod.dark_yellow)
    # display the player bid in the message screen


def show_future_auctions(x, y):
    lot_console = libtcod.console_new(VIEWPORT_WIDTH - 2,
                                      VIEWPORT_HEIGHT - 2)  # new console for showing the future lots
    inventory = map[x][y].shop.inventory

    ##render_all() #display standard game state in background (for alpha channels benefit)

    print_status(x, y)  # show the status of the auction house

    for a in range(VIEWPORT_WIDTH - 2):  # clear screen, colour dark grey
        for b in range(VIEWPORT_HEIGHT - 2):
            libtcod.console_set_back(lot_console, a, b, libtcod.Color(10, 10, 10), libtcod.BKGND_SET)
            libtcod.console_put_char(lot_console, a, b, ' ', libtcod.BKGND_NONE)

    libtcod.console_set_foreground_color(lot_console, libtcod.white)

    libtcod.console_print_left(lot_console, 1, 1, libtcod.BKGND_NONE, 'Welcome to ' + map[x][y].name + '.')
    libtcod.console_print_left(lot_console, 3, 2, libtcod.BKGND_NONE, 'Owned by ' + map[x][y].shop.owner_name + '.')
    libtcod.console_print_left(lot_console, 5, 3, libtcod.BKGND_NONE, 'of the ' + map[x][y].faction + '.')

    if len(inventory):
        # libtcod.console_set_foreground_color(lot_console, libtcod.yellow)
        # libtcod.console_print_left(lot_console, 1, 5, libtcod.BKGND_NONE, player_item_display(auction_item))
        libtcod.console_set_foreground_color(lot_console, libtcod.white)
        libtcod.console_print_left(lot_console, 1, 6, libtcod.BKGND_NONE, 'Upcoming auctions (take place daily!)')
    else:
        libtcod.console_print_left(lot_console, 1, 5, libtcod.BKGND_NONE,
                                   'No upcoming auctions. Waiting for some people to die and bequeath.')
        libtcod.console_print_left(lot_console, 1, 6, libtcod.BKGND_NONE, 'Have a nice day, sir.')

    upcoming = len(inventory)

    if not upcoming:
        libtcod.console_print_left(lot_console, 1, 8, libtcod.BKGND_NONE, 'Currently no-one')
        libtcod.console_print_left(lot_console, 1, 10, libtcod.BKGND_NONE, '(press a key to exit)')
        libtcod.console_blit(lot_console, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)

    else:
        no_lots = upcoming  # set the number of items to the same as the stock level
        if no_lots > 10:
            no_lots = 10
        # limit the no_items shown to ten

        # draw out all the items in the inventory, to the screen
        for z in range(no_lots):
            libtcod.console_print_left(lot_console, 1, 8 + z, libtcod.BKGND_NONE,
                                       str(z) + ' ' + player_item_display(inventory[z]))
        if upcoming > no_lots:
            libtcod.console_print_left(lot_console, 1, 18, libtcod.BKGND_NONE, '*more*')
        libtcod.console_print_left(lot_console, 1, 21, libtcod.BKGND_NONE, '(z and x to scroll)')
        libtcod.console_print_left(lot_console, 1, 22, libtcod.BKGND_NONE, '(enter to go back)')
        # libtcod.console_print_left(lot_console, 1, 23, libtcod.BKGND_NONE, '(number to interact)')
        # draws out all the inventory items and

        offset = 0  # set the offset for a scrollable screen
        libtcod.console_blit(lot_console, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
        libtcod.console_flush()

        key = libtcod.console_wait_for_keypress(True)

        while not key.vk == libtcod.KEY_ENTER:
            current_offset = offset

            # libtcod.console_clear(lot_console)
            for a in range(VIEWPORT_WIDTH - 2):  # clear screen, colour dark grey, every cycle
                for b in range(VIEWPORT_HEIGHT - 2):
                    libtcod.console_set_back(lot_console, a, b, libtcod.Color(10, 10, 10), libtcod.BKGND_SET)
                    libtcod.console_put_char(lot_console, a, b, ' ', libtcod.BKGND_NONE)

            if key.c == 122:  # z
                offset -= 1
            elif key.c == 120:  # x
                offset += 1
            elif key.vk == libtcod.KEY_1 or key.vk == libtcod.KEY_KP1:
                pass
                # I want to interact with the item in the '1' slot in the interface
            elif key.vk == libtcod.KEY_2 or key.vk == libtcod.KEY_KP2:
                pass
            elif key.vk == libtcod.KEY_3 or key.vk == libtcod.KEY_KP3:
                pass
            elif key.vk == libtcod.KEY_4 or key.vk == libtcod.KEY_KP4:
                pass
            elif key.vk == libtcod.KEY_5 or key.vk == libtcod.KEY_KP5:
                pass
            elif key.vk == libtcod.KEY_6 or key.vk == libtcod.KEY_KP6:
                pass
            elif key.vk == libtcod.KEY_7 or key.vk == libtcod.KEY_KP7:
                pass
            elif key.vk == libtcod.KEY_8 or key.vk == libtcod.KEY_KP8:
                pass
            elif key.vk == libtcod.KEY_9 or key.vk == libtcod.KEY_KP9:
                pass
            elif key.vk == libtcod.KEY_0 or key.vk == libtcod.KEY_KP0:
                pass
                ##else:
                ##   pass

            if offset < 0:
                offset = 0
            if offset + no_lots > upcoming:
                offset = current_offset

            libtcod.console_print_left(lot_console, 1, 1, libtcod.BKGND_NONE, 'Welcome to ' + map[x][y].name + '.')
            libtcod.console_print_left(lot_console, 3, 2, libtcod.BKGND_NONE,
                                       'Owned by ' + map[x][y].shop.owner_name + '.')
            libtcod.console_print_left(lot_console, 5, 3, libtcod.BKGND_NONE, 'of the ' + map[x][y].faction + '.')

            # libtcod.console_set_foreground_color(lot_console, libtcod.yellow)
            # libtcod.console_print_left(lot_console, 1, 5, libtcod.BKGND_NONE, player_item_display(auction_item))
            libtcod.console_set_foreground_color(lot_console, libtcod.white)
            libtcod.console_print_left(lot_console, 1, 6, libtcod.BKGND_NONE, 'Upcoming auctions (take place daily!)')

            for z in range(offset, no_lots + offset):
                libtcod.console_print_left(lot_console, 1, 8 + z - offset, libtcod.BKGND_NONE,
                                           str(z) + ' ' + player_item_display(inventory[z]))

            if upcoming > no_lots:
                if offset + no_lots < upcoming:
                    libtcod.console_print_left(lot_console, 1, 18, libtcod.BKGND_NONE, '*more*')

            if offset > 0:
                libtcod.console_print_left(lot_console, 1, 7, libtcod.BKGND_NONE, '*more*')

            libtcod.console_print_left(lot_console, 1, 21, libtcod.BKGND_NONE, '(z and x to scroll)')
            libtcod.console_print_left(lot_console, 1, 22, libtcod.BKGND_NONE, '(enter to go back)')
            # libtcod.console_print_left(bid_console, 1, 23, libtcod.BKGND_NONE, '(number to interact)')

            # update, including scrolling
            libtcod.console_blit(lot_console, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
            libtcod.console_flush()

            key = libtcod.console_wait_for_keypress(True)


def show_bidders(x, y):
    bid_console = libtcod.console_new(VIEWPORT_WIDTH - 2,
                                      VIEWPORT_HEIGHT - 2)  # shop interface screen, nearly as big as normal town view console

    ##render_all() #display standard game state in background (for alpha channels benefit)

    print_status(x, y)  # show the status of the auction house

    for a in range(VIEWPORT_WIDTH - 2):  # clear screen, colour dark grey
        for b in range(VIEWPORT_HEIGHT - 2):
            libtcod.console_set_back(bid_console, a, b, libtcod.Color(10, 10, 10), libtcod.BKGND_SET)
            libtcod.console_put_char(bid_console, a, b, ' ', libtcod.BKGND_NONE)

    libtcod.console_set_foreground_color(bid_console, libtcod.white)

    libtcod.console_print_left(bid_console, 1, 1, libtcod.BKGND_NONE, 'Welcome to ' + map[x][y].name + '.')
    libtcod.console_print_left(bid_console, 3, 2, libtcod.BKGND_NONE, 'Owned by ' + map[x][y].shop.owner_name + '.')
    libtcod.console_print_left(bid_console, 5, 3, libtcod.BKGND_NONE, 'of the ' + map[x][y].faction + '.')

    if auction_item:
        libtcod.console_set_foreground_color(bid_console, libtcod.yellow)
        libtcod.console_print_left(bid_console, 1, 5, libtcod.BKGND_NONE, player_item_display(auction_item))
        libtcod.console_set_foreground_color(bid_console, libtcod.white)
        libtcod.console_print_left(bid_console, 1, 6, libtcod.BKGND_NONE, 'Possible interest shown by:')
    else:
        libtcod.console_print_left(bid_console, 1, 5, libtcod.BKGND_NONE, 'No auction today.')
        libtcod.console_print_left(bid_console, 1, 6, libtcod.BKGND_NONE, 'Have a nice day, sir.')

    interest_level = len(bidders)

    if not interest_level:
        libtcod.console_print_left(bid_console, 1, 8, libtcod.BKGND_NONE, 'Currently no-one')
        libtcod.console_print_left(bid_console, 1, 10, libtcod.BKGND_NONE, '(press a key to exit)')
        libtcod.console_blit(bid_console, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)

    else:
        no_bidders = interest_level  # set the number of items to the same as the stock level
        if no_bidders > 10:
            no_bidders = 10
        # limit the no_items shown to ten

        # draw out all the items in the inventory, to the screen
        for z in range(no_bidders):
            libtcod.console_print_left(bid_console, 1, 8 + z, libtcod.BKGND_NONE,
                                       str(z) + ' A visit from ' + bidders[z][0])
        if interest_level > no_bidders:
            libtcod.console_print_left(bid_console, 1, 18, libtcod.BKGND_NONE, '*more*')
        libtcod.console_print_left(bid_console, 1, 21, libtcod.BKGND_NONE, '(z and x to scroll)')
        libtcod.console_print_left(bid_console, 1, 22, libtcod.BKGND_NONE, '(enter to go back)')
        # libtcod.console_print_left(bid_console, 1, 23, libtcod.BKGND_NONE, '(number to interact)')
        # draws out all the inventory items and

        offset = 0  # set the offset for a scrollable screen
        libtcod.console_blit(bid_console, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
        libtcod.console_flush()

        key = libtcod.console_wait_for_keypress(True)

        while not key.vk == libtcod.KEY_ENTER:
            current_offset = offset

            # libtcod.console_clear(bid_console)
            for a in range(VIEWPORT_WIDTH - 2):  # clear screen, colour dark grey, every cycle
                for b in range(VIEWPORT_HEIGHT - 2):
                    libtcod.console_set_back(bid_console, a, b, libtcod.Color(10, 10, 10), libtcod.BKGND_SET)
                    libtcod.console_put_char(bid_console, a, b, ' ', libtcod.BKGND_NONE)

            if key.c == 122:  # z
                offset -= 1
            elif key.c == 120:  # x
                offset += 1
            elif key.vk == libtcod.KEY_1 or key.vk == libtcod.KEY_KP1:
                pass
                # I want to interact with the item in the '1' slot in the interface
            elif key.vk == libtcod.KEY_2 or key.vk == libtcod.KEY_KP2:
                pass
            elif key.vk == libtcod.KEY_3 or key.vk == libtcod.KEY_KP3:
                pass
            elif key.vk == libtcod.KEY_4 or key.vk == libtcod.KEY_KP4:
                pass
            elif key.vk == libtcod.KEY_5 or key.vk == libtcod.KEY_KP5:
                pass
            elif key.vk == libtcod.KEY_6 or key.vk == libtcod.KEY_KP6:
                pass
            elif key.vk == libtcod.KEY_7 or key.vk == libtcod.KEY_KP7:
                pass
            elif key.vk == libtcod.KEY_8 or key.vk == libtcod.KEY_KP8:
                pass
            elif key.vk == libtcod.KEY_9 or key.vk == libtcod.KEY_KP9:
                pass
            elif key.vk == libtcod.KEY_0 or key.vk == libtcod.KEY_KP0:
                pass
                ##else:
                ##   pass

            if offset < 0:
                offset = 0
            if offset + no_bidders > interest_level:
                offset = current_offset

            libtcod.console_print_left(bid_console, 1, 1, libtcod.BKGND_NONE, 'Welcome to ' + map[x][y].name + '.')
            libtcod.console_print_left(bid_console, 3, 2, libtcod.BKGND_NONE,
                                       'Owned by ' + map[x][y].shop.owner_name + '.')
            libtcod.console_print_left(bid_console, 5, 3, libtcod.BKGND_NONE, 'of the ' + map[x][y].faction + '.')

            libtcod.console_set_foreground_color(bid_console, libtcod.yellow)
            libtcod.console_print_left(bid_console, 1, 5, libtcod.BKGND_NONE, player_item_display(auction_item))
            libtcod.console_set_foreground_color(bid_console, libtcod.white)
            libtcod.console_print_left(bid_console, 1, 6, libtcod.BKGND_NONE, 'Possible interest shown by:')

            for z in range(offset, no_bidders + offset):
                libtcod.console_print_left(bid_console, 1, 8 + z - offset, libtcod.BKGND_NONE,
                                           str(z) + ' A visit from ' + bidders[z][0])

            if interest_level > no_bidders:
                if offset + no_bidders < interest_level:
                    libtcod.console_print_left(bid_console, 1, 18, libtcod.BKGND_NONE, '*more*')

            if offset > 0:
                libtcod.console_print_left(bid_console, 1, 7, libtcod.BKGND_NONE, '*more*')

            libtcod.console_print_left(bid_console, 1, 21, libtcod.BKGND_NONE, '(z and x to scroll)')
            libtcod.console_print_left(bid_console, 1, 22, libtcod.BKGND_NONE, '(enter to go back)')
            # libtcod.console_print_left(bid_console, 1, 23, libtcod.BKGND_NONE, '(number to interact)')

            # update, including scrolling
            libtcod.console_blit(bid_console, 0, 0, VIEWPORT_WIDTH - 2, VIEWPORT_HEIGHT - 2, 0, 1, 1, 1, 1.0)
            libtcod.console_flush()

            key = libtcod.console_wait_for_keypress(True)


def player_relationship_test(x, y):
    if map[x][y].shop.base_level <= player.base_level + 1:
        return True
    else:
        return False


def player_item_display(item):
    # return what the player sees as the name of an item. Also detects bonus / enchantment
    # This function is analgous to a cursory glance, what does our current knowledge allow us to find out about the item?
    item_index = item[0]

    item_real_bonus = item[2][0]
    item_known_bonus = item[2][1]

    item_real_quality = item[1][0]
    item_known_quality = item[1][1]

    item_type = master_item_list[item_index][9]

    # need to bring this out somewhere where we can change the values ... ?

    if item_type == 'armor':
        if player_specialisms['armor'] == 0:
            pass
        elif player_specialisms['armor'] == 1:
            if item_real_quality <= 1:
                item[1][1] = item_real_quality
        elif player_specialisms['armor'] == 2:
            if item_real_quality <= 2:
                item[1][1] = item_real_quality
        elif player_specialisms['armor'] == 3:
            if item_real_quality <= 3:
                item[1][1] = item_real_quality
            if item_real_bonus <= 1:
                item[2][1] = item_real_bonus
        elif player_specialisms['armor'] == 4:
            if item_real_quality <= 4:
                item[1][1] = item_real_quality
            if item_real_bonus <= 2:
                item[2][1] = item_real_bonus

    if item_type == 'scroll':
        if player_specialisms['scroll'] == 0:
            pass
        elif player_specialisms['scroll'] == 1:
            if item_real_quality <= 1:
                item[1][1] = item_real_quality
        elif player_specialisms['scroll'] == 2:
            if item_real_quality <= 2:
                item[1][1] = item_real_quality
        elif player_specialisms['scroll'] == 3:
            if item_real_quality <= 3:
                item[1][1] = item_real_quality
            if item_real_bonus <= 1:
                item[2][1] = item_real_bonus
        elif player_specialisms['scroll'] == 4:
            if item_real_quality <= 4:
                item[1][1] = item_real_quality
            if item_real_bonus <= 2:
                item[2][1] = item_real_bonus

    if item_type == 'weapon':
        if player_specialisms['weapon'] == 0:
            pass
        elif player_specialisms['weapon'] == 1:
            if item_real_quality <= 1:
                item[1][1] = item_real_quality
        elif player_specialisms['weapon'] == 2:
            if item_real_quality <= 2:
                item[1][1] = item_real_quality
        elif player_specialisms['weapon'] == 3:
            if item_real_quality <= 3:
                item[1][1] = item_real_quality
            if item_real_bonus <= 1:
                item[2][1] = item_real_bonus
        elif player_specialisms['weapon'] == 4:
            if item_real_quality <= 4:
                item[1][1] = item_real_quality
            if item_real_bonus <= 2:
                item[2][1] = item_real_bonus

    if item_type == 'clothing':
        if player_specialisms['clothing'] == 0:
            pass
        elif player_specialisms['clothing'] == 1:
            if item_real_quality <= 1:
                item[1][1] = item_real_quality
        elif player_specialisms['clothing'] == 2:
            if item_real_quality <= 2:
                item[1][1] = item_real_quality
        elif player_specialisms['clothing'] == 3:
            if item_real_quality <= 3:
                item[1][1] = item_real_quality
            if item_real_bonus <= 1:
                item[2][1] = item_real_bonus
        elif player_specialisms['clothing'] == 4:
            if item_real_quality <= 4:
                item[1][1] = item_real_quality
            if item_real_bonus <= 2:
                item[2][1] = item_real_bonus

    if item_type == 'scroll':
        item_display_name = 'Scroll called ' + str(player_item_knowledge_list[item_index][0])
    else:
        item_display_name = str(player_item_knowledge_list[item_index][0])

    return item_display_name


def name_actor(gender='m'):
    # specify the gender
    if gender == 'm':
        forename = pick_random_from_list(male_forename_list)
    else:  # only currently dealing with either female or male names
        forename = pick_random_from_list(female_forename_list)
    surname = pick_random_from_list(hero_surname_list)

    name = forename + ' ' + surname

    return name


def name_monster(alignment='evil'):
    forename = pick_random_from_list(monster_forenames)
    monster = pick_random_from_list(wandering_monster_types)

    name = forename + ' the ' + monster

    return name


def get_random_faction():
    # return a random faction.
    random_faction_index = libtcod.random_get_int(0, 0, len(faction_list) - 1)

    return faction_list[random_faction_index]


def yes_no_prompt():
    key = libtcod.console_wait_for_keypress(True)

    if key.c == 121:  # y
        return True

    elif key.c == 110:  # n
        return False

    else:
        return False


def hero_message(message, colour1, colour2):
    global hero_message_buffer

    if len(message) > 38:
        message_1 = message[:37] + '-'
        message_2 = message[37:]
        hero_message_buffer.insert(0, [message_1, colour1, colour2])
        hero_message_buffer.insert(0, [message_2, colour1, colour2])
    else:
        hero_message_buffer.insert(0, [message, colour1, colour2])
    # message_buffer.pop() #uncomment this function if message list becomes too big?
    # hero_message_buffer.insert(0, [message, colour1, colour2])

    # clear the info bar area for hero messages
    for x in range(INFO_BAR_WIDTH):
        for y in range(10):
            libtcod.console_set_back(her, x, y, libtcod.Color(24, 2, 24), libtcod.BKGND_SET)
            libtcod.console_put_char(her, x, y, ' ', libtcod.BKGND_NONE)

    # write to the message bar
    libtcod.console_set_foreground_color(her, colour1)
    libtcod.console_print_left(her, 1, 8, libtcod.BKGND_NONE, hero_message_buffer[0][0])
    # now write remaining messages

    for x in range(1, 8):  # currently showing 8 messages
        libtcod.console_set_foreground_color(her, hero_message_buffer[x][2])
        libtcod.console_print_left(her, 1, 8 - x, libtcod.BKGND_NONE, hero_message_buffer[x][0])

    # the above lends itself to a for x in message_bar_height loop, for variable display, and more messages

    libtcod.console_blit(her, 0, 0, INFO_BAR_WIDTH, 10, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT - 10)
    libtcod.console_flush()


def message(message, colour1, colour2):
    global message_buffer

    # message_buffer.pop() #uncomment this function if message list becomes too big?
    message_buffer.insert(0, [message, colour1, colour2])

    # clear the message bar
    for x in range(SCREEN_WIDTH):
        for y in range(MESSAGE_BAR_HEIGHT):
            libtcod.console_set_back(mes, x, y, libtcod.Color(2, 2, 13), libtcod.BKGND_SET)
            libtcod.console_put_char(mes, x, y, ' ', libtcod.BKGND_NONE)

    # write to the message bar
    libtcod.console_set_foreground_color(mes, colour1)
    libtcod.console_print_left(mes, 1, 8, libtcod.BKGND_NONE, message_buffer[0][0])
    # now write remaining messages
    for x in range(1, 8):  # currently showing 8 messages
        libtcod.console_set_foreground_color(mes, message_buffer[x][2])
        libtcod.console_print_left(mes, 1, 8 - x, libtcod.BKGND_NONE, message_buffer[x][0])

    # the above lends itself to a for x in message_bar_height loop, for variable display, and more messages

    libtcod.console_blit(mes, 0, 0, SCREEN_WIDTH, MESSAGE_BAR_HEIGHT, 0, 0, VIEWPORT_HEIGHT)
    libtcod.console_flush()


def log_info(info):
    f = open('logfile.txt', 'a')
    f.write(info + '\n')
    f.close


def log_sales_info(info):
    json_output = json.dumps(info, sort_keys=False, indent=4, separators=(',', ':'))

    f = open('sales_metrics.txt', 'a')
    f.write(json_output + '\n')
    f.close


def render_all():
    global seasons
    global season, game_day

    for y in range(VIEWPORT_HEIGHT):  # set background colours
        for x in range(VIEWPORT_WIDTH):
            bgR = map[x][y].color[0] + glow_map[x][y][0] + seasons[0][2]
            bgG = map[x][y].color[1] + glow_map[x][y][1] + seasons[0][3]
            bgB = map[x][y].color[2] + glow_map[x][y][2] + seasons[0][4]

            if bgR > 250:
                bgR = 250
            elif bgR < 5:
                bgR = 5
            if bgG > 250:
                bgG = 250
            elif bgG < 5:
                bgG = 5
            if bgB > 250:
                bgB = 250
            elif bgB < 5:
                bgB = 5

            libtcod.console_set_back(con, x, y, libtcod.Color(bgR, bgG, bgB), libtcod.BKGND_SET)


    # go through all tiles, and draw any icons
    for y in range(VIEWPORT_HEIGHT):
        for x in range(VIEWPORT_WIDTH):
            fgR = map[x][y].color[3]
            fgG = map[x][y].color[4]
            fgB = map[x][y].color[5]
            libtcod.console_set_foreground_color(con, libtcod.Color(fgR, fgG, fgB))
            libtcod.console_put_char(con, x, y, map[x][y].legend, libtcod.BKGND_NONE)

    # now any heroes, monsters to con_over, blitted after the main screen at a reduced transparency
    for y in range(VIEWPORT_HEIGHT):
        for x in range(VIEWPORT_WIDTH):
            libtcod.console_put_char(con_over, x, y, ' ', libtcod.BKGND_NONE)
            for heroes in town_heroes:
                if heroes.hp['current'] > 0:  # is the hero alive?
                    if [x, y] == [heroes.x, heroes.y]:
                        libtcod.console_set_foreground_color(con_over, libtcod.light_red)  # all one colour for now
                        libtcod.console_put_char(con_over, x, y, '@', libtcod.BKGND_NONE)
            for monster in monster_list:
                if [x, y] == [monster.x, monster.y]:
                    libtcod.console_set_foreground_color(con_over, libtcod.red)  # all one colour for now
                    libtcod.console_put_char(con_over, x, y, 'M', libtcod.BKGND_NONE)

    # blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_blit(con_over, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0, 0.75,
                         0.0)  # blitted after the main console, background clear
    # blit the message bar
    libtcod.console_blit(mes, 0, 0, SCREEN_WIDTH, MESSAGE_BAR_HEIGHT, 0, 0, VIEWPORT_HEIGHT)
    # blit the info bar
    libtcod.console_blit(inf, 0, 0, INFO_BAR_WIDTH, VIEWPORT_HEIGHT - 10, 0, VIEWPORT_WIDTH, 0)
    libtcod.console_blit(her, 0, 0, INFO_BAR_WIDTH, 10, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT - 10)

    libtcod.console_flush()


def update_info_bar():
    global player_bid, bid_placed, auction_item, pause

    # clear the info bar prior to input of info
    for x in range(INFO_BAR_WIDTH):
        for y in range(VIEWPORT_HEIGHT - 10):
            libtcod.console_set_back(inf, x, y, libtcod.Color(24, 2, 2), libtcod.BKGND_SET)
            libtcod.console_put_char(inf, x, y, ' ', libtcod.BKGND_NONE)

    # write info in info bar

    libtcod.console_set_foreground_color(inf, libtcod.white)
    # mouse location information
    libtcod.console_print_left(inf, 1, 2, libtcod.BKGND_NONE, get_info_under_mouse()['map_name'])
    libtcod.console_print_left(inf, 1, 4, libtcod.BKGND_NONE, get_info_under_mouse()['map_faction'])

    # reputation, marks out of six for next level
    pl_xp_float = float(player.reputation.xp)
    pl_nextlevel = float(player.base_level * store_base_level_exp)

    rep_bar = int((pl_xp_float / pl_nextlevel) * 6)  # number from 1 to 6

    # player shop information
    libtcod.console_print_left(inf, 7, 7, libtcod.BKGND_NONE, str(player.wealth))
    libtcod.console_print_left(inf, 7, 8, libtcod.BKGND_NONE, str(player.base_level))
    libtcod.console_set_foreground_color(inf, libtcod.gray)
    libtcod.console_print_left(inf, 7, 9, libtcod.BKGND_NONE, '------')
    libtcod.console_set_foreground_color(inf, libtcod.light_red)
    for p in range(rep_bar):
        libtcod.console_print_left(inf, 7 + p, 9, libtcod.BKGND_NONE, '#')

    libtcod.console_set_foreground_color(inf, libtcod.white)
    libtcod.console_print_left(inf, 20, 7, libtcod.BKGND_NONE, str(turns))
    libtcod.console_print_left(inf, 20, 8, libtcod.BKGND_NONE, game_day + " " + str(day))
    libtcod.console_print_left(inf, 20, 9, libtcod.BKGND_NONE, season)

    libtcod.console_set_foreground_color(inf, libtcod.light_blue)
    if get_info_under_mouse()['hero_present']:  # is a hero at the location?
        libtcod.console_print_left(inf, 20, 4, libtcod.BKGND_NONE, 'Hero Present')

        show_heroes(get_info_under_mouse()['hero_list'])

    libtcod.console_set_foreground_color(inf, libtcod.light_red)
    if get_info_under_mouse()['monster_present']:
        libtcod.console_print_left(inf, 20, 5, libtcod.BKGND_NONE, 'Monster Present')

        show_monsters(get_info_under_mouse()['monsters'])

        # else:
        #   libtcod.console_print_left(inf, 20, 4, libtcod.BKGND_NONE, '            ')

    libtcod.console_set_foreground_color(inf, libtcod.red)
    libtcod.console_print_left(inf, 12, 11, libtcod.BKGND_NONE, str(tax_rate))

    libtcod.console_set_foreground_color(inf, libtcod.gray)
    # mouse location information, printing the header text (in grey)
    libtcod.console_print_left(inf, 1, 1, libtcod.BKGND_NONE, 'Name:')
    libtcod.console_print_left(inf, 1, 3, libtcod.BKGND_NONE, 'Belongs to:')

    # player shop information
    libtcod.console_print_left(inf, 1, 6, libtcod.BKGND_NONE, '-YOUR STATUS-')
    libtcod.console_print_left(inf, 3, 7, libtcod.BKGND_NONE, '$$$:')
    libtcod.console_print_left(inf, 3, 8, libtcod.BKGND_NONE, 'LVL:')
    libtcod.console_print_left(inf, 3, 9, libtcod.BKGND_NONE, 'REP:')

    libtcod.console_print_left(inf, 3, 11, libtcod.BKGND_NONE, 'TAX RATE:')


    # turn information
    libtcod.console_print_left(inf, 15, 7, libtcod.BKGND_NONE, 'Time:')
    libtcod.console_print_left(inf, 15, 8, libtcod.BKGND_NONE, 'Day:')
    libtcod.console_print_left(inf, 15, 9, libtcod.BKGND_NONE, 'Mnth:')

    libtcod.console_set_foreground_color(inf, libtcod.dark_gray)
    libtcod.console_print_left(inf, 3, 12, libtcod.BKGND_NONE, '(pay end mth.)')

    # paused?
    if pause:
        libtcod.console_set_foreground_color(inf, libtcod.red)
        libtcod.console_print_left(inf, 20, 2, libtcod.BKGND_NONE, 'P A U S E D')

    if game_speed == fast_speed:
        libtcod.console_set_foreground_color(inf, libtcod.light_red)
        libtcod.console_print_left(inf, 35, 2, libtcod.BKGND_NONE, '>>>')
    elif game_speed == slow_speed:
        libtcod.console_set_foreground_color(inf, libtcod.light_green)
        libtcod.console_print_left(inf, 35, 2, libtcod.BKGND_NONE, '>')
    elif game_speed == normal_speed:
        libtcod.console_set_foreground_color(inf, libtcod.light_blue)
        libtcod.console_print_left(inf, 35, 2, libtcod.BKGND_NONE, '>>')
    elif game_speed == daft_speed:
        libtcod.console_set_foreground_color(inf, libtcod.red)
        libtcod.console_print_left(inf, 35, 2, libtcod.BKGND_NONE, '>>>>')

    # News / Update information
    if auction_item:
        libtcod.console_set_foreground_color(inf, libtcod.white)
        libtcod.console_print_left(inf, 20, 11, libtcod.BKGND_NONE, 'Auction Today!')
        libtcod.console_print_left(inf, 20, 12, libtcod.BKGND_NONE, str(len(bidders)) + ' interested')
        if not bid_placed:
            libtcod.console_set_foreground_color(inf, libtcod.gray)
            libtcod.console_print_left(inf, 20, 13, libtcod.BKGND_NONE, 'You have not bid')
            libtcod.console_print_right(inf, 37, 14, libtcod.BKGND_NONE, 'on ' + player_item_display(auction_item))
        else:
            libtcod.console_set_foreground_color(inf, libtcod.yellow)
            libtcod.console_print_left(inf, 20, 13, libtcod.BKGND_NONE, 'You bid $' + str(player_bid))
            libtcod.console_set_foreground_color(inf, libtcod.dark_yellow)
            libtcod.console_print_right(inf, 39, 14, libtcod.BKGND_NONE, 'on ' + player_item_display(auction_item))
    else:
        libtcod.console_set_foreground_color(inf, libtcod.gray)
        libtcod.console_print_left(inf, 20, 11, libtcod.BKGND_NONE, 'No auction today.')

    if item_examined:
        libtcod.console_set_foreground_color(inf, libtcod.gray)
        libtcod.console_print_left(inf, 20, 15, libtcod.BKGND_NONE, 'Item examined today')
    else:
        libtcod.console_set_foreground_color(inf, libtcod.yellow)
        libtcod.console_print_left(inf, 20, 15, libtcod.BKGND_NONE, 'Can examine items')

    if accepting_offers:
        libtcod.console_set_foreground_color(inf, libtcod.dark_green)
        libtcod.console_print_left(inf, 22, 16, libtcod.BKGND_NONE, 'Taking (O)ffers')
    else:
        libtcod.console_set_foreground_color(inf, libtcod.dark_red)
        libtcod.console_print_left(inf, 20, 16, libtcod.BKGND_NONE, 'Not Taking (O)ffers')

    if selling_goods:  # player shop status
        libtcod.console_set_foreground_color(inf, libtcod.dark_green)
        libtcod.console_print_left(inf, 4, 16, libtcod.BKGND_NONE, 'Shop O(p)en')
    else:
        libtcod.console_set_foreground_color(inf, libtcod.dark_red)
        libtcod.console_print_left(inf, 1, 16, libtcod.BKGND_NONE, '(P)remises closed')

    # world evil and chaos measures
    libtcod.console_set_foreground_color(inf, libtcod.gray)  # draw middle point of balance
    libtcod.console_print_left(inf, 19, 17, libtcod.BKGND_NONE, '.')

    world_evil_float = float(total_item_evil)
    total_evil_float = float(100)

    evil_bar = int((world_evil_float / total_evil_float) * 25)  # normalising number for display bar length

    libtcod.console_set_foreground_color(inf, libtcod.dark_red)
    libtcod.console_print_left(inf, 2, 18, libtcod.BKGND_NONE, 'evil|                         |good')
    libtcod.console_set_foreground_color(inf, libtcod.gray)
    libtcod.console_print_left(inf, 7, 18, libtcod.BKGND_NONE, '------------|------------')
    libtcod.console_set_foreground_color(inf, libtcod.red)

    libtcod.console_print_left(inf, 7 + evil_bar, 18, libtcod.BKGND_NONE, 'o')

    world_chaos_float = float(total_item_chaos)
    total_chaos_float = float(100)

    chaos_bar = int((world_chaos_float / total_chaos_float) * 25)  # normalising number for display bar length

    libtcod.console_set_foreground_color(inf, libtcod.dark_green)
    libtcod.console_print_left(inf, 1, 19, libtcod.BKGND_NONE, 'chaos|                         |order')
    libtcod.console_set_foreground_color(inf, libtcod.gray)
    libtcod.console_print_left(inf, 7, 19, libtcod.BKGND_NONE, '------------|------------')
    libtcod.console_set_foreground_color(inf, libtcod.green)

    libtcod.console_print_left(inf, 7 + chaos_bar, 19, libtcod.BKGND_NONE, 'o')

    libtcod.console_blit(inf, 0, 0, INFO_BAR_WIDTH, VIEWPORT_HEIGHT - 10, 0, VIEWPORT_WIDTH, 0)


def get_info_under_mouse():
    # gives information at the mouse coordinates
    info = {}
    mouse = libtcod.mouse_get_status()
    (x, y) = (mouse.cx, mouse.cy)
    if x > MAP_WIDTH - 1:
        x = MAP_WIDTH - 1
    if y > MAP_HEIGHT - 1:
        y = MAP_HEIGHT - 1
    if x < 0:
        x = 0
    if y < 0:
        y = 0

    hero_here = 0
    monster_here = 0

    mouse_heroes = []
    for heroes in town_heroes:
        if [x, y] == [heroes.x, heroes.y]:
            if heroes.hp['current'] > 0:  # is the hero alive?
                hero_here = 1
                mouse_heroes.append(heroes)

    monsters = []
    for monster in monster_list:
        if [x, y] == [monster.x, monster.y]:
            monster_here = 1
            monsters.append(monster)

    info = {
        'map_name': map[x][y].name,
        'map_faction': map[x][y].faction,
        'hero_present': hero_here,
        'hero_list': mouse_heroes,
        'monster_present': monster_here,
        'monsters': monsters
    }  # expand as necessary

    return info


def handle_mouse(status='main'):
    # watch the mouse during the normal game turn
    # global actor_selected

    if status == 'main':
        mouse = libtcod.mouse_get_status()
        (x, y) = (mouse.cx, mouse.cy)

        if x > MAP_WIDTH - 1:
            x = MAP_WIDTH - 1
        if y > MAP_HEIGHT - 1:
            y = MAP_HEIGHT - 1
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        pressed = 0  # clearing generic output signal from any logic

        if mouse.lbutton_pressed:
            if map[x][y].name == 'Auction House':
                auction_house_welcome(x, y)
                # elif map[x][y].faction == player_name:
                # run the player home functions, awaited, generic will do for now
            elif map[x][y].shop:
                faction_house_welcome(x, y)

        if mouse.rbutton_pressed:
            # display relevant information about that particular map tile?
            pass


def handle_keys():
    global pause, game_speed, debug_mode
    global accepting_offers, selling_goods
    global font_index

    key = libtcod.console_check_for_keypress()  # real-time
    # key = libtcod.console_wait_for_keypress(True)  #turn-based

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_BACKSPACE:
        save_game()
        return True  # exit game

    elif key.vk == libtcod.KEY_PAGEUP:
        max_fonts = len(available_fonts)

        if font_index != max_fonts - 1:
            font_index += 1
        else:
            font_index = 0

        font_name = available_fonts[font_index]
        libtcod.console_set_custom_font(font_name, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, menu_title, False)

    elif libtcod.console_is_key_pressed(libtcod.KEY_SPACE):
        if pause:
            pause = False
            message('Unpaused', libtcod.light_yellow, libtcod.dark_yellow)
        elif not pause:
            pause = True
            message('Paused', libtcod.light_red, libtcod.dark_red)

    elif key.c == 108 or key.c == 76:  # l,L = 108, 76
        # show ledger
        show_ledger()

        # ~ elif libtcod.console_is_key_pressed(libtcod.KEY_2):
        # ~ #give the player 10 experience
        # ~ ledger_new_month()

    elif key.c == 106:
        message(player_name, libtcod.red, libtcod.dark_red)

    elif key.c == 104:  # h,H = 104, 72
        # hero message
        hero_interface()

    elif key.c == 72:
        if len(town_heroes) > 0:
            individual_hero_interface(0)

    elif key.c == 63:
        # help message
        help()  # ? = 63

    elif key.c == 99:
        contract_interface()

    elif key.c == 68 or key.c == 100:  # d = 100, D = 68
        # dungeon display interface
        dungeon_interface()

    elif key.c == 112 or key.c == 80:  # p or P
        if selling_goods:
            selling_goods = 0
        else:
            selling_goods = 1

    elif key.c == 111 or key.c == 79:  # o or O
        if accepting_offers:
            accepting_offers = 0
        else:
            accepting_offers = 1

    elif key.c == 105:  # i for inventory
        for shop in shop_list_inc_player:
            if shop[0] == player_name:
                [x, y] = [shop[2], shop[3]]
        faction_house_welcome(x, y)

    elif key.c == 97:  # a for auction house
        x = 0
        y = 0
        for shop in shop_list_inc_player:
            if shop[1] == 'Auction House':
                [x, y] = [shop[2], shop[3]]
        if x and y:
            auction_house_welcome(x, y)

    elif libtcod.console_is_key_pressed(libtcod.KEY_5) or libtcod.console_is_key_pressed(libtcod.KEY_KP5):
        # Speed up game
        if game_speed == slow_speed:
            game_speed = normal_speed
        elif game_speed == normal_speed:
            game_speed = fast_speed
        elif game_speed == fast_speed:
            game_speed = daft_speed
        else:
            pass

    elif libtcod.console_is_key_pressed(libtcod.KEY_6) or libtcod.console_is_key_pressed(libtcod.KEY_KP6):
        # Slow down game
        if game_speed == daft_speed:
            game_speed = fast_speed
        elif game_speed == fast_speed:
            game_speed = normal_speed
        elif game_speed == normal_speed:
            game_speed = slow_speed
        else:
            pass

    elif libtcod.console_is_key_pressed(libtcod.KEY_4):
        pass
        # output_data()

    elif libtcod.console_is_key_pressed(libtcod.KEY_7) or libtcod.console_is_key_pressed(libtcod.KEY_KP7):
        # debug key to add some cash to the player
        player.wealth += 100
        message('F U N D', libtcod.light_green, libtcod.dark_green)

    elif libtcod.console_is_key_pressed(libtcod.KEY_0) or libtcod.console_is_key_pressed(libtcod.KEY_KP0):
        debug_mode = 1
        message('debug mode on', libtcod.green, libtcod.dark_green)

    elif libtcod.console_is_key_pressed(libtcod.KEY_9) or libtcod.console_is_key_pressed(libtcod.KEY_KP9):
        debug_mode = 0
        message('debug mode off', libtcod.green, libtcod.dark_green)

    elif libtcod.console_is_key_pressed(libtcod.KEY_1) or libtcod.console_is_key_pressed(libtcod.KEY_KP1):
        if len(town_heroes) > 0:
            individual_hero_interface(0)


def name_scroll():
    # initialise random names
    libtcod.namegen_parse('data/names/standard_names.txt')
    # generate name, and store it
    name = libtcod.namegen_generate_custom('male', '$s$50m$25m$e')

    # now clear memory
    libtcod.namegen_destroy()
    return name


def log_sale(item_name, amount, buyer):
    global the_ledger

    datestamp = game_day + ' ' + str(day)  # + time? str(turns)

    record = [season, datestamp, item_name, 'Sold  ', str(amount), '-', buyer]

    the_ledger[-1].append(record)


def log_purchase(item_name, amount, seller):
    global the_ledger

    datestamp = game_day + ' ' + str(day)  # + time? str(turns), year etc... no space ...

    record = [season, datestamp, item_name, 'Bought', '-', str(amount), seller]

    the_ledger[-1].append(record)


def ledger_new_month():  # new sheet on the ledger
    global the_ledger

    the_ledger.append([[season, ' ', ' ', ' ', ' ', ' ', ' ']])


def hero_rot():
    global hero_rot_time, contract_list

    for hero in dead_heroes:
        hero[1] += 1
        if hero[
            1] >= hero_rot_time:  # should only happen once, but we keep a log of all dead heroes anyway, and of course respective time of death

            if log_information:
                log_info(str(hero[0].name) + " rotting, with a time of " + str(hero[1]))

            try:
                town_heroes.remove(hero[0])
            except:
                pass
            dead_heroes.remove(hero)

            # need to birth another ...
            hero_message(hero[0].name + ' rots away!', libtcod.red, libtcod.dark_red)

            gender_test = libtcod.random_get_int(0, 0, 1)
            if gender_test == 0:
                gender = 'm'
            else:
                gender = 'f'

            birth_hero(gender)
            hero_message(hero_list[-1].name + ' takes up the fight!', libtcod.green, libtcod.dark_green)


def json_output(path, filename, info):
    json_output = json.dumps(info, sort_keys=False, indent=4, separators=(',', ':'))

    f = open(path + filename + '.txt', 'w')
    f.write(json_output + '\n')
    f.close


def output_data():
    json_output('data/init/', 'available_fonts', available_fonts)
    json_output('data/init/', 'menu_title', menu_title)

    json_output('data/names/', 'male_forename_list', male_forename_list)
    json_output('data/names/', 'female_forename_list', female_forename_list)
    json_output('data/names/', 'hero_surname_list', hero_surname_list)
    json_output('data/names/', 'monster_forenames', monster_forenames)
    json_output('data/names/', 'wandering_monster_types', wandering_monster_types)

    json_output('data/dungeons/', 'dungeon_type_list', dungeon_type_list)
    json_output('data/names/', 'nasty_things_prefixes', nasty_things_prefixes)
    json_output('data/names/', 'nasty_things_suffixes', nasty_things_suffixes)

    json_output('data/names/', 'town_names', town_names)

    json_output('data/events/', 'event_chat_with_pre', event_chat_with_pre)
    json_output('data/events/', 'event_chat_with_post', event_chat_with_post)

    json_output('data/events/', 'event_enter_town_by_faction', event_enter_town_by_faction)
    json_output('data/events/', 'event_leave_town_by_faction', event_leave_town_by_faction)
    json_output('data/events/', 'event_world_by_faction', event_world_by_faction)

    json_output('data/events/', 'event_tout', event_tout)

    json_output('data/events/', 'event_fight_monster', event_fight_monster)
    json_output('data/events/', 'event_fight', event_fight)
    json_output('data/events/', 'event_success_fight', event_success_fight)
    json_output('data/events/', 'event_damaged_fight', event_damaged_fight)

    json_output('data/events/', 'event_down_stairs', event_down_stairs)
    json_output('data/events/', 'event_up_stairs', event_up_stairs)

    json_output('data/events/', 'event_misc_evil', event_misc_evil)
    json_output('data/events/', 'event_misc_good', event_misc_good)
    json_output('data/events/', 'event_misc_neutral', event_misc_neutral)

    json_output('data/events/', 'event_item_location', event_item_location)
    json_output('data/events/', 'event_item_found', event_item_found)

    json_output('data/events/', 'event_item_bought', event_item_bought)
    json_output('data/events/', 'event_item_sold', event_item_sold)

    json_output('data/events/', 'event_gain_level', event_gain_level)

    json_output('data/monsters/', 'master_monster_list', master_monster_list)
    json_output('data/items/', 'master_item_list', master_item_list)
    json_output('data/heroes/', 'perk_tables', perk_tables)


def main_init():
    # initialise main items
    # font_name = 'arial10x10.png'
    font_name = available_fonts[font_index]
    libtcod.console_set_custom_font(font_name, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, menu_title, False)
    libtcod.sys_set_fps(LIMIT_FPS)


def game_screen_init():
    global con, con_over, mes, inf, her
    # initialise game screens
    con = libtcod.console_new(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)  # main viewport
    con_over = libtcod.console_new(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)  # overlay to main viewport, for actors etc.
    mes = libtcod.console_new(SCREEN_WIDTH, MESSAGE_BAR_HEIGHT)  # message bar (at bottom)
    inf = libtcod.console_new(INFO_BAR_WIDTH, VIEWPORT_HEIGHT - 10)  # info bar (to right)
    her = libtcod.console_new(INFO_BAR_WIDTH, 10)  # hero output bar (bottom ish right)


def setup_new_data():
    global player_specialisms
    global master_item_list, master_monster_list
    global player_item_knowledge_list
    global hero_list, town_heroes, dead_heroes
    global monster_list
    global contract_list
    global the_ledger
    global ecosystems
    global message_buffer, hero_message_buffer
    global seasons, season, day_names, game_day
    global faction_list, scroll_users, perk_tables
    global sales_metrics, the_mayoress
    global built_dungeon_room_tables, dungeon_layout_list

    ##########################
    ##SEASON AND DAY INFORMATION ##
    ##########################

    # season information (name, daysinmonth, red offset, green offset, blue offset)
    seasons = [
        ('January', 31, 0, 15, 30),
        ('February', 28, 5, 20, 25),
        ('March', 31, 10, 25, 15),
        ('April', 30, 20, 35, 5),
        ('May', 31, 25, 30, 0),
        ('June', 30, 30, 25, 0),
        ('July', 31, 35, 20, 0),
        ('August', 31, 30, 10, 5),
        ('September', 30, 25, 5, 10),
        ('October', 31, 15, 0, 10),
        ('November', 30, 5, 0, 15),
        ('December', 31, 0, 0, 25),
    ]

    season = seasons[0][0]

    day_names = [
        ('Monday', 0),
        ('Tuesday', 0),
        ('Wednesday', 0),
        ('Thursday', 0),
        ('Friday', 0),
        ('Saturday', 0),
        ('Sunday', 0),
    ]

    game_day = day_names[0][0]

    # these are the factions that have real estate in the world.
    # Set up the shop in the map builder (currently manually built)
    # Generic factions can be made, with no shops (e.g. dungeons)?
    faction_list = [
        'Thieves',
        'Assassins',
        'Swashbucklers',
        'Fighters',
        'Barbarians',
        'Mages Guild',
        'Druids',
        'Summoners',
        'Necromancers',
        'Temple',
        'Church',
        'Merchants',
    ]

    scroll_users = [  # list of factions that want to keep hold of scrolls. to be deprecated by faction raison d'etre.
                      'Mages Guild',
                      'Druids',
                      'Summoners',
                      'Necromancers',
                      'Temple',
                      'Church',
                      ]

    sales_metrics = Metrics({}, {})

    for faction in faction_list:
        sales_metrics.item_bought[faction] = []
        sales_metrics.item_sold[faction] = []
    sales_metrics.item_bought[player_name] = []
    sales_metrics.item_sold[player_name] = []

    # message buffers for a new game
    blank_message = ['', libtcod.white, libtcod.light_grey]
    message_buffer = [blank_message, blank_message, blank_message, blank_message, blank_message, blank_message,
                      blank_message, blank_message]
    hero_message_buffer = [blank_message, blank_message, blank_message, blank_message, blank_message, blank_message,
                           blank_message, blank_message]

    player_specialisms = {
        'weapon': 0,
        'armor': 0,
        'clothing': 0,
        'scroll': 0,
    }

    ##initialise main knowledge, lists etc.

    f = open('data/heroes/perk_tables.txt', 'r')
    perk_tables = yaml.load(f.read())
    f.close()

    monster_list = []  # none yet
    contract_list = []  # none yet (of course)

    f = open('data/items/master_item_list.txt', 'r')
    master_item_list = yaml.load(f.read())
    f.close()

    for item in master_item_list:
        if item[0] == 'RANDOM':
            item[0] = name_scroll()  # then convert any random names to something else - mainly for scrolls ...

    f = open('data/monsters/master_monster_list.txt', 'r')
    master_monster_list = yaml.load(f.read())
    f.close()
    ##initialise main monster list / dictionary

    hero_list = []  # used for all heroes throughout the world
    town_heroes = []  # used for the heroes in town, starts empty
    dead_heroes = []  # thankfully this is also empty at the start

    the_ledger = [[[season, ' ', ' ', ' ', ' ', ' ', ' ']]]

    # create player knowledge list from master list
    player_item_knowledge_list = []

    for x in range(len(master_item_list)):
        y = master_item_list[x]
        player_item_knowledge_list.append([y[0], 0, 0, 0, 0, 0, [], []])  # no knowledge for the starting player
        # [Known_name, Known_reason, Known_description, Known_level, Known_alignment, Known_order, Known_faction, Known_effect]

    the_mayoress = Mayoress(
        basic_inventory(),
        1800,
        1,
        Reputation(0, blank_faction_relations()),
        libtcod.random_get_int(0, 15, 25),
        50,
        50,
        Noticeboard([], []),
        default_personality['Mayoress'],
        []  # flags
    )

    # generate map
    make_map()
    # generate levelled monster lists
    ecosystems = {}  # the ecosystems dictionary, used for population generation
    build_ecosystems()
    # setup dungeon room types
    build_dungeon_room_tables()
    # say hello, as we are creating data for a new game
    message('Welcome to 100 Heroes! Press ? for help.', libtcod.white, libtcod.light_grey)  # show the message bar
    hero_message('Hero activity will appear here!', libtcod.white, libtcod.light_grey)  # highlight the hero messages

    # generate some heroes
    no_heroes = 100  # set the number here, worldwide for now.

    for c in range(no_heroes):  # make the heroes to start with
        gender_test = libtcod.random_get_int(0, 0, 1)
        if gender_test == 0:
            gender = 'm'
        else:
            gender = 'f'

        level_roll = libtcod.random_get_int(0, 0, 100)

        if level_roll < 80:
            level = 1
        elif level_roll < 94:
            level = 2
        else:
            level = 3

        birth_hero(gender, level)

    for heroes in hero_list:  # get them to appraise their items to start with, plus anything else
        heroes.appraise_inventory()
        heroes.add_perks()


def build_shop_and_dungeon_lists():
    global shop_list_inc_player
    global shop_list
    # map out the starting stores
    map_shops()
    map_dungeons()
    shop_list_inc_player = shop_list[:]  # set up a copy of the shop list, which we will add the player to

    for y in range(VIEWPORT_HEIGHT):
        for x in range(VIEWPORT_WIDTH):
            if map[x][y].faction == player_name:
                shop_list_inc_player.append(
                    [map[x][y].faction, map[x][y].name, x, y])  # add player details to this copy of the shop list


def commence_new_commerce():
    global bid_placed, bidders, auction_item
    global player_bid

    for shop in shop_list:  # set value of stock at the start of the game, on a shop by shop basis
        appraise_stock(shop[1])

        # set up the starting condition for the auction house, which will change back to this every day
    bid_placed = 0  # no bid has been placed by the player
    bidders = []
    player_bid = 0
    auction_item = None

    auction_commence()  # start up the auction process


def new_game():
    enter_name()
    intro()

    setup_new_data()
    build_shop_and_dungeon_lists()
    commence_new_commerce()
    set_glow()

    render_all()
    update_info_bar()

    libtcod.console_flush()

    choose_upgrade()

    if log_information:
        log_info('#===>   *  - New Game -  *   <===#')


def intro():
    window = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
    libtcod.console_set_foreground_color(window, libtcod.white)

    img = libtcod.image_load('gfx/intro.png')
    libtcod.image_blit_2x(img, 0, 0, 0)

    libtcod.console_print_left(window, 11, 2, libtcod.BKGND_NONE, 'Welcome to Town.')
    libtcod.console_print_left(window, 14, 6, libtcod.BKGND_NONE, 'It aint the competition you need to worry about.')
    libtcod.console_print_left(window, 17, 10, libtcod.BKGND_NONE, 'Happy retailin.')
    libtcod.console_print_left(window, 32, 14, libtcod.BKGND_NONE, 'PRESS SPACE TO BEGIN')

    libtcod.console_blit(window, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0, 1.0, 0.0)
    libtcod.console_flush()

    key = libtcod.console_wait_for_keypress(True)

    while key.vk != libtcod.KEY_SPACE:
        pass
        key = libtcod.console_wait_for_keypress(True)


def continue_game():
    global player

    build_shop_and_dungeon_lists()
    set_glow()

    for y in range(VIEWPORT_HEIGHT):
        for x in range(VIEWPORT_WIDTH):
            if map[x][y].faction == player_name:
                player = map[x][y].shop

    message('Game loaded ... welcome back', libtcod.white, libtcod.light_grey)
    hero_message('The Heroes return!', libtcod.white, libtcod.light_grey)


def menu(header, options, width):
    # # code almost entirely reappropriated from Jotaf's Tutorial --- Thanks Jotaf!
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = 1
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_foreground_color(window, libtcod.white)
    libtcod.console_print_left_rect(window, 0, 0, width, height, libtcod.BKGND_NONE, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_left(window, 0, y, libtcod.BKGND_NONE, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = SCREEN_WIDTH / 2 - width / 2
    y = SCREEN_HEIGHT / 2 - height / 2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

    # present the root console to the player and wait for a key-press
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:  # (special case) Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    # convert the ASCII code to an index; if it corresponds to an option, return it
    index = key.c - ord('a')
    if index >= 0 and index < len(options): return index
    return None


def main_menu():
    img = libtcod.image_load('gfx/title.png')

    while not libtcod.console_is_window_closed():
        # show the background image, at twice the regular console resolution
        libtcod.image_blit_2x(img, 0, 0, 0)

        # show options and wait for the player's choice
        choice = menu('WELCOME TO 100 HEROES', ['Play a new game', 'Continue last game', 'Quit'], 24)

        if choice == 0:  # new game
            game_screen_init()
            new_game()
            break
        if choice == 1:  # continue game
            try:
                load_game()
            except:
                # pass
                continue
            game_screen_init()
            continue_game()
            break
        elif choice == 2:  # quit
            sys.exit()


#####################
## game data file functions ##
#####################

def save_game():  # game save function

    message('saving game', libtcod.white, libtcod.light_grey)

    # sanitise_hero_lists_for_saving() #not now necessary

    file = shelve.open('savegame', 'n')
    file['the_mayoress'] = the_mayoress
    file['sales_metrics'] = sales_metrics
    file['day_count'] = day_count
    file['map'] = map
    file['player_item_knowledge_list'] = player_item_knowledge_list
    file['master_monster_list'] = master_monster_list
    file['master_item_list'] = master_item_list
    file['town_heroes'] = town_heroes  # town heroes
    file['dead_heroes'] = dead_heroes  # dead heroes
    file['hero_list'] = hero_list  # other heroes
    file['auction_item'] = auction_item  # auction item
    file['bid_placed'] = bid_placed  # bid placed
    file['item_examined'] = item_examined  # item examined
    file['game_speed'] = game_speed
    file['tax_rate'] = tax_rate
    file['bidders'] = bidders
    file['player_bid'] = player_bid
    file['pause'] = pause
    file['player_specialisms'] = player_specialisms
    file['hero_message_buffer'] = hero_message_buffer
    file['message_buffer'] = message_buffer
    file['the_ledger'] = the_ledger
    file['faction_list'] = faction_list
    file['scroll_users'] = scroll_users
    file['ecosystems'] = ecosystems
    file['max_monster_level'] = max_monster_level
    file['seasons'] = seasons
    file['season'] = season
    file['day_names'] = day_names
    file['game_day'] = game_day
    file['day'] = day
    file['year'] = year
    file['turns'] = turns
    file['sub_turns'] = sub_turns
    file['perk_tables'] = perk_tables
    file['total_item_evil'] = total_item_evil
    file['total_item_chaos'] = total_item_chaos
    file['selling_goods'] = selling_goods
    file['accepting_offers'] = accepting_offers
    file['evil_counter'] = evil_counter
    file['chaos_counter'] = chaos_counter
    file['inactive_sites'] = inactive_sites
    file['monster_list'] = monster_list
    file['contract_list'] = contract_list
    file['player_name'] = player_name
    file['built_dungeon_room_tables'] = built_dungeon_room_tables
    file['dungeon_layout_list'] = dungeon_layout_list
    file.close()

    if log_information:
        log_info('Game successfully saved')


def load_game():
    global map  # need to get all variables into global
    global player_item_knowledge_list, master_monster_list, master_item_list
    global message_buffer, hero_message_buffer, the_ledger
    global town_heroes, dead_heroes, hero_list
    global auction_item, bid_placed, item_examined, bidders, player_bid
    global game_speed, pause
    global tax_rate
    global player_specialisms
    global faction_list, scroll_users, ecosystems, max_monster_level
    global seasons, season, day_names, game_day, day, year, turns, sub_turns
    global perk_tables, total_item_evil, total_item_chaos, selling_goods, accepting_offers
    global evil_counter, chaos_counter
    global inactive_sites
    global monster_list, contract_list
    global player_name
    global the_mayoress, sales_metrics
    global built_dungeon_room_tables, dungeon_layout_list

    file = shelve.open('savegame', 'r')
    map = file['map']
    player_item_knowledge_list = file['player_item_knowledge_list']
    master_monster_list = file['master_monster_list']
    master_item_list = file['master_item_list']
    town_heroes = file['town_heroes']
    dead_heroes = file['dead_heroes']
    hero_list = file['hero_list']
    auction_item = file['auction_item']
    bid_placed = file['bid_placed']
    item_examined = file['item_examined']
    game_speed = file['game_speed']
    tax_rate = file['tax_rate']
    bidders = file['bidders']
    player_bid = file['player_bid']
    pause = file['pause']
    player_specialisms = file['player_specialisms']
    hero_message_buffer = file['hero_message_buffer']
    message_buffer = file['message_buffer']
    the_ledger = file['the_ledger']
    faction_list = file['faction_list']
    scroll_users = file['scroll_users']
    ecosystems = file['ecosystems']
    max_monster_level = file['max_monster_level']
    seasons = file['seasons']
    season = file['season']
    day_names = file['day_names']
    game_day = file['game_day']
    day = file['day']
    day_count = file['day_count']
    year = file['year']
    turns = file['turns']
    sub_turns = file['sub_turns']
    perk_tables = file['perk_tables']
    total_item_evil = file['total_item_evil']
    total_item_chaos = file['total_item_chaos']
    selling_goods = file['selling_goods']
    accepting_offers = file['accepting_offers']
    evil_counter = file['evil_counter']
    chaos_counter = file['chaos_counter']
    inactive_sites = file['inactive_sites']
    contract_list = file['contract_list']
    monster_list = file['monster_list']
    player_name = file['player_name']
    sales_metrics = file['sales_metrics']
    the_mayoress = file['the_mayoress']
    built_dungeon_room_tables = file['built_dungeon_room_tables']
    dungeon_layout_list = file['dungeon_layout_list']
    # ... etc
    file.close()

    # rebuild_hero_lists_after_loading()

    if log_information:
        log_info('Game successfully loaded')


def clear_savegame():
    try:
        os.remove('savegame')
    except:
        pass


def sanitise_hero_lists_for_saving():
    global town_heroes

    heroes_to_clean = []

    for corpse in dead_heroes:
        if corpse[1] < hero_rot_time:  # hero could still be saved?
            heroes_to_clean.append(corpse[0])

    if heroes_to_clean:  # did we find any?
        for cadaver in heroes_to_clean:
            if log_information:
                log_info(str(cadaver))
            town_heroes.remove(cadaver)  # remove these heroes from the town list


def rebuild_hero_lists_after_loading():
    global town_heroes

    for corpse in dead_heroes:
        if corpse[1] < hero_rot_time:  # hero is still solid
            town_heroes.append(corpse[0])  # add partially rotted corpse back in to town list


###############
## main game loop ##
###############

main_init()
main_menu()

while not libtcod.console_is_window_closed():

    # render the screen
    render_all()
    update_info_bar()

    libtcod.console_flush()

    # go to the pass turn function, controls game flow
    if not pause:
        pass_turn()

    # handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break

    handle_mouse()
