'''
Created on 21 Aug 2013

@author: Emily
'''

import libtcodpy as libtcod
import random
import json
import json_map

import entities
import Utils

MIN_BSP_SIZE = 5
MIN_ROOM_SIZE = 2

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
        self.continent = -1 #this is here so the pathfinding can check it.
        
        
class Rect:
    def __init__(self,w,h,x,y):
        """ @param w: width of rectangle
            @param h: height of rect
            @param x: x-position of rect
            @param y: y-position of rect
        """ 
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        
    def intersect_other(self, other):
        """
        Can be used in a loop, to compare against all other in a list.
        """
        if other.x > self.x and other.x < self.x + self.w:
            return True
        elif other.y > self.y and other.y < self.y + self.h:
            return True
        
        else:
            return False
        
    def bsp(self,parent=None):   
        self.babies = []
        self.parent = parent
        self.end = False
        
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_w(self):
        return self.w
    def get_h(self):
        return self.h
        


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
                colour = libtcod.Color(mons[2][0],mons[2][1],mons[2][2])
                temp = entities.Object(0,0, char=[1], name=mons[0], colour=colour, blocks=False, always_visible=False)
                
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
        self.w = libtcod.random_get_int(0,30,80)
        self.h = libtcod.random_get_int(0,20,60)
        
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
        self.entities = []
        self.construct_objects()
        
        self.fov_map = libtcod.map_new(self.w, self.h)
        self.make_fov_map()
        self.assign_tiles()
       
       
    def get_floor_tile(self, x, y):
        return self.tiles[x][y] 
        
    def construct_floor(self):
        for x in range(len(self.map)):
            self.map[x][0] = 1
            self.map[x][len(self.map[x])-1] = 1
        for y in range(len(self.map[0])):
            self.map[0][y] = 1
            self.map[len(self.map)-1][y] = 1
            
        self.map[libtcod.random_get_int(0, 2, len(self.map)-3)][libtcod.random_get_int(0, 2, len(self.map[0])-3)] = 0
        
        self.rects = []
        
        self.bsp_gen()
        if len(self.rects) > 0:
            self.up = (self.rects[0].x, self.rects[0].y)
            self.down = (self.rects[len(self.rects) -1].x + 1, self.rects[len(self.rects)-1].y + 1)
        else:
            self.up = (0, 0)
            self.down = (10,10)
        self.place_rooms()

    
    def construct_objects(self):
        stair = entities.Object(self.up[0], self.up[1], char="<", name="stair", colour=libtcod.purple, blocks=False, always_visible=False)
        self.objects.append(stair)
        stair = entities.Object(self.down[0], self.down[1], char=">", name="stair", colour=libtcod.red, blocks=False, always_visible=False)
        self.objects.append(stair)
        
        if len(self.rects) > 0:
            room = self.rects[libtcod.random_get_int(0, 0, len(self.rects)-1)]
            item = entities.Item()
            potion = entities.Object(libtcod.random_get_int(0,room.x,room.x + room.w-2),libtcod.random_get_int(0,room.y,room.y + room.h-2),
                                        char="!", name="potion", colour=libtcod.orange,blocks = False, always_visible=False, item=item)
            self.objects.append(potion)
        
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
                            return rect
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
            #if room.
            for x in range(0,room.w):
                for y in range(0, room.h):
                    _x = room.x + x
                    _y = room.y + y
                    if 0 >_x >= len(self.map) or 0 > _y >= len(self.map[x]):
                        print _x,_y, "out of bounds"
                    else:
                        self.map[_x][_y] = 0
                        
    def make_corridors(self,st_x,st_y,en_x, en_y):
        pass
        #for rect in self.rects
    
    def place_corridors(self,st_x,st_y,en_x, en_y):
        bx = 0
        by = 0
        for x in range(st_x,en_x):
            print x
    
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
                            elif self.is_wall(x-1, y-1) and self.is_wall(x-1, y+1): #top right and bottom right empty.T shaped
                                tile = 195
                            elif self.is_wall(x+1, y-1) and self.is_wall(x+1, y+1): #top right and bottom right empty.T shaped
                                tile = 180
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
              
    def bsp_gen(self):
        
        w = self.w - 2
        h = self.h - 2
        
        whole_map = Rect(w,h,1,1)
        whole_map.bsp()
        
        self.new_split(whole_map)
        self.convert_to_rects(whole_map)
                    
    def split(self, rect):
        if rect.w - 1 >= MIN_BSP_SIZE*1.5 or rect.h - 1 >= MIN_BSP_SIZE*1.5:
            if flip_coin() and rect.w >= MIN_BSP_SIZE:
                x = libtcod.random_get_int(0,rect.x + MIN_BSP_SIZE, rect.x + rect.w - MIN_BSP_SIZE)
                w = (rect.x + rect.w) - x 
                
                tries = 0
                while x + w >= len(self.map) or tries <= 3:
                    print x,w, " horz out of bounds"
                    x = rect.x + 1
                    w = rect.w / 2 - 1
                    
                baby = Rect(rect.w - w, rect.h, rect.x, rect.y)
                baby.bsp(rect)
                baby_2 = Rect(w, rect.h, x, rect.y)
                baby_2.bsp(rect)
                
                rect.babies.append(baby)
                rect.babies.append(baby_2)
            else:
                if rect.w < MIN_BSP_SIZE:
                    y = libtcod.random_get_int(0,rect.y + MIN_BSP_SIZE, rect.y + rect.h - MIN_BSP_SIZE)
                    h = (rect.y + rect.h) - y
                    
                    tries = 0
                    while y + h> len(self.map[0]) or tries <= 3:
                        print y,h, "vert out of bounds"
                        y = rect.y + 1
                        h = rect.h / 2
                            
                    baby = Rect(rect.w, rect.h - h, rect.x, rect.y)
                    baby.bsp(rect)
                    rect.babies.append(baby)
                    
                else:
                    y = libtcod.random_get_int(0,rect.y + MIN_BSP_SIZE, rect.y + rect.h - MIN_BSP_SIZE)
                    
                    h = (rect.y + rect.h) - y
                    
                    tries = 0
                    while y + h> len(self.map[0]) or tries <= 3:
                        print y,h, "vert out of bounds"
                        y = rect.y + 1
                        h = rect.h / 2
                            
                    baby = Rect(rect.w, rect.h - h, rect.x, rect.y)
                    baby.bsp(rect)
                    baby_2 = Rect(rect.w, h, rect.x, y)
                    baby_2.bsp(rect)
                    
                    rect.babies.append(baby)
                    rect.babies.append(baby_2)
                    
        else:
            rect.end = True      
              
        for baby in rect.babies:
            if baby.end != True:
                self.split(baby)
    
    
    
    def new_split(self, rect):
        if rect.w > MIN_BSP_SIZE*2 and rect.h > MIN_BSP_SIZE*2:
            if flip_coin() and rect.x + rect.w/2 + MIN_BSP_SIZE < len(self.map) and rect.y + rect.h/2 + MIN_BSP_SIZE < len(self.map[0]):
                
                x = libtcod.random_get_int(0,rect.x + MIN_BSP_SIZE, rect.x + rect.w - MIN_BSP_SIZE)
                w = (rect.x + rect.w) - x 
                    
                baby = Rect(rect.w - w, rect.h, rect.x, rect.y)
                baby.bsp(rect)
                baby_2 = Rect(w-1, rect.h, x, rect.y)
                baby_2.bsp(rect)
                
                rect.babies.append(baby)
                rect.babies.append(baby_2)
            else:
                y = libtcod.random_get_int(0,rect.y + MIN_BSP_SIZE, rect.y + rect.h - MIN_BSP_SIZE)
                
                h = (rect.y + rect.h) - y
                
                        
                baby = Rect(rect.w, rect.h - h, rect.x, rect.y)
                baby.bsp(rect)
                baby_2 = Rect(rect.w, h-1, rect.x, y)
                baby_2.bsp(rect)
                
                rect.babies.append(baby)
                rect.babies.append(baby_2)   
        else:
            rect.end = True      
              
        for baby in rect.babies:
            if baby.end != True:
                self.new_split(baby)
        
        
    def convert_to_rects(self,rect):
        pool = []
        orig_rect = rect
        #go up and down the bsp tree and fethc only the "end" pieces to store in pool.
        while len(orig_rect.babies) > 0:
            if len(rect.babies) == 0 and rect.parent != None:
                for baby in rect.parent.babies:
                    if baby.end == True:
                        pool.append(baby)
                    rect.parent.babies.remove(baby)
                rect = rect.parent
            if len(rect.babies) > 0:
                rect = rect.babies[0]
            elif rect.parent != None:
                rect = rect.parent
            else:
                break
        
        #then go through the pool and put rooms inside them
        while len(pool) > 0:
            bounds = pool.pop()
            overtried = False
            
            max_w = bounds.w
            max_h = bounds.h
            tries = 0
            while max_w >= MIN_ROOM_SIZE and max_h >= MIN_ROOM_SIZE and not overtried:
                
                if max_w <= MIN_ROOM_SIZE:
                    w = max_w
                else:
                    w = libtcod.random_get_int(0,MIN_ROOM_SIZE,max_w)
                    
                if max_h <= MIN_ROOM_SIZE:
                    h = max_h
                else:
                    h = libtcod.random_get_int(0,MIN_ROOM_SIZE,max_h)
                    
                placed = False
                while not placed:
                    if tries > 5:
                        overtried = True
                    x = libtcod.random_get_int(0,bounds.x,bounds.x + bounds.w - w)
                    y = libtcod.random_get_int(0,bounds.y,bounds.y + bounds.h - h)
                    
                    if x + w >= len(self.map):
                        x = bounds.x 
                    if y + h >= len(self.map[0]):
                        y = bounds.y
                        
                    if x + w >= len(self.map) or y + h >= len(self.map[0]):
                        print x,",",y,"   ", w, h, "out of bounds"
                        placed = True #get rid.
                        
                    else:  
                        new = Rect(w,h,x,y)
                        if len(self.rects) > 0:
                            found = False
                            for other in self.rects:
                                if new.intersect_other(other) == True: 
                                    found = False
                                    tries += 1
                                    break
                            if not found:
                                self.rects.append(new)
                        else:
                            self.rects.append(new)
                            
                        max_w = max_w - w - 1
                        max_h = max_h - h - 1
                        
                        placed = True            
    
def flip_coin():
    if Utils.chance_roll(50):
        return True
    else:
        return False
    
    


    
    
    
    
    
    
          
        
        