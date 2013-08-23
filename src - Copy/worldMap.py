'''
Created on 16 Mar 2013

@author: Emily
'''
import libtcodpy as libtcod
import R
import entities
import json
import json_map
import random
import city
import math
import Utils
import cProfile


WATER_THRESHOLD = 100
MOUNTAIN_THRESHOLD = 200
COASTLINE_THRESHOLD = 15

# WATER_THRESHOLD = 100
# MOUNTAIN_THRESHOLD = 200
# COASTLINE_THRESHOLD = 15

TROPICS_THRESHOLD = 0 #15% #needs to be defined when the size of the map is.
TEMPERATE_THRESHOLD = 0 #upto 50%

HUMIDITY_MAX = 255
TEMP_MAX = 255  # FOR THE MAP. not celsius.

MONSTERS = json.loads(json_map.monsters)
ITEMS = ["sword","potion","shield","armour","leggings","scroll","wand","book","food"] #TODO: This stuff should be handled elsewhere. I want this file to handle world creation ONLY.

#print MONSTERS["1"]

class Tile:
    # a map tile and its properties.
    def __init__(self, x, y, blocked, block_sight = None, char = " ", cost = 10, bg = [60,100,80], fg= [255,255,255], map_tile = False):
        self.blocked = blocked
        self.x = x
        self.y = y
        self.colours = [bg[0],bg[1],bg[2],fg[0],fg[1],fg[2]]
        if bg[0] >= 255:
            bg[0] = 254
        if bg[1] >= 255:
            bg[1] = 254
        if bg[2] >= 255:
            bg[2] = 254
        self.bg = libtcod.Color(bg[0],bg[1],bg[2])
        self.fg = libtcod.Color(fg[0],fg[1],fg[2])
        self.explored = False #all tiles start unexplored
        self.char = char 
        self.cost = cost #10 for normal tile, 5 for road?
        
        if block_sight is None: 
            block_sight = blocked #by default, if a tile is blocked, it also blocks sight
        else: 
            self.block_sight = block_sight
        if map_tile is True:
            self.mapTile()
            
        self.type = ""
        
        
    def mapTile(self):
        self.POI = None
        
        self.elevation = 0 # max 255
        self.temperature = 0 # max 255
        self.humidity = 0 #max 255
        
        self.height_metres = 0
        self.temp_cel = 0 
        self.humidity_per = 0 # 0-100
        
class Rect:
    def __init__(self,w,h,x,y):  
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        
    def intersect_other(self):
        
        return False     
    
class Particle:
    def __init__(self,x,y):
        self.active = False
        self.value = 0
        self.temperature = 18 #
        self.speed = 100 # out of 100
        self.x = x
        self.y = y
        self.previous = None
        
        
    def move(self,dx,dy):
        
        if dx > 0 or dy > 0:
            if self.x + dx >= R.MAP_WIDTH:
                self.x = 0
            elif self.x + dx < 0:
                self.x = R.MAP_WIDTH -1
            else:
                self.x += dx
                 
            if self.y + dy >= R.MAP_HEIGHT: 
                self.y = 0
            elif self.y + dy < 0:
                self.y = R.MAP_HEIGHT -1 
            else:
                self.y += dy
            return True
        else:
            return False
        
            
        """
        The particle needs to deal with the moisture changes. does it do it here? or does it do it else where?
        
        I could tell the particle what function to use when it moves?
        
        FOR NOW. do it outside this class.
        
        """        
    def move_to(self,x,y):
        self.x = x
        self.y = y
        
class Particle_Map:

    
    
    def __init__(self,parent,num):
        self.parent = parent
        self.particles = []
        self.map = [[[] 
                     for y in range(self.parent.h)]
                            for x in range(self.parent.w)]
        
        #generate particle pool
        self.particles = [Particle(0,0) for n in range(num)]
        
    def add_particles(self,x,y,column=True):   
        #TODO: add in row . 
        for iy in range(len(self.map[x])):
            if len(self.particles) != 0 and len(self.particles) >= len(self.map[x]):
                
                r = len(self.particles)-1
                bleh = libtcod.random_get_int(0, 0, r)
                particle = self.particles.pop(bleh)
                particle.x = x
                particle.y = iy
                self.map[x][iy].append(particle)
            
            else:
                #make some more particles and continue!
                self.particles = [Particle(0,0) for n in range(500)]
                r = len(self.particles)-1
                bleh = libtcod.random_get_int(0, 0, r)
                particle = self.particles.pop(bleh)
                particle.x = x
                particle.y = iy
                self.map[x][iy].append(particle)  
            #y += 1 
                
    def run_simulation(self, rounds):
        
        #put first "line" of wind in.
