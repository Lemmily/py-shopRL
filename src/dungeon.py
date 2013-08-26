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
class Tile():
    
    def __init__(self,x,y, blocks, blocks_sight=True, char = " "):
        self.x = x
        self.y = y
        if isinstance(char, int):
            self.char = chr(char)
        else:
            self.char = char
            
        self.blocks = blocks
        self.blocks_sight = blocks_sight
        self.explored = False
        
        
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
        
        self.tiles = [[None
                       for y in range(self.h)]
                        for x in range(self.w)]
        
        self.up = (self.w/2, self.h/2)
        self.down = (self.w/2 + 4, self.h/2 + 4)
        
        self.construct_floor()
        self.objects = []
        self.construct_objects()
        
        self.fov_map = libtcod.map_new(self.w, self.h)
        self.make_fov_map()
        self.assign_tiles()
        
        
    def construct_floor(self):
        for x in range(len(self.map)):
            self.map[x][0] = 1
            self.map[x][len(self.map[x])-1] = 1
        for y in range(len(self.map[0])):
            self.map[0][y] = 1
            self.map[len(self.map)-1][y] = 1
            
        self.map[libtcod.random_get_int(0, 2, len(self.map)-3)][libtcod.random_get_int(0, 2, len(self.map[0])-3)] = 0
        
        self.rects = []
        self.rects.append(self.make_room(2, 2, 5, 5))
        self.rects.append(self.make_room_random())
        self.rects.append(self.make_room_random())
        self.rects.append(self.make_room_random())
        self.rects.append(self.make_room_random())
        
        self.place_rooms()

    
    def construct_objects(self):
        door = entities.Object(self.up[0], self.up[1], char="D", name="door", colour=libtcod.purple, blocks=True, always_visible=False)
        self.objects.append(door)
        door = entities.Object(self.down[0], self.down[1], char="D", name="door", colour=libtcod.red, blocks=True, always_visible=False)
        self.objects.append(door)
        
        
    def make_room(self,x,y,w,h):
        
        rect = Rect(w,h,x,y)
        for other in self.rects:
            if rect.intersect_other(other):
                return
        
        return rect
    
    
    def make_room_random(self):
        
        unplaced = True
        
        if len(self.rects) > 0:
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
        else:
            w = libtcod.random_get_int(0, 4, 9)
            h = libtcod.random_get_int(0, 4, 9)
            x = libtcod.random_get_int(0, 1, len(self.map) - w - 2)
            y = libtcod.random_get_int(0, 1, len(self.map) - h - 2)
            
            rect = Rect(w,h,x,y)
                
        return rect
    
    def place_rooms(self):
        
        for room in self.rects:
            for x in range(room.x, room.x + room.w -1):
                for y in range(room.y, room.y + room.h -1):
                    self.map[x][y] = 0
                    
    
    def make_fov_map(self):
        
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                if self.map[x][y] == 0:
                    libtcod.map_set_properties(self.fov_map, x, y, True, True)
                else:
                    libtcod.map_set_properties(self.fov_map, x, y, False, False)
                    
    def assign_tiles(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                if self.is_wall(x, y):
                    if self.is_wall(x, y+1) and self.is_wall(x, y-1): #above and below.
                        if self.is_wall(x+1, y) and self.is_wall(x-1, y): #left and right.
                            if self.is_wall(x+1, y+1) and self.is_wall(x-1, y+1) and self.is_wall(x+1, y-1) and self.is_wall(x-1, y-1):
                                #Completeley surrounded by wall.
                                tile = ord(" ")
                            elif self.is_wall(x+1, y-1) and self.is_wall(x-1, y-1) and self.is_wall(x+1, y+1): #bottom left empty.
                                tile = 191
                            elif self.is_wall(x+1, y+1) and self.is_wall(x-1, y+1) and self.is_wall(x+1, y-1): #top left empty.
                                tile = 217
                                
                            elif self.is_wall(x+1, y-1) and self.is_wall(x-1, y-1) and self.is_wall(x-1, y+1): #bottom right empty
                                tile = 218
                            elif self.is_wall(x+1, y+1) and self.is_wall(x-1, y+1) and self.is_wall(x-1, y-1): # top right empty.
                                tile = 192
                                
                            elif self.is_wall(x+1, y-1) and self.is_wall(x-1, y-1): #bottom left and right empty. T shaped
                                tile = 194
                            elif self.is_wall(x+1, y+1) and self.is_wall(x-1, y+1): #top left and right empty.T shaped
                                tile = 193
                            else:
                                tile = 197
                        elif self.is_wall(x+1, y): # right
                            if self.is_wall(x+1, y+1) and self.is_wall(x+1, y-1): # bottom right and top right  
                                tile = 179
                            else:
                                tile = 195
                        elif self.is_wall(x-1, y):
                            if self.is_wall(x-1, y+1) and self.is_wall(x-1, y-1): # bottom left and top left.
                                tile = 179
                            else:
                                tile = 180
                        else:
                            tile = 179
                    elif self.is_wall(x, y+1): #below
                        if self.is_wall(x+1, y) and self.is_wall(x-1, y): #left and right
                            if self.is_wall(x+1, y+1) and self.is_wall(x-1, y+1):
                                tile = 196
                            else:
                                tile = 194
                        elif self.is_wall(x+1, y):
                            tile = 218
                        elif self.is_wall(x-1, y):
                            tile = 191
                        else:
                            tile = 179
                            
                    elif self.is_wall(x, y-1): #above
                        if self.is_wall(x+1, y) and self.is_wall(x-1, y): #left and right
                            if self.is_wall(x+1, y-1) and self.is_wall(x-1, y-1):
                                tile = 196
                            else:
                                tile = 193
                        elif self.is_wall(x+1, y):
                            tile = 192
                        elif self.is_wall(x-1, y):
                            tile = 217
                        else:
                            tile = 179        
                    else:
                        if self.is_wall(x+1, y) and self.is_wall(x-1, y):
                            tile = 196
                        elif self.is_wall(x+1, y):
                            tile = 196
                        elif self.is_wall(x-1, y):
                            tile = 196
                        else:
                            tile = 197
            
                    self.tiles[x][y] = Tile(x,y,True, char = chr(tile))
                else:
                    tile = 056
                    self.tiles[x][y] = Tile(x,y,False, char = chr(tile))


    def is_wall(self,x, y):
        if 0 <= x < len(self.map) and 0 <= y < len(self.map[x]):
            if self.map[x][y] != 0:
                return True
            else:
                return False
        else:
            return False        
        
        