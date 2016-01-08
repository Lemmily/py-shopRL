'''
Created on 16 Mar 2013

@author: Emily
'''
import json
import math

import R
import city
import dungeon
import json_map
import pathfinding
import utils
from src import libtcodpy as libtcod

SAND_HEIGHT = 0.14
grassHeight = 0.16
rockHeight = 0.655
snowHeight = 0.905

WATER_THRESHOLD = int(255 * SAND_HEIGHT)
MOUNTAIN_THRESHOLD = int(255 * rockHeight)
SNOW_THRESHOLD = int(255 * snowHeight)
GRASS_THRESHOLD = int(255 * grassHeight)

PATH_COST = 1.0
GRASS_COST = 1.8
COAST_COST = 2.5
MOUNTAIN_COST = 3.5
WATER_COST = 200.0  # potential for shippy ships later?

# WATER_THRESHOLD = 100
# MOUNTAIN_THRESHOLD = 200
# COASTLINE_THRESHOLD = 15

TROPICS_THRESHOLD = 0  # 15% #needs to be defined when the size of the map is.
TEMPERATE_THRESHOLD = 0  # upto 50%
EVAP_THRESHOLD = 20  # after 20C evaporation occurs!

HUMIDITY_MAX = 255
TEMP_MAX = 255  # FOR THE MAP. not celsius. in colour hex.
MONSTERS = json.loads(json_map.monsters)
ITEMS = ["sword", "potion", "shield", "armour", "leggings", "scroll", "wand", "book",
         "food"]  # TODO: This stuff should be handled elsewhere. I want this file to handle world creation ONLY.

# print MONSTERS["1"]

class Tile:
    # a map tile and its properties.
    def __init__(self, x, y, blocked, block_sight=False, char=" ", cost=5.0, bg=(0, 100, 80), fg=(255, 255, 255),
                 map_tile=False):

        self.x = x
        self.y = y
        self.colours = [bg[0], bg[1], bg[2], fg[0], fg[1], fg[2]]
        if bg[0] >= 255:
            bg[0] = 254
        if bg[1] >= 255:
            bg[1] = 254
        if bg[2] >= 255:
            bg[2] = 254
        self.bg = libtcod.Color(bg[0], bg[1], bg[2])
        self.fg = libtcod.Color(fg[0], fg[1], fg[2])
        self.explored = False  #:all tiles start unexplored
        self.char = char
        self.cost = cost  #:10 for normal tile, 5 for road?

        self.blocked = blocked
        self.block_sight = block_sight

        if map_tile is True:
            self.mapTile()

        self.type = ""


    def mapTile(self):
        self.POI = None
        self.continent = -1  # used for pathfining. if on the same "continent", can reach.

        self.elevation = 0  #: max 255
        self.temperature = 0  #: max 255
        self.humidity = 0  #:max 255

        self.height_metres = 0  #:Also used for DEPTH. which is a negative value.
        self.temp_cel = 0  #: temp in celsius
        self.humidity_per = 0  #: precentage humidity.


class Rect:
    def __init__(self, w, h, x, y):
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


class Particle:
    def __init__(self, x, y, max_):
        self.active = False
        self.value = 0
        self.temperature = 18  #
        self.speed = 100  # out of 100
        self.life = 1000  #:life of the particle.
        self.x = x
        self.y = y
        self.previous = None
        self.max_value = max_


    def move(self, dx, dy):

        if dx > 0 or dy > 0:
            if self.x + dx >= R.MAP_WIDTH:
                self.x = 0
            elif self.x + dx < 0:
                self.x = R.MAP_WIDTH - 1
            else:
                self.x += dx

            if self.y + dy >= R.MAP_HEIGHT:
                self.y = 0
            elif self.y + dy < 0:
                self.y = R.MAP_HEIGHT - 1
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

    def move_to(self, x, y):
        self.x = x
        self.y = y


    def is_max_value(self):
        if self.value >= self.max_value:
            self.value = self.max_value
            return True
        else:
            return False