#         for x in reversed(range(self.parent.w)):
#             #for y in range(self.parent.h):
#                 self.add_particles(x, 0)
        self.add_particles(0, 0)
        render()      
        for n in range(rounds):
            #this goes in reverse.
            if Utils.chance_roll(50):
                x_loc = libtcod.random_get_int(0, 0, R.MAP_WIDTH-1)
                self.add_particles(x_loc, 0)
            for x in reversed(range(self.parent.w)):
                for y in reversed(range(self.parent.h)):
                    self.take_turn(x, y)  
                                
            print "round ", n
            
            #self.humidity_colourise()
            
            """ THIS NEEDS REMOVING AFTER TESTING"""
            render()  
            
    def take_turn(self,x,y):
        for particle in self.map[x][y]:
            if particle is not None:                         
                if x < R.MAP_WIDTH and y < R.MAP_HEIGHT: 
                    if Utils.chance_roll(10): dy = 1
                    elif Utils.chance_roll(10): dy = -1
                    else: dy = 0
                    
                    if Utils.chance_roll(80): dx = 1
                    else: dx = 2
                        
                    MOVED = particle.move(dx,dy)
                    if MOVED:
                        removed = False
                        
                        if particle.x < R.MAP_WIDTH and particle.x >= 0 and particle.y < R.MAP_HEIGHT and particle.y >= 0:
                            #all is fine to move around.
                            if particle.x == R.MAP_WIDTH -1:
                                if Utils.chance_roll(particle.speed):
                                    particle.move_to(0,particle.y)
                                else:
                                    self.map[x][y].remove(particle)   
                                    removed = True 
                                    
                            if particle.y == R.MAP_HEIGHT-1:
                                particle.move_to(particle.x,0)
                            
                        
                        elif particle.x >= R.MAP_WIDTH  or particle.x < 0 or particle.y >= R.MAP_HEIGHT  or particle.y < 0:
                            print "the end of the map!"
                            if Utils.chance_roll(90):
                                #these shouldn't happen at all.
                                if x > R.MAP_WIDTH-1:
                                    print "somehow out of range x"
                                if y > R.MAP_HEIGHT-1:
                                    print "somehow out of range y"
                                
                                if particle.x > R.MAP_WIDTH -1:
                                    particle.move_to(0,particle.y)    
                                elif particle.x < 0:
                                    particle.move_to(R.MAP_WIDTH -1,particle.y)    
                                    
                                if particle.y > R.MAP_HEIGHT -1:
                                    particle.move_to(particle.x,0) 
                                    
                                elif particle.y < 0:
                                    particle.move_to(particle.x,R.MAP_HEIGHT-1) 
                            else:
                                #it gets taken off the map!
                                removed = True
                                self.map[x][y].remove(particle)
                                self.particles.append(particle) 
                                
                                
                        else:
                            print"the values are out of range. SOMETHING WENT WRONG."
                            
                        #NOW: do the moisture thaaaang.
                            
                    else:
                        particle.previous = self.parent.tiles[particle.x][particle.y]
                        #if not moved then assign the previous tile as the one it's in
                
                    if not removed:
                        self.moisture_exchange(particle,x,y)
                    
                if x > R.MAP_WIDTH -1 or y > R.MAP_HEIGHT -1:
                    print"the values are out of range. SOMETHING WENT WRONG."
                    pass
                
                  
                        
      
    def moisture_exchange(self,the_particle,x,y):
        #if particle.value > tile.humidity_per:
        self.map[x][y].remove(the_particle)
        particle = the_particle
        previous = self.parent.tiles[x][y]
        tile = self.parent.tiles[particle.x][particle.y]
        
        if previous.elevation < tile.elevation:
            #if the current tile is HIGHER than the previous
            n = tile.height_metres - previous.height_metres
            if previous.height_metres != 0:
                z = (n/ previous.height_metres) #incline increase
            else:
                z = 10
            if Utils.chance_roll(50):
                change = ((particle.speed/100) * z) * 10
                particle.speed += change
                
            if particle.value > tile.humidity_per:
                if Utils.chance_roll(tile.humidity_per + tile.humidity_per*z):
                    particle.value -= tile.humidity_per*0.15  
                    if tile.type != "water":
                        tile.humidity_per += tile.humidity_per*0.1 #%5 is lost in translation.
            
            elif particle.value < tile.humidity_per:
                if Utils.chance_roll(tile.humidity_per + tile.humidity_per*z):
                    particle.value += (tile.humidity_per*0.05) # %5 is lost in translation.
                    if tile.type != "water":
                        tile.humidity_per -= tile.humidity_per*0.1 
            else:
                if Utils.chance_roll(50):
                    particle.value -= tile.humidity_per*0.1
                    if tile.type != "water":
                        tile.humidity_per += (tile.humidity_per*0.07) # %5 is lost in translation.
                else:
                    particle.value += tile.humidity_per*0.07  # %5 is lost in translation.
                    if tile.type != "water":
                        tile.humidity_per -= tile.humidity_per*0.1 
                    
        elif previous.elevation > tile.elevation: 
            #the current tile is LOWER than the previous.
            n = previous.height_metres - tile.height_metres
            if tile.height_metres != 0:
                z = n/ tile.height_metres
            else:
                z = 10
                
            if Utils.chance_roll(50):
                change = ((particle.speed/100) * z) * 10
                particle.speed += change
            
            if particle.value > tile.humidity_per:
                if Utils.chance_roll(tile.humidity_per):
                    if tile.type != "water":
                        tile.humidity_per += particle.value*0.05 
                    particle.value -= particle.value*0.1
            
            elif particle.value < tile.humidity_per:
                if Utils.chance_roll(tile.humidity_per + z):
                    particle.value += tile.humidity_per*0.14
                    if tile.type != "water":
                        tile.humidity_per -= tile.humidity_per*0.1
            else:
                if Utils.chance_roll(50):
                    particle.value -= tile.humidity_per*0.1
                    if tile.type != "water":
                        tile.humidity_per -= tile.humidity_per*0.05 
                else:
                    particle.value -= tile.humidity_per*0.1
                    if tile.type != "water":
                        tile.humidity_per += tile.humidity_per*0.05
            
        else:
            #the height is the same? 
            
            if particle.value > tile.humidity_per:
                if Utils.chance_roll(tile.humidity_per):
                    particle.value += tile.humidity_per*0.1
                    if tile.type != "water":
                        tile.humidity_per -= tile.humidity_per*0.1 
            
            elif particle.value < tile.humidity_per:
                if Utils.chance_roll(tile.humidity_per):
                    particle.value -= tile.humidity_per*0.1
                    if tile.type != "water":
                        tile.humidity_per += tile.humidity_per*0.1 
            else:
                if Utils.chance_roll(50):
                    particle.value -= tile.humidity_per*0.1
                    
        """check speed values are within limits!"""
        if particle.speed < 1:
            #particle has *died" so as it is already removed, just add it into the particles list.
            self.particles.append(particle)
            
        else:
            if Utils.chance_roll(5):
                #chsnce to disappear.
                particle.value = 0
                self.particles.append(particle)
            else:    
            
                """move to the correct tile in the map lists."""
                tile.humidity = HUMIDITY_MAX * (tile.humidity_per/100)
                self.map[particle.x][particle.y].append(particle)
                self.parent.tiles[x][y] = previous
                self.parent.tiles[particle.x][particle.y] = tile
        
        
        
    def humidity_colourise(self):
        
        """Finally, change the humidty colour value"""
        self.parent.normalise_humidity()
        
        for x in range(len(self.parent.tiles)):
            for y in range(len(self.parent.tiles[x])):
                tile = self.parent.tiles[x][y]
                if tile.type != "water":
                    tile.humidity = 255 * (tile.humidity_per/100)
                
        #end particle map.
        
