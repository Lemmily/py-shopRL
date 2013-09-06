'''
Created on 6 Sep 2013

@author: Emily
'''

skill_list_1 = [ #// 0_name:string, 1_attribute, 2_needTraining:Boolean, 3_desc:String,[4_dependsOn],[5_dependants]
                 ["Appraise", "int", False, "Used to analyse an item for monetary value, and contributing factors",["none"],["none"]],
                 ["Armour", "str", False, "How well you can wear armour. Negates some of the penalties of heavier armour",["none"],["none"]],
                 ["Dodge", "dex", False, "Improves your chance of dodging attacks and traps",["none"],["none"]],
                 ["Fighting", "dex", False, "Improves your chance of hitting and your damage in melee",["none"],["none"]],
                ]
class Skills:
    def __init__(self):
        pass
        self.dict = {}
        for line in skill_list_1:
            self.dict[line[0]] = Skill( line[0], line[1])
        
        
    def skill_level_check(self,skill):
        
        sk_exp = self.dict[skill].exp
        
        return sk_exp #TODO: nake lookup table to look up what level the skill is at. for now just retrun this/

class Skill:
    def __init__(self,name,group="None"):
        self.name = name
        self.group = group
        self.exp = 0
        