class Particle_Map:
    def __init__(self, parent, num):
        self.parent = parent
        self.particles = []
        self.map = [[[]
                        for y in range(self.parent.h)]
                    for x in range(self.parent.w)]

        # generate particle pool
        self.particles = [Particle(0, 0, 100) for n in range(num)]

    def add_particles(self, x, y, column=True):
        # TODO: add in row .
        for iy in range(len(self.map[x])):
            if len(self.particles) != 0 and len(self.particles) >= len(self.map[x]):

                r = len(self.particles) - 1
                bleh = libtcod.random_get_int(0, 0, r)
                particle = self.particles.pop(bleh)
                particle.x = x
                particle.y = iy
                self.map[x][iy].append(particle)

            else:
                #make some more particles and continue!
                self.particles = [Particle(0, 0) for n in range(500)]
                r = len(self.particles) - 1
                bleh = libtcod.random_get_int(0, 0, r)
                particle = self.particles.pop(bleh)
                particle.x = x
                particle.y = iy
                self.map[x][iy].append(particle)
                #y += 1

    def run_simulation(self, rounds):

        # put first "line" of wind particles in.
        self.add_particles(0, 0)
        render()
        for n in range(rounds):
            #this goes in reverse.
            if utils.chance_roll(50):
                #x_loc = libtcod.random_get_int(0, 0, R.MAP_WIDTH-1)
                self.add_particles(0, 0)
            for x in reversed(range(self.parent.w)):
                for y in reversed(range(self.parent.h)):
                    self.take_turn(x, y)

            print "round ", n

            #self.humidity_colourise()

            """ THIS NEEDS REMOVING AFTER TESTING"""
            render()

    def take_turn(self, x, y):
        for particle in self.map[x][y]:
            if particle is not None:
                if x < R.MAP_WIDTH and y < R.MAP_HEIGHT:
                    if utils.chance_roll(10):
                        dy = 1
                    elif utils.chance_roll(10):
                        dy = -1
                    else:
                        dy = 0

                    if utils.chance_roll(80):
                        dx = 1
                    else:
                        dx = 2

                    MOVED = particle.move(dx, dy)
                    if MOVED:
                        removed = False

                        if particle.x < R.MAP_WIDTH and particle.x >= 0 and particle.y < R.MAP_HEIGHT and particle.y >= 0:
                            # all is fine to move around.
                            if particle.x == R.MAP_WIDTH - 1:
                                if utils.chance_roll(particle.speed):
                                    particle.move_to(0, particle.y)
                                else:
                                    self.map[x][y].remove(particle)
                                    removed = True

                            if particle.y == R.MAP_HEIGHT - 1:
                                particle.move_to(particle.x, 0)


                        elif particle.x >= R.MAP_WIDTH or particle.x < 0 or particle.y >= R.MAP_HEIGHT or particle.y < 0:
                            print "the end of the map!"
                            if utils.chance_roll(90):
                                # these shouldn't happen at all.
                                if x > R.MAP_WIDTH - 1:
                                    print "somehow out of range x"
                                if y > R.MAP_HEIGHT - 1:
                                    print "somehow out of range y"

                                if particle.x > R.MAP_WIDTH - 1:
                                    particle.move_to(0, particle.y)
                                elif particle.x < 0:
                                    particle.move_to(R.MAP_WIDTH - 1, particle.y)

                                if particle.y > R.MAP_HEIGHT - 1:
                                    particle.move_to(particle.x, 0)

                                elif particle.y < 0:
                                    particle.move_to(particle.x, R.MAP_HEIGHT - 1)
                            else:
                                # it gets taken off the map!
                                removed = True
                                self.map[x][y].remove(particle)
                                self.particles.append(particle)


                        else:
                            print"the values are out of range. SOMETHING WENT WRONG."

                            # NOW: do the moisture thaaaang.

                    else:
                        particle.previous = self.parent.tiles[particle.x][particle.y]
                        # if not moved then assign the previous tile as the one it's in

                    if not removed:
                        self.moisture_exchange(particle, x, y)

                if x > R.MAP_WIDTH - 1 or y > R.MAP_HEIGHT - 1:
                    print"the values are out of range. SOMETHING WENT WRONG."
                    pass


    def moisture_exchange(self, the_particle, x, y):
        # if particle.value > tile.humidity_per:
        self.map[x][y].remove(the_particle)
        particle = the_particle
        previous = self.parent.tiles[x][y]
        #particle = previous
        tile = self.parent.tiles[particle.x][particle.y]

        if previous.elevation < tile.elevation and (tile.type != "water" and previous.type != "water"):
            #if the current tile is HIGHER than the previous
            target = tile.height_metres
            last = previous.height_metres
            if previous.height_metres < 0:
                last = -previous.height_metres
            if tile.height_metres < 0:
                target = -previous.height_metres

            n = target - last
            if last != 0:
                z = (n / last)  #incline increase
            else:
                z = 10
            if utils.chance_roll(50):
                change = ((particle.speed / 100) * z) * 10
                particle.speed += change

            height_mod = z * 100
            height_mod = int(height_mod)
            height_mod = float(height_mod)
            height_mod = height_mod / 100

            if particle.value > tile.humidity_per:
                if utils.chance_roll(tile.humidity_per + tile.humidity_per * z):
                    dif = particle.value
                    particle.value -= dif * 0.15
                    if tile.type != "water":
                        tile.humidity_per += dif * 0.1  #%5 is lost in translation.

            elif particle.value < tile.humidity_per:
                if utils.chance_roll(tile.humidity_per + tile.humidity_per * z):
                    dif = tile.humidity_per
                    particle.value += dif * 0.05
                    if tile.type != "water":
                        tile.humidity_per -= dif * 0.1  #%5 is lost in translation.
            else:
                if utils.chance_roll(50):
                    particle.value -= tile.humidity_per * 0.1
                    if tile.type != "water":
                        tile.humidity_per += (tile.humidity_per * 0.07)  # %5 is lost in translation.
                else:
                    particle.value += tile.humidity_per * 0.07  # %5 is lost in translation.
                    if tile.type != "water":
                        tile.humidity_per -= tile.humidity_per * 0.1

        elif previous.elevation > tile.elevation and (tile.type != "water" and previous.type != "water"):
            #the current tile is LOWER than the previous.
            n = previous.height_metres - tile.height_metres
            if tile.height_metres != 0:
                z = n / tile.height_metres
            else:
                z = 10

            if utils.chance_roll(50):
                change = ((particle.speed / 100) * z) * 10
                particle.speed += change

            if particle.value > tile.humidity_per:
                if utils.chance_roll(tile.humidity_per):
                    if tile.type != "water":
                        tile.humidity_per += particle.value * 0.05
                    particle.value -= particle.value * 0.1

            elif particle.value < tile.humidity_per:
                if utils.chance_roll(tile.humidity_per + z):
                    particle.value += tile.humidity_per * 0.14
                    if tile.type != "water":
                        tile.humidity_per -= tile.humidity_per * 0.1
            else:
                if utils.chance_roll(50):
                    particle.value -= tile.humidity_per * 0.1
                    if tile.type != "water":
                        tile.humidity_per -= tile.humidity_per * 0.05
                else:
                    particle.value -= tile.humidity_per * 0.1
                    if tile.type != "water":
                        tile.humidity_per += tile.humidity_per * 0.05

        else:
            #the height is the same? 
            if particle.value > tile.humidity_per:
                if utils.chance_roll(tile.humidity_per):
                    particle.value += tile.humidity_per * 0.1
                    if tile.type != "water":
                        tile.humidity_per -= tile.humidity_per * 0.1

            elif particle.value < tile.humidity_per:
                if utils.chance_roll(tile.humidity_per):
                    particle.value -= tile.humidity_per * 0.1
                    if tile.type != "water":
                        tile.humidity_per += tile.humidity_per * 0.1
            else:
                if utils.chance_roll(50):
                    particle.value -= tile.humidity_per * 0.1

        """check life values are within limits!"""
        if particle.life < 1:
            #particle has *died" so as it is already removed, just add it into the particles list.
            self.particles.append(particle)

        else:
            if utils.chance_roll(5):
                #chaance to disappear.
                particle.value = 0
                self.particles.append(particle)
            else:

                """move to the correct tile in the map lists."""
                particle.life -= libtcod.random_get_int(0, 1, 10)
                tile.humidity = HUMIDITY_MAX * (tile.humidity_per / 100)
                self.map[particle.x][particle.y].append(particle)
                self.parent.tiles[x][y] = previous
                self.parent.tiles[particle.x][particle.y] = tile

    def moisture_change(self, the_particle, x, y):
        self.map[x][y].remove(the_particle)
        particle = the_particle
        previous = self.parent.tiles[x][y]
        particle.previous = previous
        tile = self.parent.tiles[particle.x][particle.y]

        target = tile.height_metres
        last = previous.height_metres

        if previous.height_in_metres <= 0:
            last = 0
        if tile.height_in_metres <= 0:
            target = 0

        if last == 0 and target == 0:
            height_mod = 1

        if last > target:
            n = last - target
            if last != 0:
                height_mod = (n / last)
            else:
                height_mod = 1

        elif last < target:
            n = target - last
            if last != 0:
                height_mod = (n / last)
            else:
                height_mod = 1

        """ TEMPERATURE EFFECTS"""

        target = tile.temperature
        part_temp = particle.temperature
        if target > EVAP_THRESHOLD:
            t = target - EVAP_THRESHOLD
            t = t / EVAP_THRESHOLD
        else:
            t = 1

        dif = (target - part_temp) / target

        # TODO: average of both? probably better way to do this.
        temp_mod = (dif + t) / 2

        if particle.life >= 1:
            value, tile_value = self.moisture_calc(particle, height_mod, temp_mod)
            particle.value = value
            tile.humidity = tile_value

            particle.life -= libtcod.random_get_int(0, 1, 10)
            tile.humidity = HUMIDITY_MAX * (tile.humidity_per / 100)
            self.map[particle.x][particle.y].append(particle)
            self.parent.tiles[x][y] = previous
            self.parent.tiles[particle.x][particle.y] = tile

    def moisture_calc(self, particle, height, temp, other=0):
        """
        :returns the values/....
        """
        previous = particle.previous
        tile = self.parent.tiles[particle.x][particle.y]

        # TODO: finish this. moisture calcs,

        #TEMPORARY!!!!!!!!!!!!!!
        if other == 0:
            mod_tot = (height + temp) / 2.0
        else:
            mod_tot = (height + temp + other) / 3.0

        if previous.height_in_metres < tile.height_in_metres:
            humid = tile.humidity_per + mod_tot
            humid_part = particle.value + (particle.value * mod_tot)

        elif previous.height_in_metres > tile.height_in_metres:
            humid = tile.humidity_per + mod_tot
            humid_part = particle.value + mod_tot

        else:
            humid = tile.humidity_per + mod_tot
            humid_part = particle.value + mod_tot

        value = 0
        tile_value = 0
        return value, tile_value

    def humidity_colourise(self):

        """Finally, change the humidty colour value"""
        self.parent.normalise_humidity()

        for x in range(len(self.parent.tiles)):
            for y in range(len(self.parent.tiles[x])):
                tile = self.parent.tiles[x][y]
                if tile.type != "water":
                    tile.humidity = 255 * (tile.humidity_per / 100)

                    # end particle map.