class Map:
    def __init__(self, w, h):
        global TROPICS_THRESHOLD, TEMPERATE_THRESHOLD, TAIGA_THRESHOLD
        
        self.w = w
        self.h = h
        
        self.equator = h/2
        TROPICS_THRESHOLD = (self.equator/2)/3
        TEMPERATE_THRESHOLD = self.equator/2
        TAIGA_THRESHOLD = self.equator - self.equator*0.1
        self.tiles = [[ Tile(ix,iy, False, map_tile=True)
            for iy in range(h) ]
                for ix in range(w)]
        x,y = 0,0
        self.traffic = [[0
                         for y in range(h)]
                            for x in range(w)]
        #this holds the *colour* value of the tiles temps.
        self.temperature_map = [[0
                         for y in range(h)]
                            for x in range(w)]
        self.moisture_map = [[0
                         for y in range(h)]
                            for x in range(w)]
        
        self.hm = libtcod.heightmap_new(self.w, self.h)
        self.hm2 = libtcod.heightmap_new(self.w, self.h)
        self.hm3 = libtcod.heightmap_new(self.w, self.h)
        
        self.generate_land(self.hm)
        self.generate_land(self.hm2)
        self.generate_land(self.hm3)
        
        libtcod.noise_set_type(self.noise, libtcod.NOISE_SIMPLEX)
        self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        #libtcod.heightmap_add_fbm(self.hm3, self.noise, 1, 1, 0, 0, 8, 0.8, 0.5)
        #self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        #libtcod.heightmap_add_fbm(self.hm3, self.noise, 1, 1, 0, 0, 8, 0.8, 0.5)
        #self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        #libtcod.heightmap_add_fbm(self.hm3, self.noise, 1, 1, 0, 0, 8, 0.8, 0.5)
        self.multiply_noise()
        self.multiply_noise()
        libtcod.heightmap_normalize(self.hm, 0, 255)
        #libtcod.heightmap_normalize(self.hm2, 0, 255)
        #libtcod.heightmap_normalize(self.hm3, 0, 255)
        #libtcod.heightmap_rain_erosion(self.hm, (self.w + self.h)*4, 0.5, 0.1, None)
        
        self.add_noise()
        self.turn_to_tiles()
        self.determine_temperatures()
        self.normalise_temperatures()
        self.wind_gen = Particle_Map(self,1500)
        self.generate_mini_map(10)
        self.cities = []
        self.dungeons = []
        self.generate_city(libtcod.random_get_int(0, 4, 10))
        self.generate_dungeons(10)
        
        
    def generate_city(self, num):
        
        for n in range(num):
            placed = False
            while not placed:
                x = libtcod.random_get_int(0, 1, self.w-1)
                y = libtcod.random_get_int(0, 1, self.h-1)
                tile = self.tiles[x][y]
                if tile.POI is None and tile.blocked is not True:
                    tempCity = city.City(x,y)
                    self.cities.append(tempCity)
                    self.tiles[x][y].POI = tempCity
                    placed = True
                    print "City succeeded", x, y, tempCity.name
                else:
                    print "failed", x, y
                    
    def generate_dungeons(self, num):
        for n in range(num):
            placed = False
            while not placed:
                x = libtcod.random_get_int(0, 1, self.w-1)
                y = libtcod.random_get_int(0, 1, self.h-1)
                tile = self.tiles[x][y]
                if tile.POI is None and tile.blocked is not True:
                    temp = Dungeon(x,y)
                    self.dungeons.append(temp)
                    self.tiles[x][y].POI = temp
                    placed = True
                    print "Dungeon succeeded", x, y, temp.name
                else:
                    print "failed", x, y
           
    def connect_cities(self):
        
        pather = entities.Pather()
        city_one = self.cities[libtcod.random_get_int(0, 0, len(self.cities) - 1)]
        city_two = self.cities[libtcod.random_get_int(0, 0, len(self.cities) - 1)]
        
        while city_one == city_two and len(self.cities) > 1:
            city_two = self.cities[libtcod.random_get_int(0, 0, len(self.cities) - 1)]
        
        path = pather.find_path((city_one.x,city_one.y), (city_two.x,city_two.y), self.tiles)
            
        while path == None:
            path = pather.find_path((city_one.x,city_one.y), (city_two.x,city_two.y), self.tiles)
            
            if path == None:
                city_one = self.cities[libtcod.random_get_int(0, 0, len(self.cities) - 1)]
                city_two = self.cities[libtcod.random_get_int(0, 0, len(self.cities) - 1)]
                
                while city_one == city_two and len(self.cities) > 1:
                    city_two = self.cities[libtcod.random_get_int(0, 0, len(self.cities) - 1)]
        
        for node in path:
            self.tiles[node[0]][node[1]].bg = libtcod.Color(200,200,10)
            self.tiles[node[0]][node[1]].cost = 5
        
        print "........................connected ", city_one.name, " and ", city_two.name
    
    def add_foot_traffic(self,x,y):
        
        self.traffic[x][y] += 1
        
    def get_foot_traffic(self,x,y):
        
        return self.traffic[x][y]
        
    def sort_for_highest_traffic(self, highest = True):
        highest = [0.0,0,0]
        lowest = [99999999,0,0]
        for x in range(len(self.traffic)):
            for y in range(len(self.traffic[x])):
                if self.traffic[x][y][0] > highest[0]:
                    highest = [self.traffic[x][y][0],x,y]
                elif self.traffic[x][y][0] < lowest[0]:
                    lowest = [self.traffic[x][y][0],x,y]
        
        if highest:           
            return highest #can return lowest too.
        else:
            return lowest
        
    def generate_mini_map(self, zone = 10,  hm = None):
        
        if hm == None:
            hm = self.hm
            
        if (self.w % zone) > 0:
            print "doesn't smoothly fit - W"
        if (self.h % zone) > 0:
            print "doesn't smoothly fit - H"
        
        self.mini_map = [] 
        self.mini_map = [[None
                         for y in range(int(self.h/zone))]
                            for x in range(int(self.w/zone))]
            
        
        for a in range(len(self.tiles)/zone):
            for b in range(len(self.tiles[a])/zone):
                cell_x = 0
                cell_y = 0
                tiles = [[0,[]],[0,[]]]
                x = a * zone
                y = b * zone 
                for cell_x in range(zone):
                    if x + cell_x > len(self.tiles)-1:
                        break
                    for cell_y in range(zone):
                        if y + cell_y > len(self.tiles[cell_x])-1:
                            break
                        #TODO: put in catches for the "end" bits where there is less tiles left than the "zone".
                        value = int(libtcod.heightmap_get_value(hm, x + cell_x, y + cell_y))
                        if value > WATER_THRESHOLD:
                            tiles[0][0] += 1
                            tiles[0][1].append(value)
                            
                        else:
                            tiles[1][0] += 1
                            tiles[1][1].append(value)
                            
                if tiles[0] > tiles[1]:
                    #make land
                    sum_ = sum(num for num in tiles[0][1])
                    value = sum_ / len(tiles[0][1])
                    self.mini_map[a][b] = Tile(cell_x,cell_y, False, map_tile=True, bg=[10,value,10])
                elif tiles[1] > tiles[0]:
                    #make water
                    sum_ = sum(num for num in tiles[1][1])
                    value = sum_ / len(tiles[1][1])
                    self.mini_map[a][b] = Tile(cell_x,cell_y, True, map_tile=True, bg=[10,10,value])
                else:
                    #flip for either.
                    flip = libtcod.random_get_int(0, 0, 1)
                    if flip == 1:
                        #water
                        sum_ = sum(num for num in tiles[1][1])
                        value = sum_ / len(tiles[1][1])
                        self.mini_map[a][b] = Tile(cell_x,cell_y, True, map_tile=True, bg=[10,10,value])
                    if flip == 0:
                        #land
                        sum_ = sum(num for num in tiles[0][1])
                        value = sum_ / len(tiles[0][1])
                        self.mini_map[a][b] = Tile(cell_x,cell_y, False, map_tile=True, bg=[10,value,10])
        
    def generate_land(self,hm):
        
        print hm.w, hm.h
        #self.noise = perlin_noise.PerlinNoiseGenerator()
        #self.noise.generate_noise(self.w, self.h, 1, 16)
        #print str(self.noise.noise[1][1])
        self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        libtcod.heightmap_add_fbm(hm, self.noise, 1, 1, 0, 0, 8, 0.5, 0.8)
        print "scale", str(libtcod.heightmap_get_value(hm, 1, 1))
        self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        libtcod.noise_set_type(self.noise, libtcod.NOISE_PERLIN)
        libtcod.heightmap_scale_fbm(hm, self.noise, 1, 1, 0, 0, 8, 0.5, 0.8)
        
