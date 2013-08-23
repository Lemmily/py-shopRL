'''
Created on 21 Aug 2013

@author: Emily
'''

import libtcodpy as libtcod
import random
import json
import json_map

import entities

MONSTERS = json.loads(json_map.monsters)
ITEMS = ["sword","potion","shield","armour","leggings","scroll","wand","book","food"]
#TODO: This stuff should be handled elsewhere.

class Dungeon():
    def __init__(self, x,y, POI):
        self.x = x
        self.y = y 
        self.POI = POI
        self.name = "Dungeon" #TODO: Make a name generator.
        self.floors = []
        
    def turmoil(self):
        """This function will help to randomise the monsters inside. Once the dungeon hits some critical point.
        This will be called and the numbers of monsters inside will shift and change, depending on different thibgs"""
        pass
    
    def addMonster(self, type = ""):
        pass
    
    def addFloor(self, level = -1):
        pass
    
    def generate_floors(self, level = 1, num=5):
        for ID in range(num):
            monster_num = libtcod.random_get_int(0,10,25)
            item_num = libtcod.random_get_int(0,5,15)
            a_items = []
            a_monst = []
            for n in range(monster_num):
                key = random.choice(MONSTERS[str(self.level)].keys())
                mons = MONSTERS[str(self.level)][key]
                #not finsiehd yet.
                colour = libtcod.Color(mons["colour"][0],mons["colour"][1],mons["colour"][2])
                temp = entities.Object(0,0, char=mons["char"], name=mons["name"], colour=colour, blocks=False, always_visible=False)
                
                a_monst.append(mons)
            for n in range(item_num):
                item = random.choice(ITEMS)
                #colour = libtcod.Color(item["colour"][0],item["colour"][1],item["colour"][2])
                #temp = entities.Object(0,0, char=item["char"], name=item["name"], colour=colour, blocks=False, always_visible=False)
                a_items.append(item)
            floor = Floor(ID, a_monst, a_items)
            self.floors.append(floor)
            
class Floor:
    def __init__(self, ID, monst, items):
        self.ID = ID
        self.num_monster = monst 
        self.num_items = items
        self.w = 100
        self.h = 100
        self.map = [[0
                     for y in range(self.h)]
                        for x in range(self.w)]