class Map:
    def __init__(self, w, h):
        global TROPICS_THRESHOLD, TEMPERATE_THRESHOLD, TAIGA_THRESHOLD

        self.w = w
        self.h = h

        self.equator = h / 2
        TROPICS_THRESHOLD = (self.equator / 2) / 3
        TEMPERATE_THRESHOLD = self.equator / 2
        TAIGA_THRESHOLD = self.equator - self.equator * 0.1
        self.tiles = [[Tile(ix, iy, False, map_tile=True)
                       for iy in range(h)]
                      for ix in range(w)]
        x, y = 0, 0
        self.traffic = [[0
                         for y in range(h)]
                        for x in range(w)]
        # this holds the *colour* value of the tiles temps.
        self.temperature_map = [[0
                                 for y in range(h)]
                                for x in range(w)]
        self.moisture_map = [[0
                              for y in range(h)]
                             for x in range(w)]

        self.blocked = []
        self.weights = {}

        self.hm = libtcod.heightmap_new(self.w, self.h)

        self.generate(51708288)  #51708288)   55920912

        # self.hm2 = libtcod.heightmap_new(self.w, self.h)
        # self.hm3 = libtcod.heightmap_new(self.w, self.h)
        #
        # self.generate_land(self.hm)
        # self.generate_land(self.hm2)
        # self.generate_land(self.hm3)
        #
        # libtcod.noise_set_type(self.noise, libtcod.NOISE_SIMPLEX)
        # self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        # #libtcod.heightmap_add_fbm(self.hm3, self.noise, 1, 1, 0, 0, 8, 0.8, 0.5)
        # #self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        # #libtcod.heightmap_add_fbm(self.hm3, self.noise, 1, 1, 0, 0, 8, 0.8, 0.5)
        # #self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        # #libtcod.heightmap_add_fbm(self.hm3, self.noise, 1, 1, 0, 0, 8, 0.8, 0.5)
        # # self.multiply_noise()
        # self.multiply_noise()
        # libtcod.heightmap_normalize(self.hm, 0, 255)
        # #libtcod.heightmap_normalize(self.hm2, 0, 255)
        # #libtcod.heightmap_normalize(self.hm3, 0, 255)
        # #libtcod.heightmap_rain_erosion(self.hm, (self.w + self.h)*4, 0.5, 0.1, None)
        #
        # # self.add_noise()

        self.turn_to_tiles()
        self.seperate_continents()
        self.determine_temperatures()
        # self.normalise_temperatures()
        self.wind_gen = Particle_Map(self, 1500)
        self.generate_mini_map(10)
        self.cities = []
        self.dungeons = []
        self.pois = []
        # self.world_noise1d = libtcod.noise_new(1, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY, self.rand)
        self.generate_city(4 + abs(libtcod.noise_get(self.map_noise1d, [0.5, 0.9, 1.0])) * 30)
        self.generate_dungeons(10)

    def generate_city(self, num):

        for n in range(int(num)):
            placed = False
            i = 1
            while not placed:

                xh = self.w / 2 - libtcod.noise_get_fbm(self.map_noise2d, [0.0, i / self.w, 0.5, 0.0], 32.0,
                                                        libtcod.NOISE_DEFAULT) * (
                                      self.w / 2)
                xh = int(xh)

                yh = self.h / 2 - libtcod.noise_get_fbm(self.map_noise2d, [0.0, i / self.h, 0.5, 0.0], 32.0,
                                                        libtcod.NOISE_DEFAULT) * (
                                      self.h / 2)
                yh = int(yh)
                # x = libtcod.random_get_int(0, 1, self.w - 1)
                # y = libtcod.random_get_int(0, 1, self.h - 1)
                tile = self.tiles[xh][yh]
                if tile.POI is None and tile.blocked is not True and tile.type != "coast":
                    tempCity = City(xh, yh)
                    self.cities.append(tempCity.component)
                    self.pois.append(tempCity)
                    self.tiles[xh][yh].POI = tempCity
                    placed = True
                    print "City succeeded", xh, yh, tempCity.name
                else:
                    print "failed", xh, yh
                    i += 1

    def generate_dungeons(self, num):
        for n in range(num):
            placed = False
            while not placed:
                x = libtcod.random_get_int(0, 1, self.w - 1)
                y = libtcod.random_get_int(0, 1, self.h - 1)
                tile = self.tiles[x][y]
                if tile.POI is None and tile.blocked is not True:
                    temp = Dungeon(x, y)
                    self.dungeons.append(temp.component)
                    self.pois.append(temp)
                    self.tiles[x][y].POI = temp
                    placed = True
                    print "Dungeon succeeded", x, y, temp.name
                else:
                    print "failed", x, y


    def seperate_continents(self):
        self.continents = [None]
        for x in range(len(self.tiles) - 1):
            for y in range(len(self.tiles[0]) - 1):
                tile = self.tiles[x][y]
                if tile.type != "water" and tile.continent == -1:
                    self.flood_fill(tile)

        for x in range(len(self.tiles) - 1):
            for y in range(len(self.tiles[0]) - 1):
                tile = self.tiles[x][y]
                if tile.continent != -1:
                    continent = self.continents[tile.continent]
                    continent.tiles[tile.x][tile.y] = tile
                    if tile.POI is not None:
                        self.continents[tile.continent].add_POI(tile.POI)

    def flood_fill_recur(self, tile, ID=-1):
        ## Recursion error. Max recurion depth exceeded.
        if tile.type == "water":
            print "huh, found water", tile.x, tile.y
            return
        if ID == -1:
            ID = len(self.continents)
            continent = Continent(ID)
            self.continents.append(continent)

        tile.continent = ID
        self.tiles[tile.x][tile.y] = tile  # don't think i need to do this.
        if tile.x + 1 < len(self.tiles):  # the right
            self.flood_fill(self.tiles[tile.x + 1][tile.y], ID)
        if tile.x - 1 > 0:  # the left
            self.flood_fill(self.tiles[tile.x - 1][tile.y], ID)
        if tile.y + 1 < len(self.tiles[0]):  # below
            self.flood_fill(self.tiles[tile.x][tile.y + 1], ID)
        if tile.y - 1 > 0:  # above
            self.flood_fill(self.tiles[tile.x][tile.y - 1], ID)

        return

    def flood_fill(self, tile, ID=-1):
        ## Recursion error. Max recurion depth exceeded.
        if tile.type == "water":
            print "huh, found water", tile.x, tile.y
            return

        if ID == -1:
            ID = len(self.continents)
            continent = Continent(ID, self.w, self.h)
            self.continents.append(continent)
        toFill = set()
        toFill.add(tile)

        while len(toFill) > 0:
            tile = toFill.pop()
            if tile.type == "water" or tile.continent == ID:
                print "huh, found water or already done", tile.x, tile.y
                continue
            else:
                tile.continent = ID
                if tile.x + 1 < len(self.tiles):  # the right
                    toFill.add(self.tiles[tile.x + 1][tile.y])
                if tile.x - 1 > 0:  # the left
                    toFill.add(self.tiles[tile.x - 1][tile.y])
                if tile.y + 1 < len(self.tiles[0]):  # below
                    toFill.add(self.tiles[tile.x][tile.y + 1])
                if tile.y - 1 > 0:  # above
                    toFill.add(self.tiles[tile.x][tile.y - 1])

        return

    def connect_cities(self):
        pather = pathfinding.Pather()
        for city in self.cities:
            for other_city in self.cities:
                if city == other_city:
                    continue
                else:
                    path = pather.new_find_path((city.x, city.y), (other_city.x, other_city.y), self.tiles) or []
                    while len(path) > 0:
                        node = path.pop()
                        self.tiles[node[0]][node[1]].bg = libtcod.Color(200, 200, 10)
                        self.tiles[node[0]][node[1]].cost = PATH_COST
                        self.tiles[node[0]][node[1]].type = "path"
                    print "........................connected ", city.name, " and ", other_city.name



                    # i = 0.1
                    #
                    # fc = libtcod.noise_get_fbm(self.map_noise2d, [0.0, 0.5, i / 2], 32.0, libtcod.NOISE_SIMPLEX) * ( len(self.cities) - 1)
                    # fc = int(abs(fc))
                    #
                    # oc = libtcod.noise_get_fbm(self.map_noise2d, [0.0, 0.5, i * 2], 32.0, libtcod.NOISE_DEFAULT) * ( len(self.cities) - 1)
                    # oc = int(abs(oc))
                    # pather = pathfinding.Pather()
                    # city_one = self.cities[fc]
                    # city_two = self.cities[oc]#libtcod.random_get_int(0, 0, len(self.cities) - 1)]
                    #
                    # while city_one == city_two and len(self.cities) > 1 and city_one:
                    # fc = 0.0 + libtcod.noise_get(self.map_noise1d, [0.0, 0.5, i * len(self.cities)], libtcod.NOISE_DEFAULT) * ( len(self.cities) - 1)
                    #     fc = int(abs(fc))
                    #     city_two = self.cities[fc]
                    #     i += 0.1
                    #
                    # path = pather.new_find_path((city_one.x, city_one.y), (city_two.x, city_two.y), self.tiles)
                    #
                    # while path == None:
                    #     path = pather.new_find_path((city_one.x, city_one.y), (city_two.x, city_two.y), self.tiles)
                    #
                    #     # if path == None:
                    #     #     city_one = self.cities[libtcod.random_get_int(0, 0, len(self.cities) - 1)]
                    #     #     city_two = self.cities[libtcod.random_get_int(0, 0, len(self.cities) - 1)]
                    #     #
                    #     #     while city_one == city_two and len(self.cities) > 1:
                    #     #         city_two = self.cities[libtcod.random_get_int(0, 0, len(self.cities) - 1)]
                    #
                    # # for node in path:
                    #
                    # while len(path) > 0:
                    #     node = path.pop()
                    #     self.tiles[node[0]][node[1]].bg = libtcod.Color(200, 200, 10)
                    #     self.tiles[node[0]][node[1]].cost = PATH_COST
                    #     self.tiles[node[0]][node[1]].type = "path"
                    #     # path = path.parent_node

                    # print "........................connected ", city_one.name, " and ", city_two.name

    def add_foot_traffic(self, x, y):
        self.traffic[x][y] += 1

    def get_foot_traffic(self, x, y):
        return self.traffic[x][y]

    def sort_for_highest_traffic(self, highest=True):
        highest = [0.0, 0, 0]
        lowest = [99999999, 0, 0]
        for x in range(len(self.traffic)):
            for y in range(len(self.traffic[x])):
                if self.traffic[x][y][0] > highest[0]:
                    highest = [self.traffic[x][y][0], x, y]
                elif self.traffic[x][y][0] < lowest[0]:
                    lowest = [self.traffic[x][y][0], x, y]

        if highest:
            return highest  # can return lowest too.
        else:
            return lowest

    def generate_mini_map(self, zone=10, hm=None):

        if hm is None:
            hm = self.hm

        if (self.w % zone) > 0:
            print "doesn't smoothly fit - W"
        if (self.h % zone) > 0:
            print "doesn't smoothly fit - H"

        self.mini_map = []
        self.mini_map = [[None
                          for y in range(int(self.h / zone))]
                         for x in range(int(self.w / zone))]

        for a in range(len(self.tiles) / zone):
            for b in range(len(self.tiles[a]) / zone):
                cell_x = 0
                cell_y = 0
                tiles = [[0, []], [0, []]]
                x = a * zone
                y = b * zone
                for cell_x in range(zone):
                    if x + cell_x > len(self.tiles) - 1:
                        break
                    for cell_y in range(zone):
                        if y + cell_y > len(self.tiles[cell_x]) - 1:
                            break
                        # TODO: put in catches for the "end" bits where there is less tiles left than the "zone".
                        value = int(libtcod.heightmap_get_value(hm, x + cell_x, y + cell_y))
                        if value > WATER_THRESHOLD:
                            tiles[0][0] += 1
                            tiles[0][1].append(value)

                        else:
                            tiles[1][0] += 1
                            tiles[1][1].append(value)

                if tiles[0] > tiles[1]:
                    # make land
                    sum_ = sum(num for num in tiles[0][1])
                    value = sum_ / len(tiles[0][1])
                    self.mini_map[a][b] = Tile(cell_x, cell_y, False, map_tile=True, bg=[10, value, 10])
                elif tiles[1] > tiles[0]:
                    # make water
                    sum_ = sum(num for num in tiles[1][1])
                    value = sum_ / len(tiles[1][1])
                    self.mini_map[a][b] = Tile(cell_x, cell_y, True, map_tile=True, bg=[10, 10, value])
                else:
                    # flip for either.
                    flip = libtcod.random_get_int(0, 0, 1)
                    if flip == 1:
                        #water
                        sum_ = sum(num for num in tiles[1][1])
                        value = sum_ / len(tiles[1][1])
                        self.mini_map[a][b] = Tile(cell_x, cell_y, True, map_tile=True, bg=[10, 10, value])
                    if flip == 0:
                        #land
                        sum_ = sum(num for num in tiles[0][1])
                        value = sum_ / len(tiles[0][1])
                        self.mini_map[a][b] = Tile(cell_x, cell_y, False, map_tile=True, bg=[10, value, 10])

                        #     def generate_land(self,hm):
                        #
                        #         print hm.w, hm.h
                        #         #self.noise = perlin_noise.PerlinNoiseGenerator()
                        #         #self.noise.generate_noise(self.w, self.h, 1, 16)
                        #         #print str(self.noise.noise[1][1])
                        #
                        #         self.add_hill(self.w/2, self.h/2, hm)
                        #         self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
                        #         libtcod.heightmap_add_fbm(hm, self.noise, 1, 1, 0, 0, 8, 0.5, 0.8)
                        #         print "scale", str(libtcod.heightmap_get_value(hm, 1, 1))
                        #         self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
                        #         libtcod.noise_set_type(self.noise, libtcod.NOISE_PERLIN)
                        #         libtcod.heightmap_scale_fbm(hm, self.noise, 1, 1, 0, 0, 8, 0.5, 0.8)
                        # #        self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
                        # #        libtcod.heightmap_add_fbm(hm, self.noise, 1, 1, 0, 0, 8, 0.8, 0.5)
                        # #
                        #         libtcod.heightmap_normalize(hm, 0, 255)
                        #         print "normalized", str(libtcod.heightmap_get_value(hm, 1, 1))
                        #
                        #         # return hm

    def add_noise(self):
        libtcod.heightmap_normalize(self.hm, 0, 1)
        self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        libtcod.noise_set_type(self.noise, libtcod.NOISE_PERLIN)
        libtcod.heightmap_add_fbm(self.hm, self.noise, 1, 1, 1, 1, 8, 0.5, 0.5)
        libtcod.heightmap_normalize(self.hm, 0, 255)

    def multiply_noise(self):
        self.noise = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY)
        # libtcod.noise_set_type(self.noise, libtcod.NOISE_PERLIN)
        libtcod.heightmap_scale_fbm(self.hm, self.noise, 1, 1, 1, 1, 16, 0.5, 0.5)
        # libtcod.heightmap_normalize(self.hm, 0, 255)

    def add_hill(self, x, y, hm):
        r = 20
        xh = self.w
        yh = self.h

        one = (x - xh ) * (x - xh )
        two = (y - yh) * (y - yh)

        hill_height = ((r * r) + one + two) / 4

        if hill_height > 0:
            libtcod.heightmap_add_hill(hm, x, y, r, 1)
            # libtcod.heightmap_normalize(hm, 0, 255)

    def turn_to_tiles(self):
        if R.DEBUG:
            t0 = libtcod.sys_elapsed_seconds()

        self.tiles = []

        self.tiles = [[Tile(ix, iy, False, map_tile=True)
                       for iy in range(self.h)]
                      for ix in range(self.w)]

        for cell_x in range(self.w):
            for cell_y in range(self.h):
                value = int(libtcod.heightmap_get_value(self.hm, cell_x, cell_y))

                if value < WATER_THRESHOLD:  # water
                    tote = value + libtcod.random_get_int(0, -5, 5)
                    if tote > 255:
                        tote = 255
                    if tote < 0:
                        tote = 0

                    self.tiles[cell_x][cell_y] = Tile(cell_x, cell_y, True, map_tile=True, bg=[10, 10, tote],
                                                      cost=WATER_COST)
                    self.tiles[cell_x][cell_y].elevation = value
                    self.tiles[cell_x][cell_y].humidity = 255
                    self.tiles[cell_x][cell_y].humidity_per = 100.0
                    self.tiles[cell_x][cell_y].type = "water"
                    self.blocked.append((cell_x, cell_y))  #add water tile to blocked.

                elif value < GRASS_THRESHOLD:  # coast
                    test = int(math.sqrt(value))
                    # test = test ** 3
                    self.tiles[cell_x][cell_y] = Tile(cell_x, cell_y, False, map_tile=True,
                                                      bg=[value + libtcod.random_get_int(0, -5, 5),
                                                          value - test + libtcod.random_get_int(0, -5, 5),
                                                          test],
                                                      cost=COAST_COST)
                    self.tiles[cell_x][cell_y].elevation = value
                    self.tiles[cell_x][cell_y].humidity = libtcod.heightmap_get_value(self.precipitation_map, cell_x,
                                                                                      cell_y)
                    self.tiles[cell_x][cell_y].humidity_per = (self.tiles[cell_x][cell_y].humidity / 255) * 100
                    self.tiles[cell_x][cell_y].type = "coast"

                elif value < MOUNTAIN_THRESHOLD:  # grass
                    ran_1 = 255 - (value + libtcod.random_get_int(0, -5, 5))
                    if ran_1 > 255:
                        ran_1 = 255
                    self.tiles[cell_x][cell_y] = Tile(cell_x, cell_y, False, map_tile=True,
                                                      bg=[10 + libtcod.random_get_int(0, -5, 5),
                                                          ran_1,
                                                          10 + libtcod.random_get_int(0, -5, 5)],
                                                      cost=GRASS_COST)
                    self.tiles[cell_x][cell_y].elevation = value
                    self.tiles[cell_x][cell_y].humidity = libtcod.heightmap_get_value(self.precipitation_map, cell_x,
                                                                                      cell_y)
                    self.tiles[cell_x][cell_y].humidity_per = (self.tiles[cell_x][cell_y].humidity / 255) * 100
                    self.tiles[cell_x][cell_y].type = "grass"

                else:
                    mountain = 50 + (value - MOUNTAIN_THRESHOLD)
                    shift = libtcod.random_get_int(0, -5, 5)
                    tote = mountain + shift
                    if tote > 255:
                        tote = 255
                    if tote < 0:
                        tote = 0
                    # self.tiles[cell_x][cell_y] = Tile(cell_x,cell_y, False, map_tile=True, bg=[40 + mountain, value - mountain, 40 + mountain], cost = 20)
                    self.tiles[cell_x][cell_y] = Tile(cell_x, cell_y, False,
                                                      map_tile=True, bg=[tote,
                                                                         tote,
                                                                         tote + libtcod.random_get_int(0, -5, 5)],
                                                      cost=MOUNTAIN_COST)
                    self.tiles[cell_x][cell_y].elevation = value
                    self.tiles[cell_x][cell_y].humidity = libtcod.heightmap_get_value(self.precipitation_map, cell_x,
                                                                                      cell_y)
                    self.tiles[cell_x][cell_y].humidity_per = (self.tiles[cell_x][cell_y].humidity / 255) * 100
                    self.tiles[cell_x][cell_y].type = "mountain"

                self.weights[(cell_x, cell_y)] = self.tiles[cell_x][cell_y].cost  # add the weight!
        #
        if R.DEBUG:
            t1 = libtcod.sys_elapsed_seconds()
            print "Converted to Tiles %s" % (t1 - t0)

            # self.tiles = []
            #
            # self.tiles = [[ Tile(ix,iy, False, map_tile=True)
            # for iy in range(self.h) ]
            #         for ix in range(self.w)]
            #
            # for cell_x in range(self.w):
            #     for cell_y in range(self.h):
            #         value = int(libtcod.heightmap_get_value(self.hm, cell_x, cell_y))
            #
            #         if value > MOUNTAIN_THRESHOLD: #mountain
            #             mountain = 50 + (value - MOUNTAIN_THRESHOLD)
            #             shift = libtcod.random_get_int(0,-5,5)
            #             tote = mountain + shift
            #             if tote > 255:
            #                 tote = 255
            #             if tote < 0:
            #                 tote = 0
            #             #self.tiles[cell_x][cell_y] = Tile(cell_x,cell_y, False, map_tile=True, bg=[40 + mountain, value - mountain, 40 + mountain], cost = 20)
            #             self.tiles[cell_x][cell_y] = Tile(cell_x,cell_y, False, map_tile=True, bg=[tote, tote, tote], cost = 40)
            #             self.tiles[cell_x][cell_y].elevation = value
            #             self.tiles[cell_x][cell_y].humidity = libtcod.random_get_int(0,0,5)
            #             self.tiles[cell_x][cell_y].humidity_per = self.tiles[cell_x][cell_y].humidity/255*100
            #             self.tiles[cell_x][cell_y].type = "mountain"
            #
            #         elif value > WATER_THRESHOLD + COASTLINE_THRESHOLD: #grass
            #             ran_1 = 255- value+ libtcod.random_get_int(0,-5,5)
            #             if ran_1 > 255:
            #                 ran_1 = 255
            #             self.tiles[cell_x][cell_y] = Tile(cell_x,cell_y, False, map_tile=True, bg=[10,ran_1,10 + libtcod.random_get_int(0,-5,5)], cost = 15)
            #             self.tiles[cell_x][cell_y].elevation = value
            #             self.tiles[cell_x][cell_y].humidity = libtcod.random_get_int(0,10,100)
            #             self.tiles[cell_x][cell_y].humidity_per = self.tiles[cell_x][cell_y].humidity/255*100
            #
            #         elif value > WATER_THRESHOLD: #coast
            #             test = int(math.sqrt(value))
            #             #test = test ** 3
            #             self.tiles[cell_x][cell_y] = Tile(cell_x,cell_y, False, map_tile=True, bg=[value+ libtcod.random_get_int(0,-5,5),value-test+ libtcod.random_get_int(0,-5,5),test])
            #             self.tiles[cell_x][cell_y].elevation = value
            #             self.tiles[cell_x][cell_y].humidity = 25.5
            #             self.tiles[cell_x][cell_y].humidity_per = 10.0
            #
            #         else: #water
            #             tote = value + libtcod.random_get_int(0,-5,5)
            #             if tote > 255:
            #                 tote = 255
            #             if tote < 0:
            #                 tote = 0
            #
            #             self.tiles[cell_x][cell_y] = Tile(cell_x,cell_y, True, map_tile=True, bg=[10,10,tote])
            #             self.tiles[cell_x][cell_y].elevation = value
            #             self.tiles[cell_x][cell_y].humidity = 255
            #             self.tiles[cell_x][cell_y].humidity_per = 100.0
            #             self.tiles[cell_x][cell_y].type = "water"

    def get_temperature(self, x, y):
        return self.temperature_map[x][y]

    def determine_temperatures(self):

        for x in range(self.w):
            for y in range(self.h):
                altitude = self.tiles[x][y].elevation
                if altitude > WATER_THRESHOLD:
                    altitude -= WATER_THRESHOLD
                    multiplier = math.e ** (0.0207345 * altitude)
                    height_in_metres = 282.33 * multiplier
                    self.tiles[x][y].height_metres = height_in_metres

                    if y <= self.equator:
                        distance_from_equator = float(self.equator - y)
                    elif y > self.equator:
                        distance_from_equator = float(y - self.equator)
                        # this needs to be softer. too "bandy" at the moment. somehow do this ona  scale rather than BAM you're now x.
                    # if distance_from_equator <= TROPICS_THRESHOLD:
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
                    temp_drop = 0.006 * percent ** 2 + 5.71976 * 10 ** -16 * percent - 5.89344 * 10 ** -14
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

                    multiplier = math.e ** (0.0207345 * altitude)
                    depth_in_metres = 282.33 * multiplier
                    self.tiles[x][y].height_metres = -depth_in_metres

                    if y <= self.equator:
                        distance_from_equator = float(self.equator - y)
                    elif y > self.equator:
                        distance_from_equator = float(y - self.equator)
                        # start at equator temp
                    temp = 5
                    # percent of total possible distance
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
                    temp_drop = 0.006 * percent ** 2 + 5.71976 * 10 ** -16 * percent - 5.89344 * 10 ** -14
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
        # find the high and low temps.
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
        # find the high and low temps.
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

    def generate_stupid_map(self, seed=None):

        t00 = t0 = libtcod.sys_elapsed_seconds()

        if seed is None:
            self.rand = libtcod.random_new()
        else:
            self.rand = libtcod.random_new_from_seed(seed)

        self.map_noise1d = libtcod.noise_new(1, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY,
                                             self.rand)
        self.map_noise2d = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY,
                                             self.rand)

        self.hm = libtcod.heightmap_new(self.w, self.h)
        self.hm_wo_erosion = libtcod.heightmap_new(self.w, self.h)
        self.temperature_map = libtcod.heightmap_new(self.w, self.h)
        self.precipitation_map = libtcod.heightmap_new(self.w, self.h)

        t1 = libtcod.sys_elapsed_seconds()
        print "init hills %s" % (t1 - t0)
        t0 = t1
        self.add_hills(self.hm, 800, 16.0 * self.w / 200.0, 0.7, 0.3)

        # libtcod.heightmap_normalize(self.hm)
        libtcod.heightmap_add_fbm(self.hm, self.map_noise2d, 2.20 * self.w / 400.0, 2.20 * self.h / 400.0, 0, 0, 5.0,
                                  1.0,
                                  2.05)
        # libtcod.heightmap_add_fbm(self.hm, self.noise2d, 1, 1, 0, 0, 10.0, 1, 1)

        libtcod.heightmap_normalize(self.hm, 0, 255)

        t1 = libtcod.sys_elapsed_seconds()
        print "turn to tiles... %s" % (t1 - t0)
        self.turn_to_tiles()
        t0 = t1

    def generate(self, seed=None):
        t00 = t0 = libtcod.sys_elapsed_seconds()

        if seed is None:
            self.rand = libtcod.random_new()  # random seed
        else:
            self.rand = libtcod.random_new_from_seed(seed)  # specified seed

        print self.rand
        self.map_noise1d = libtcod.noise_new(1, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY,
                                             self.rand)
        self.map_noise2d = libtcod.noise_new(2, libtcod.NOISE_DEFAULT_HURST, libtcod.NOISE_DEFAULT_LACUNARITY,
                                             self.rand)

        self.hm = libtcod.heightmap_new(self.w, self.h)
        self.hm_wo_erosion = libtcod.heightmap_new(self.w, self.h)
        self.temperature_map = libtcod.heightmap_new(self.w, self.h)
        self.precipitation_map = libtcod.heightmap_new(self.w, self.h)

        t1 = libtcod.sys_elapsed_seconds()
        print "init... %s" % (t0)
        self.generate_land()
        t0 = t1

        t1 = libtcod.sys_elapsed_seconds()
        print "init clouds %s" % (t1 - t0)
        t0 = t1

        self.smooth_map()
        t1 = libtcod.sys_elapsed_seconds()
        print "Smooth Map... %s" % (t1 - t0)
        t0 = t1

        self.compute_precipitations()
        t1 = libtcod.sys_elapsed_seconds()
        print "Precipitation Map.... %s" % (t1 - t0)
        t0 = t1

        self.dig_border_hills(self.hm, 10, 0.7, 0.3)
        t1 = libtcod.sys_elapsed_seconds()
        print "Dig border hills.... %s" % (t1 - t0)
        t0 = t1

        # self.erode_map()
        self.other_erode()
        t1 = libtcod.sys_elapsed_seconds()
        print "Erode Map... %s" % (t1 - t0)
        t0 = t1

        self.smooth_map()
        t1 = libtcod.sys_elapsed_seconds()
        print "Smooth Map... %s" % (t1 - t0)
        t0 = t1

        self.set_land_mass(0.4, SAND_HEIGHT)

        # do rivers

        # smooth rains

        # do temps and biomes
        self.determine_temperatures()  #own hacky version?
        # self.normalise_temperatures()

        #do colours n shit

        libtcod.heightmap_normalize(self.hm, 0, 255)

        t1 = libtcod.sys_elapsed_seconds()
        print "turn to tiles... %s" % (t1 - t0)
        self.turn_to_tiles()
        t0 = t1

        print "total time.. %s" % (t1 - t00)


    def compute_precipitations(self):
        if R.DEBUG:
            t0 = libtcod.sys_elapsed_seconds()
        water_add = 0.0
        slope_coef = 2.0
        base_precip = 0.01

        for diry in xrange(-1, 1, 2):
            for x in xrange(self.w):
                noise_x = [float((x) * 5 / self.w)]
                water_amount = (1.0 + libtcod.noise_get_fbm(self.map_noise1d, noise_x, 3.0, libtcod.NOISE_SIMPLEX))
                if diry == -1:
                    starty = self.h - 1
                else:
                    starty = 0
                if diry == -1:
                    endy = -1
                else:
                    endy = self.h
                for y in xrange(starty, endy, diry):
                    h = libtcod.heightmap_get_value(self.hm, x, y)
                    if h < SAND_HEIGHT:
                        water_amount += water_add
                    elif water_amount > 0.0:
                        slope = 0.0
                        if abs(y + diry) < abs(self.h):
                            slope = libtcod.heightmap_get_value(self.hm, x, y + diry) - h
                        else:
                            slope = h - libtcod.heightmap_get_value(self.hm, x, y - diry)
                        if slope >= 0.0:
                            precip = water_amount * (base_precip + slope * slope_coef )
                            libtcod.heightmap_set_value(self.precipitation_map, x, y,
                                                        libtcod.heightmap_get_value(self.precipitation_map, x,
                                                                                    y) + precip)
                            water_amount -= precip
                            water_amount = max(0.0, water_amount)

        if R.DEBUG:
            t1 = libtcod.sys_elapsed_seconds()
            print "N/S winds %s" % (t1 - t0)
            t0 = t1

        for dirx in xrange(-1, 1, 2):
            for y in xrange(self.h):
                noise_y = [float((y) * 5 / self.h)]
                water_amount = (1.0 + libtcod.noise_get_fbm(self.map_noise1d, noise_y, 3.0, libtcod.NOISE_SIMPLEX))
                if dirx == -1:
                    startx = self.w - 1
                else:
                    startx = 0
                if dirx == -1:
                    endx = -1
                else:
                    endx = self.h
                for x in xrange(startx, endx, dirx):
                    h = libtcod.heightmap_get_value(self.hm, y, y)
                    if h < SAND_HEIGHT:
                        water_amount += water_add
                    elif water_amount > 0.0:
                        slope = 0.0
                        if abs(x + dirx) < abs(self.h):
                            slope = libtcod.heightmap_get_value(self.hm, x + dirx, y) - h
                        else:
                            slope = h - libtcod.heightmap_get_value(self.hm, x - dirx, y)
                        if slope >= 0.0:
                            precip = water_amount * (base_precip + slope * slope_coef )
                            libtcod.heightmap_set_value(self.precipitation_map, x, y,
                                                        libtcod.heightmap_get_value(self.precipitation_map, y,
                                                                                    y) + precip)
                            water_amount -= precip
                            water_amount = max(0.0, water_amount)

        if R.DEBUG:
            t1 = libtcod.sys_elapsed_seconds()
            print "E/W winds.. %s" % (t1 - t0)
            t0 = t1

        max_, max_ = libtcod.heightmap_get_minmax(self.precipitation_map)

        for y in xrange(self.h / 4, 3 * self.h / 4):
            lat = (y - self.h / 4) * 2 / self.h
            coef = math.sin(2 * math.pi * lat)
            for x in xrange(0, self.w):
                f = [float(x) / self.w, float(y) / self.h]
                xcoef = coef + 0.5 * libtcod.noise_get(self.map_noise2d, f, libtcod.NOISE_SIMPLEX)
                precip = libtcod.heightmap_get_value(self.precipitation_map, x, y)
                precip += (max_ - max_) * xcoef * 0.1
                libtcod.heightmap_set_value(self.precipitation_map, x, y, precip)

        if R.DEBUG:
            t1 = libtcod.sys_elapsed_seconds()
            print "latitude.. %s" % (t1 - t0)
            t0 = t1

        factor = 8
        small_width = (self.w + factor - 1) / factor
        small_height = (self.h + factor - 1) / factor
        low_res = [0.0] * (small_width * small_height)

        for x in xrange(self.w):
            for y in xrange(self.h):
                v = libtcod.heightmap_get_value(self.precipitation_map, x, y)
                ix = x / factor
                iy = y / factor
                low_res[ix + iy * small_width] += v

        coef = 1.0 / factor
        for x in xrange(self.w):
            for y in xrange(self.h):
                v = get_interpolated_float(low_res, x * coef, y * coef, small_width, small_height)
                libtcod.heightmap_set_value(self.precipitation_map, x, y, v)


    def other_erode(self):
        libtcod.heightmap_rain_erosion(self.hm, 10000, 0.1, 0.1)


    def smooth_map(self):
        smooth_kernel_size = 9
        smoothKernelDx = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
        smoothKernelDy = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
        smoothKernelWeight = [2, 8, 2, 8, 20, 8, 2, 8, 2]

        if R.DEBUG:
            t0 = libtcod.sys_elapsed_seconds()

        libtcod.heightmap_kernel_transform(self.hm, smooth_kernel_size, smoothKernelDx, smoothKernelDy,
                                           smoothKernelWeight, -1000, 1000)
        libtcod.heightmap_kernel_transform(self.hm_wo_erosion, smooth_kernel_size, smoothKernelDx, smoothKernelDy,
                                           smoothKernelWeight, -1000, 1000)
        libtcod.heightmap_normalize(self.hm)

        if R.DEBUG:
            t1 = libtcod.sys_elapsed_seconds()
            print "Blur.. %s" % (t1 - t0)

    def generate_land(self):

        if R.DEBUG:
            t0 = libtcod.sys_elapsed_seconds()

        print self.hm.w, self.hm.h
        self.add_hills(self.hm, 600, 16.0 * self.w / 200.0, 0.7, 0.3)
        # center = [libtcod.heightmap_get_value(self.hm, self.w / 2, self.h / 2),
        # libtcod.heightmap_get_value(self.hm, self.w / 2 - 1, self.h / 2 - 1),
        #           libtcod.heightmap_get_value(self.hm, self.w / 2, self.h / 2 - 1)]
        # # self.average_point(self.w / 2 + 1, self.h / 2 + 1)

        libtcod.heightmap_normalize(self.hm)

        if R.DEBUG:
            t1 = libtcod.sys_elapsed_seconds()
            print "init hills %s" % (t1 - t0)
            t0 = t1

        libtcod.heightmap_add_fbm(self.hm, self.map_noise2d, 2.20 * self.w / 200.0, 2.20 * self.h / 200.0, 0, 0, 10.0,
                                  1.0,
                                  2.05)
        # libtcod.heightmap_add_fbm(self.hm, self.noise2d, 0.20 * self.w / 400.0, 2.20 * self.h / 350.0, 100, 5, 10.0, 1.0,
        #                           2.05)


        self.dig_border_hills(self.hm, 10, 0.7, 0.5)
        t1 = libtcod.sys_elapsed_seconds()
        print "Dig border hills.... %s" % (t1 - t0)
        t0 = t1

        libtcod.heightmap_normalize(self.hm)
        t1 = libtcod.sys_elapsed_seconds()
        print "Added noise and Normalised Base Map.... %s" % (t1 - t0)
        t0 = t1

        libtcod.heightmap_copy(self.hm, self.hm_wo_erosion)

        self.set_land_mass(0.6, SAND_HEIGHT)

        # fix land/mountain ratio using x^3 curve above sea level.
        # for x in xrange(self.w):
        #     for y in xrange(self.h):
        #         h = libtcod.heightmap_get_value(self.hm, x, y)
        #         if h >= SAND_HEIGHT:
        #             coef = (h - SAND_HEIGHT) / (1.0 - SAND_HEIGHT)
        #             h = SAND_HEIGHT + coef * coef * coef * (1.0 - SAND_HEIGHT)
        #             libtcod.heightmap_set_value(self.hm, x, y, h)

        if R.DEBUG:
            t1 = libtcod.sys_elapsed_seconds()
            print "flatten plains %s" % (t1 - t0)
            t0 = t1


            # compute clouds.
            # f = [0.0, 0.0]
            # for x in xrange(self.w):
            #     f[0] = 6.0 * (float(x) / self.w)
            #     for y in xrange(self.h):
            #         f[1] = 6.0 * (float(y) / self.h)
            #         self.clouds[x][y] = 0.5 * (1.0 + 0.8 * libtcod.noise_get_fbm(self.noise2d, f, 4.0))


    def add_hills(self, hm, number, baseRadius, radius_var, height):
        for i in range(number):
            hill_min_r = baseRadius * (1.0 - radius_var)
            hill_max_r = baseRadius * (1.0 + radius_var)
            # radius = libtcod.random_get_float(0,hill_min_r, hill_max_r)
            # (max - min) + 1) + min;
            num = libtcod.noise_get(self.map_noise1d, [baseRadius / (i + 1), i / hill_min_r, hill_max_r]) * baseRadius
            if num == 0: num += 0.1
            radius = (abs(num) - hill_min_r + 1) + hill_max_r
            if radius <= 1.0 or num == 0.0:
                print "radius less than one"
            # xh = libtcod.random_get_int(0, 0, self.w -1)
            # yh = libtcod.random_get_int(0, 0, self.h -1)
            # variance = 15
            # variance = (self.w  / 2 + libtcod.random_get_int(0, -variance, variance))
            xh = self.w / 2
            yh = self.h / 2
            # xh = (libtcod.noise_get_fbm(self.noise2d, [self.w * (i + 1), i / num, self.w], 3.0, libtcod.NOISE_PERLIN) * self.w) + 1
            xh -= libtcod.noise_get_fbm(self.map_noise2d, [0.0, i / num, 0.5, 0.0], 32.0, libtcod.NOISE_DEFAULT) * (
                self.w / 2) + 1
            # yh = (self.h / 2 + libtcod.random_get_int(0, -variance, variance))
            # yh = (libtcod.noise_get_fbm(self.noise2d, [self.h / (i + 1), i * num, self.h], 5.0, libtcod.NOISE_SIMPLEX) * self.h) + 1
            yh -= libtcod.noise_get_fbm(self.map_noise2d, [0.0, i / num, 0.5], 32.0, libtcod.NOISE_PERLIN) * (
                self.h / 2) + 1
            # xh = int(min(max(radius + 1, int(xh)), self.w - 1 - radius))
            # yh = int(min(max(radius + 1, int(yh)), self.h - 1 - radius))
            # yh = R.MAP_HEIGHT/2

            yh = int(yh)
            xh = int(xh)

            # if the hill overlaps the edge, dont add it.
            if 2 * radius > xh or xh > self.w - 2 * radius or 2 * radius > yh or yh > self.h - 2 * radius:  # or xh == yh or xh == 0:
                print "doofus", xh, yh
            else:
                print xh, yh, height
                libtcod.heightmap_add_hill(self.hm, xh, yh, radius, height)

    def dig_border_hills(self, hm, base_radius, radius_var, height):
        for x in xrange(0, self.w - 1, self.w - 1):
            for y in xrange(self.h / 10):
                if 0 < x and x < self.w and 0 < y and y < self.h:
                    hill_min_r = base_radius * (1.0 - radius_var)
                    hill_max_r = base_radius * (1.0 + radius_var)
                    num = libtcod.noise_get(self.map_noise1d,
                                            [base_radius / (x + 1), y / hill_min_r, hill_max_r]) * base_radius
                    if num == 0: num += 0.1
                    radius = (abs(num) - hill_min_r + 1) + hill_max_r

                    libtcod.heightmap_dig_hill(hm, x, y, radius, height)

        for x in xrange(5, self.w / 10):
            for y in xrange(0, self.h - 1, self.h - 1):
                if 0 < x and x < self.w and 0 < y and y < self.h:
                    hill_min_r = base_radius * (1.0 - radius_var)
                    hill_max_r = base_radius * (1.0 + radius_var)
                    num = libtcod.noise_get(self.map_noise1d,
                                            [hill_min_r / base_radius, hill_max_r / base_radius, x / self.w,
                                             y / self.h]) * base_radius
                    if num == 0: num += 0.1
                    radius = (abs(num) - hill_min_r + 1) + hill_max_r

                    libtcod.heightmap_dig_hill(hm, x, y, radius, height)

    def set_land_mass(self, land_mass, water_level):
        if R.DEBUG:
            t0 = libtcod.sys_elapsed_seconds()

        heightcount = [0] * 256
        for x in xrange(self.w):
            for y in xrange(self.h):
                h = libtcod.heightmap_get_value(self.hm, x, y)
                int_h = int(h * 255)
                int_h = utils.clamp(int_h, 0, 255)
                heightcount[int_h] += 1

        i = 0
        total_count = 0

        while total_count < self.w * self.h * (1.0 - land_mass):
            total_count += heightcount[i]
            i += 1

        new_water_level = i / 255.0
        land_coef = (1.0 - water_level) / (1.0 - new_water_level)
        water_coef = water_level / new_water_level

        # water level risen/loweered to new water level.
        for x in xrange(self.w):
            for y in xrange(self.h):
                h = libtcod.heightmap_get_value(self.hm, x, y)
                if h > new_water_level:
                    h = water_level + (h - new_water_level) * land_coef
                else:
                    h = h * water_coef

                libtcod.heightmap_set_value(self.hm, x, y, h)

        if R.DEBUG:
            t1 = libtcod.sys_elapsed_seconds()
            print "Landmass %s" % (t1 - t0)