#        self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
#        libtcod.heightmap_add_fbm(hm, self.noise, 1, 1, 0, 0, 8, 0.8, 0.5)
#        
        libtcod.heightmap_normalize(hm, 0, 255)
        print "normalized", str(libtcod.heightmap_get_value(hm, 1, 1))
        
        return hm

    
    def add_noise(self):
        libtcod.heightmap_normalize(self.hm, 0, 1)
        self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        libtcod.noise_set_type(self.noise, libtcod.NOISE_PERLIN)
        libtcod.heightmap_add_fbm(self.hm, self.noise, 1, 1, 1, 1, 8, 0.5, 0.5)
        libtcod.heightmap_normalize(self.hm, 0, 255)
        
    def multiply_noise(self):
        self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        libtcod.noise_set_type(self.noise, libtcod.NOISE_PERLIN)
        libtcod.heightmap_scale_fbm(self.hm, self.noise, 1, 1, 1, 1, 16, 0.5, 0.5)
        #libtcod.heightmap_normalize(self.hm, 0, 255)
    
    def add_hill(self,x,y):
        r = 5
        xh = self.w
        yh = self.h
        
        one = (x - xh )*(x - xh )
        two = (y - yh)*(y - yh)
        
        hill_height = ((r*r) + one + two)/4
        
        if hill_height > 0:
            libtcod.heightmap_add_hill(self.hm, x, y, 10, 20)
            libtcod.heightmap_normalize(self.hm, 0, 255)
            
    def turn_to_tiles(self):
        self.tiles = []
        
        self.tiles = [[ Tile(ix,iy, False, map_tile=True)
            for iy in range(self.h) ]
                for ix in range(self.w)]
        
        for cell_x in range(self.w):
            for cell_y in range(self.h):
                value = int(libtcod.heightmap_get_value(self.hm, cell_x, cell_y))
                
                if value > MOUNTAIN_THRESHOLD: #mountain
                    mountain = 50 + (value - MOUNTAIN_THRESHOLD)
                    shift = libtcod.random_get_int(0,-5,5)
                    tote = mountain + shift 
                    if tote > 255:
                        tote = 255
                    if tote < 0:
                        tote = 0
                    #self.tiles[cell_x][cell_y] = Tile(cell_x,cell_y, False, map_tile=True, bg=[40 + mountain, value - mountain, 40 + mountain], cost = 20)
                    self.tiles[cell_x][cell_y] = Tile(cell_x,cell_y, False, map_tile=True, bg=[tote, tote, tote], cost = 40)
                    self.tiles[cell_x][cell_y].elevation = value
                    self.tiles[cell_x][cell_y].humidity = libtcod.random_get_int(0,0,5)
                    self.tiles[cell_x][cell_y].humidity_per = self.tiles[cell_x][cell_y].humidity/255*100
                    self.tiles[cell_x][cell_y].type = "mountain"
                    
                elif value > WATER_THRESHOLD + COASTLINE_THRESHOLD: #grass
                    ran_1 = 255- value+ libtcod.random_get_int(0,-5,5)
                    if ran_1 > 255:
                        ran_1 = 255
                    self.tiles[cell_x][cell_y] = Tile(cell_x,cell_y, False, map_tile=True, bg=[10,ran_1,10 + libtcod.random_get_int(0,-5,5)], cost = 15)
                    self.tiles[cell_x][cell_y].elevation = value
                    self.tiles[cell_x][cell_y].humidity = libtcod.random_get_int(0,10,100)
                    self.tiles[cell_x][cell_y].humidity_per = self.tiles[cell_x][cell_y].humidity/255*100
                    
                elif value > WATER_THRESHOLD: #coast
                    test = int(math.sqrt(value))
                    #test = test ** 3
                    self.tiles[cell_x][cell_y] = Tile(cell_x,cell_y, False, map_tile=True, bg=[value+ libtcod.random_get_int(0,-5,5),value-test+ libtcod.random_get_int(0,-5,5),test])
                    self.tiles[cell_x][cell_y].elevation = value
                    self.tiles[cell_x][cell_y].humidity = 25.5
                    self.tiles[cell_x][cell_y].humidity_per = 10.0
                    
                else: #water
                    tote = value+ libtcod.random_get_int(0,-5,5)
                    if tote > 255:
                        tote = 255
                    if tote < 0:
                        tote = 0
                    self.tiles[cell_x][cell_y] = Tile(cell_x,cell_y, True, map_tile=True, bg=[10,10,tote])
                    self.tiles[cell_x][cell_y].elevation = value
                    self.tiles[cell_x][cell_y].humidity = 255
                    self.tiles[cell_x][cell_y].humidity_per = 100.0
                    self.tiles[cell_x][cell_y].type = "water"
                    
                    
    def get_temperature(self,x,y): 
        return self.temperature_map[x][y]  
    
    def determine_temperatures(self):
        
        for x in range(self.w):
            for y in range(self.h):
                altitude = self.tiles[x][y].elevation
                if altitude > WATER_THRESHOLD:
                    altitude -= WATER_THRESHOLD
                    multiplier = math.e**(0.0207345*altitude)
                    height_in_metres = 282.33 * multiplier
                    self.tiles[x][y].height_metres = height_in_metres
                    
                    if y <= self.equator:
                        distance_from_equator = float(self.equator - y) 
                    elif y > self.equator:
                        distance_from_equator = float(y - self.equator) 
                    #this needs to be softer. too "bandy" at the moment. somehow do this ona  scale rather than BAM you're now x.
