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

class Rect:
    def __init__(self,w,h,x,y):  
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        
    def intersect_other(self, other):
        if other.x > self.x and other.x < self.x + self.w:
            return True
        elif other.y > self.y and other.y < self.y + self.h:
            return True
        
        else:
            return False   


class Dungeon():
    def __init__(self, x,y, POI):
        self.x = x
        self.y = y 
        self.POI = POI
        self.name = "Dungeon" #TODO: Make a name generator.
        self.level = 1
        self.floors = []
        
        
        self.generate_floors(1, 3)
        
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
        self.w = 20
        self.h = 20
        self.map = [[1
                     for y in range(self.h)]
                        for x in range(self.w)]
        
        self.construct_floor()
        
        
    def construct_floor(self):
        for x in range(len(self.map)):
            self.map[x][0] = 1
            self.map[x][len(self.map[x])-1] = 1
        for y in range(len(self.map[0])):
            self.map[0][y] = 1
            self.map[len(self.map)-1][y] = 1
            
        self.map[libtcod.random_get_int(0, 2, len(self.map)-3)][libtcod.random_get_int(0, 2, len(self.map[0])-3)] = 0
        
        self.rects = []
        self.rects.append(self.make_room())
            

    def make_room(self):
        
        unplaced = True
        
        while(unplaced):
            
            w = libtcod.random_get_int(0, 4, 9)
            h = libtcod.random_get_int(0, 4, 9)
            
            count = 0
            while(count < 5):
                x = libtcod.random_get_int(0, 1, len(self.map) - w - 1)
                y = libtcod.random_get_int(0, 1, len(self.map) - h - 1)
                rect = Rect(w,h,x,y)
                for other in self.rects:
                    if rect.intersect_other(other):
                        continue
                    else: 
                        unplaced = False
                count += 1
                
        return rect