class Continent:
    def __init__(self, ID, w, h):
        self.poi_ls = []
        self.ID = ID
        self.tiles = [[[]
                          for y in range(h)]
                      for x in range(w)]

    def add_POI(self, POI):
        if POI not in self.poi_ls:
            self.poi_ls.append(POI)
        else:
            print "POI already in list."

    def remove_POI(self, POI):
        if POI in self.poi_ls:
            self.poi_ls.remove(POI)
        else:
            print "POI not in list."

    def on_continent(self, x, y):
        # todo: make this quick and easy? - maybe dict instead of list.
        pass


def within_bounds(x, y, map_=None):
    if map_ == None:
        map_ = R.world
    if x >= 0 and x < len(map_) and y >= 0 and y < len(map_[0]):
        return True
    else:
        return False


class POI:
    def __init__(self, x, y, colour=None, char="X", type="none"):
        self.x = x
        self.y = y
        self.colour = colour
        if self.colour == None:
            self.colour = libtcod.Color(libtcod.random_get_int(0, 0, 255), libtcod.random_get_int(0, 0, 255),
                                        libtcod.random_get_int(0, 0, 255))
        self.char = char
        self.type = type
        self.name = "named"
        self.component = None


# if self.type == "Dungeon":
#            self.component = Dungeon.Dungeon()