#                     if distance_from_equator <= TROPICS_THRESHOLD:
#                         temp = 30 + libtcod.random_get_int(0,-3,3)
#                     elif distance_from_equator <= TEMPERATE_THRESHOLD:
#                         temp = 20 + libtcod.random_get_int(0,-3,3)
#                     elif distance_from_equator <= TAIGA_THRESHOLD:
#                         temp = 5 + libtcod.random_get_int(0,-3,3)
#                     else: #polar
#                         temp = -10 + libtcod.random_get_int(0,-5,5)
                    #start at equator temp
                    temp = 30
                    #percent of total possible distance
                    max_ = float(self.equator)
                    pre = distance_from_equator / max_
                    if y == 10:
                        print " "
                    if distance_from_equator == max_:
                        pre = 1
                    percent = pre * 100
                    #for a drop of upto 30.
                    #temp_drop = (0.002*percent)**2 + 0.1*percent - 3.92896*10**-14
                    #for a drop of upto 60.
                    temp_drop = 0.006*percent**2 + 5.71976*10**-16 * percent-5.89344*10**-14
                    temp = temp - math.ceil(temp_drop)    
                    
                    #Now for altitude effects.
                    #if height_in_metres % 500 < height_in_metres:
                    degree_shift = (height_in_metres / 500) * 3
