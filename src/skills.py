"""
Created on 29 Aug 2013

@author: Emily
"""
import R
import libtcodpy as libtcod


class Skills:
    def __init__(self):
        self.dict = {}
        for line in R.skill_list:
            tempSkill = Skill(line[0],
                              line[1])
            self.dict[tempSkill.name] = tempSkill

    def _get_level(self):
        pass


#################################################################
# class Skill:
#     def __init__(self, name, attr, sk_amt=0):
#         self.name = name
#         self.attr = attr  # main attribute for skill
#         self.exp = sk_amt
#################################################################


attributes = ["str", "con", "dex", "int", "cha", "wis", "luc"]

skill_list_1 = [  # // 0_name:string, 1_attribute, 2_needTraining:Boolean, 3_desc:String,[4_dependsOn],[5_dependants]
                  ["Appraise", "int", False, "Used to analyse an item for monetary value, and contributing factors",
                   ["none"], ["none"]],
                  ["Armour", "str", False,
                   "How well you can wear armour. Negates some of the penalties of heavier armour", ["none"], ["none"]],
                  ["Dodge", "dex", False, "Improves your chance of dodging attacks and traps", ["none"], ["none"]],
                  ["Fighting", "dex", False, "Improves your chance of hitting and your damage in melee", ["none"],
                   ["none"]],
                  ["Tilling", "str", False, "The skill at which you can till the land.", ["none"], ["none"]],
                  ["Fertiliser", "int", False, "The knowledge on Fertilisers and their use on different plants.",
                   ["none"], ["none"]],
                  ["Harvest", "dex", False,
                   "The skill of harvesting plants. Some will need high skill to reap the rewards.", ["none"],
                   ["none"]],
                  ["Plant Expertise", "int", False,
                   "To successfully identify plants and the information about them; this skill is required", ["none"],
                   ["none"]],
                  ]


# Skill manager
class Stats:
    def __init__(self):
        self.skills = {}
        for line in skill_list_1:
            self.skills[line[0].lower()] = Skill(line[0], line[1])

        self.attr = {}
        for stat in attributes:
            self.attr[stat] = Attribute(stat, 10)

    def skill_level_check(self, skill):

        sk_exp = self.skills[skill].exp

        # TODO: make lookup table to look up what level the skill is at. for now just rerun this/
        return sk_exp

    def has(self, skill):
        if skill in self.skills:
            return True
        return False

    def get_level(self, skill):
        return self.skills[skill].level

    def skill_check(self, name):
        if self.has(name):
            skill = self.skills[name]
            return roll_d20() + skill.level + self.attr[skill.group].modifier

    def gain_exp(self, amount, skill):
        # TODO: this is temporary - I want to have exp spread over multiple skills. similar to crawl.
        self.skills[skill].gain(amount)


class Skill:
    def __init__(self, name, group="none"):
        self.name = name
        self.group = group
        self.exp = 0
        self.level = 1
        self.aptitude = 1  # speed at which they gain skill levels.... probably somewhere better to hold this.

    def gain(self, amount):
        self.exp += amount
        if self.exp > 100:
            self.level += 1
            self.exp -= 100
            R.ui.message("You have leveled up " + self.name + " to level " + str(self.level))


class Attribute():
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def modifier(self):
        if self.value <= 1:
            return -5
        elif self.value < 4:
            return -4
        elif self.value < 6:
            return -3
        elif self.value < 8:
            return -2
        elif self.value < 10:
            return -1
        elif self.value < 12:
            return 0
        elif self.value < 14:
            return 1
        elif self.value < 16:
            return 2
        elif self.value < 18:
            return 3
        elif self.value <= 20:
            return 5
        elif self.value > 20:
            return 6


def roll_d20():
    return libtcod.random_get_int(0, 1, 20)