class Dungeon(POI):
    def __init__(self, x, y, level=1):
        POI.__init__(self, x, y, libtcod.Color(libtcod.random_get_int(0, 50, 255), libtcod.random_get_int(0, 0, 100),
                                               libtcod.random_get_int(0, 200, 255)), "#")
        self.component = dungeon.Dungeon(x, y, self)
        self.name = self.component.name
        self.type = "dungeon"
        print "dungeon!"


class City(POI):
    def __init__(self, x, y, population=-1):
        POI.__init__(self, x, y, libtcod.Color(libtcod.random_get_int(0, 50, 255), libtcod.random_get_int(0, 0, 255),
                                               libtcod.random_get_int(0, 100, 255)), "C")
        self.component = city.City(x, y, self)
        self.name = self.component.name
        self.type = "city"
        self.connections = {}


class Resource(POI):
    def __init__(self, x, y):
        POI.__init__(self, x, y, libtcod.Color(libtcod.random_get_int(0, 50, 255), libtcod.random_get_int(0, 0, 255),
                                               libtcod.random_get_int(0, 100, 255)), "C")


def get_interpolated_float(arr, x, y, width, height):
    wx = utils.clamp(0.0, width - 1, x)
    wy = utils.clamp(0.0, height - 1, y)
    iwx = int(wx)
    iwy = int(wy)
    dx = wx - iwx
    dy = wy - iwy

    iNW = arr[iwx + iwy * width]
    if iwx < width - 1:
        iNE = arr[iwx + 1 + iwy * width]
    else:
        iNE = iNW
    if iwy < height - 1:
        iSW = arr[iwx + (iwy + 1) * width]
    else:
        iSW = iNW
    if iwx < width - 1 and iwy < height - 1:
        iSE = arr[iwx + 1 + (iwy + 1) * width]
    else:
        iSE = iNW

    iN = (1.0 - dx) * iNW + dx * iNE
    iS = (1.0 - dx) * iSW + dx * iSE
    return (1.0 - dy) * iN + dy * iS