#                     else:
#                         degree_shift = - 1
                    temp = temp - degree_shift
                    self.tiles[x][y].temperature = temp
                    self.tiles[x][y].temp_cel = temp
                    
                else:
                    altitude = WATER_THRESHOLD - altitude
                    
                    multiplier = math.e**(0.0207345*altitude)
                    depth_in_metres = 282.33 * multiplier
                    self.tiles[x][y].height_metres = -depth_in_metres
                    
                    if y <= self.equator:
                        distance_from_equator = float(self.equator - y) 
                    elif y > self.equator:
                        distance_from_equator = float(y - self.equator) 
                    #start at equator temp
                    temp = 5
                    #percent of total possible distance
                    max_ = float(self.equator)
                    pre = distance_from_equator / max_
                    if y == 10:
                        print " "
                    if distance_from_equator == max_:
                        pre = 1
                    percent = pre * 100
                    #for a drop of upto 30.
                    #temp_drop = (0.002*percent)**2 + 0.1*percent - 3.92896*10**-14
                    #for a drop of upto 60.
                    temp_drop = 0.006*percent**2 + 5.71976*10**-16 * percent-5.89344*10**-14
                    temp = temp - math.ceil(temp_drop)    
                    
                    #Now for altitude effects.
                    #if height_in_metres % 500 < height_in_metres:
                    degree_shift = (depth_in_metres / 500) * 5
