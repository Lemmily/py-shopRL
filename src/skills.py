"""
Created on 29 Aug 2013

@author: Emily
"""
import R


class Skills:
    def __init__(self):
        self.dict = {}
        for line in R.skill_list:
            temp_skill = Skill(line[0], line[1])
            self.dict[temp_skill.name] = temp_skill

    def _get_level(self):
        pass


class Skill:
    def __init__(self, name, attr, sk_amt=0):
        self.name = name
        self.attr = attr  # main attribute for skill
        self.exp = sk_amt