def place_on_land():
    placed = False
    while not placed:
        x = libtcod.random_get_int(0, 0, R.world.w - 1)
        y = libtcod.random_get_int(0, 0, R.world.h - 1)
        tile = R.world.tiles[x][y]
        if tile.POI is None and tile.blocked is not True:
            return x, y


def render():
    for y in range(R.SCREEN_HEIGHT):
        for x in range(R.SCREEN_WIDTH):
            #             r = int(libtcod.heightmap_get_value(map_.hm, x, y))
            #             g = int(libtcod.heightmap_get_value(map_.hm, x, y))
            if x < R.MAP_WIDTH and y < R.MAP_HEIGHT:
                b = int(map_.tiles[x][y].humidity)
                colour = libtcod.Color(30, 30, int(b))
                libtcod.console_set_char_background(con, x, y, colour)

                if len(map_.wind_gen.map[x][y]) > 0:
                    libtcod.console_set_char(con, x, y, ".")
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
                colour = libtcod.Color(int(b), int(c), int(b))
                libtcod.console_set_char_background(con, x, y, colour)

            if x >= R.MAP_WIDTH and y >= R.MAP_HEIGHT:
                ax = x - R.MAP_WIDTH
                ay = y - R.MAP_HEIGHT
                b = int(map_.tiles[ax][ay].temperature)
                colour = libtcod.Color(int(b), int(b), int(b))
                libtcod.console_set_char_background(con, x, y, colour)

    libtcod.console_blit(con, 0, 0, R.SCREEN_WIDTH, R.SCREEN_HEIGHT, 0, 0, 0)

    libtcod.console_flush()


def handle_mouse():
    mouse = libtcod.mouse_get_status()

    (x, y) = (mouse.cx, mouse.cy)

    if x > R.MAP_WIDTH - 1:
        x = R.MAP_WIDTH - 1
    if y > R.MAP_HEIGHT - 1:
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

####FOR TESTING~~~~~
def main():
    global key, mouse, map_, con

    R.SCREEN_WIDTH = 100
    R.SCREEN_HEIGHT = 80
    libtcod.console_set_custom_font("data\ont_big.png", libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(R.SCREEN_WIDTH, R.SCREEN_HEIGHT, "Trader-RL", False)
    libtcod.sys_set_fps(R.LIMIT_FPS)
    con = libtcod.console_new(R.SCREEN_WIDTH, R.SCREEN_HEIGHT)

    map_ = Map(R.MAP_WIDTH, R.MAP_HEIGHT)
    map_.wind_gen.run_simulation(500)

    mouse = libtcod.Mouse()
    key = libtcod.Key()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        render()

        player_action = handle_keys()
        if player_action == "exit":
            break

        handle_mouse()


#cProfile.run('main()')  
# main()
#

#buh = Dungeon(0,0,1)       
        
        
    
    
        