#                     else:
#                         degree_shift = - 1
                    temp = temp - degree_shift
                    self.tiles[x][y].temperature = temp
                    self.tiles[x][y].temp_cel = temp
                    
    def normalise_temperatures(self):
        
        largest = 0
        smallest = 999999 
        #find the high and low temps.
        for x in range(self.w):
            for y in range(self.h):
                self.tiles[x][y].temperature += 100
                if self.tiles[x][y].temperature > largest:
                    largest = self.tiles[x][y].temperature 
                if self.tiles[x][y].temperature < smallest:
                    smallest = self.tiles[x][y].temperature 
        #now to normalise.
        for x in range(self.w):
            for y in range(self.h):
                percent = (self.tiles[x][y].temperature - smallest) / (largest - smallest)
                self.temperature_map[x][y] = math.ceil(percent * TEMP_MAX)
                self.tiles[x][y].temperature = self.temperature_map[x][y]
    def normalise_humidity(self):
        
        largest = 0
        smallest = 999999 
        #find the high and low temps.
        for x in range(self.w):
            for y in range(self.h):
                if self.tiles[x][y].humidity_per > largest:
                    largest = self.tiles[x][y].humidity_per
                if self.tiles[x][y].humidity_per < smallest:
                    smallest = self.tiles[x][y].humidity_per
        #now to normalise.
        for x in range(self.w):
            for y in range(self.h):
                percent = (self.tiles[x][y].humidity_per - smallest) / (largest - smallest)
                self.tiles[x][y].humidity = math.ceil(percent * TEMP_MAX)
                self.tiles[x][y].humidity_per = math.ceil(self.tiles[x][y].humidity_per)


   
                
                        
class POI:             
    def __init__(self,x,y, colour = None, char = "X"):
        self.x = x
        self.y = y
        self.colour = colour
        if self.colour == None:
            self.colour = libtcod.Color(libtcod.random_get_int(0,0,255),libtcod.random_get_int(0,0,255),libtcod.random_get_int(0,0,255))
        self.char = char     
        self.name = "named"
                           
class Dungeon(POI):
    def __init__(self,x,y, level=1):
        POI.__init__(self,x,y,libtcod.Color(libtcod.random_get_int(0,50,255),libtcod.random_get_int(0,0,100),libtcod.random_get_int(0,100,150)), "#")
        self.level = level
        self.exp = 0           
        self.floors = []     
        self.generate_floors()
        print "dungeon!"
    
    def pass_turn(self):
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

def place_on_land():
    placed = False
    while not placed:
        x = libtcod.random_get_int(0, 0, R.world.w-1)
        y = libtcod.random_get_int(0, 0, R.world.h-1)
        tile = R.world.tiles[x][y]
        if tile.POI is None and tile.blocked is not True:
            return x,y
            
def render():
    
    for y in range(R.SCREEN_HEIGHT): 
        for x in range(R.SCREEN_WIDTH):
#             r = int(libtcod.heightmap_get_value(map_.hm, x, y))
#             g = int(libtcod.heightmap_get_value(map_.hm, x, y))
            if x < R.MAP_WIDTH and y < R.MAP_HEIGHT:
                b = int(map_.tiles[x][y].humidity)
                colour = libtcod.Color(0,0,int(b))
                libtcod.console_set_char_background(con, x, y, colour)
                
                if len(map_.wind_gen.map[x][y]) > 0:
                    libtcod.console_set_char(con,x,y,".")
                    libtcod.console_set_char_foreground(con, x, y, libtcod.white)
                else:
                    libtcod.console_set_char_foreground(con, x, y, libtcod.black)
                    libtcod.console_set_char(con, x, y, " ")
                    
            if x >= R.MAP_WIDTH and y < R.MAP_HEIGHT:
                ax = x - R.MAP_WIDTH 
                ay = y
                
                b = int(map_.tiles[ax][y].elevation)
                c = b
                if map_.tiles[ax][ay].type != "water":
                    c = 10
                colour = libtcod.Color(int(b),int(c),int(b))
                libtcod.console_set_char_background(con, x, y, colour)
                    
            if x >= R.MAP_WIDTH and y >= R.MAP_HEIGHT:
                ax = x - R.MAP_WIDTH
                ay = y - R.MAP_HEIGHT 
                b = int(map_.tiles[ax][ay].temperature)
                colour = libtcod.Color(int(b),int(b),int(b))
                libtcod.console_set_char_background(con, x, y, colour)
                    
    libtcod.console_blit(con, 0, 0, R.SCREEN_WIDTH, R.SCREEN_HEIGHT, 0, 0, 0)
    
    libtcod.console_flush()
           



def handle_mouse():
    
    mouse = libtcod.mouse_get_status()
    
    (x, y) = (mouse.cx, mouse.cy)

    if x > R.MAP_WIDTH - 1:
        x = R.MAP_WIDTH - 1
    if y > R.MAP_HEIGHT -  1:
        y = R.MAP_HEIGHT - 1
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    
    if x < R.MAP_WIDTH and y < R.MAP_HEIGHT:
        libtcod.console_set_char_foreground(con, x, y, libtcod.orange)
        libtcod.console_set_char(con, x, y, "#")
        
        ax = x + R.MAP_WIDTH 
        ay = y
        
        
        libtcod.console_set_char_foreground(con, ax, ay, libtcod.orange)
        libtcod.console_set_char(con, ax, ay, "#")  
        
        ax = x + R.MAP_WIDTH 
        ay = y + R.MAP_HEIGHT 
        
        libtcod.console_set_char_foreground(con, ax, ay, libtcod.orange)
        libtcod.console_set_char(con, ax, ay, "#")    
    
       
#     if mouse.lbutton_pressed:
#         print "hill"
#         map_.add_hill(x,y)
#         
#     if mouse.rbutton_pressed:
#         print "add"
#         map_.add_noise()
        
def handle_keys():
    if key.vk == libtcod.KEY_ESCAPE:
        return "exit"  #exit game
    
    if key.vk == libtcod.KEY_SPACE:
        pass
        #TODO: write function to initiate biome analysis.
    
#     if key.vk == libtcod.KEY_SPACE:
#         print "new"
#         map_.__init__(70,40)
#     if key.vk == libtcod.KEY_KPENTER:
#         print "multiply"
#         #map_.multiply_noise()


def main():
    global key, mouse, map_, con
    
    R.SCREEN_WIDTH = 100
    R.SCREEN_HEIGHT = 80
    libtcod.console_set_custom_font("data\ont_big.png",libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(R.SCREEN_WIDTH, R.SCREEN_HEIGHT, "Trader-RL", False)
    libtcod.sys_set_fps(R.LIMIT_FPS)        
    con = libtcod.console_new(R.SCREEN_WIDTH, R.SCREEN_HEIGHT)     
    
    
    map_ = Map(R.MAP_WIDTH,R.MAP_HEIGHT)        
    map_.wind_gen.run_simulation(500)
    
    mouse = libtcod.Mouse()
    key = libtcod.Key()
    
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)
        render()        
            
        
        player_action = handle_keys()
        if player_action == "exit":    
            break
        
        handle_mouse()
        
        
#cProfile.run('main()')  
main()     
        
        
#buh = Dungeon(0,0,1)       
        
        
    
    
        