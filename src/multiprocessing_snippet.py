__author__ = 'Emily'


# !/usr/bin/env python


##class threadhandler(threading.Thread):
####    def __init__(self, thread, queue):
####        threading.thread.__init__(self)
####        self.thread = thread[0]
####        self.args = thread[1]
####        self.queue = queue
##    def run(self):
##        while True:
##            task = pool.get()
##            if task != None:
##                thread = task[0]
##                args = task[1]
##                threading.Thread(target=thread, args=args).start()
##                pool.task_done()

# threading.Thread(target=your_function).start()

##class Collision(threading.Thread):
##    def __init__(self, queue, x, y):
##        threading.thread.__init__(self)
##        self.queue = queue
##        self.x = x
##        self.y = y
##
##    def run(self):
##        global map
##        incrementor = 0
##        if not map[self.x][self.y].blocked:
##            map[self.x][self.y].clearance = 1
##            incrementor += 1
##            increase = True
##            while increase == True:
##                for iy in range(self.y, (self.y + incrementor + 1)):
##                    if map[self.x + incrementor][iy].blocked:
##                        increase = False
##                for ix in range(self.x, (self.x + incrementor + 1)):
##                    if map[ix][self.y + incrementor].blocked:
##                        increase = False
##                if increase == True:
##                    map[self.x][self.y].clearance += 1
##                    incrementor += 1
##                else:
##                    increase = False
##                    incrementor = 0

# original function, the ix/iy loops are for checked the new edges every time you expand the square
##def make_collision():
##    global map
##    incrementor = 0
##    for y in range(MAP_HEIGHT):
##        for x in range(MAP_WIDTH):
##            if not map[x][y].blocked:
##                map[x][y].clearance = 1
##                incrementor += 1
##                increase = True
##                while increase == True:
##                    for iy in range(y, (y + incrementor + 1)):
##                        if map[x + incrementor][iy].blocked:
##                            increase = False
##                    for ix in range(x, (x + incrementor + 1)):
##                        if map[ix][y + incrementor].blocked:
##                            increase = False
##                    if increase == True:
##                        map[x][y].clearance += 1
##                        incrementor += 1
##                    else:
##                        increase = False
##                        incrementor = 0
from multiprocessing import *
import time

import libtcodpy as libtcod


# actual size of the window
SCREEN_WIDTH = 46
SCREEN_HEIGHT = 20

# size of the map
MAP_WIDTH = 46
MAP_HEIGHT = 20

color_dark_wall = libtcod.Color(50, 50, 50)
color_dark_ground = libtcod.Color(150, 150, 150)


class Tile:
    # a tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.clearance = 0

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight


smap = ['##############################################',
        '#######################      #################',
        '#####################    #     ###############',
        '######################  ###        ###########',
        '##################      #####             ####',
        '################       ########    ###### ####',
        '###############      #################### ####',
        '################    ######                  ##',
        '########   #######  ######   #     #     #  ##',
        '########   ######      ###                  ##',
        '########                                    ##',
        '####       ######      ###   #     #     #  ##',
        '#### ###   ########## ####                  ##',
        '#### ###   ##########   ###########=##########',
        '#### ##################   #####          #####',
        '#### ###             #### #####          #####',
        '####           #     ####                #####',
        '########       #     #### #####          #####',
        '########       #####      ####################',
        '##############################################',
        ]


def make_map():
    global map

    # fill map with "unblocked" tiles
    map = [[Tile(False)
            for y in range(MAP_HEIGHT)]
           for x in range(MAP_WIDTH)]
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if smap[y][x] == "#":
                map[x][y].blocked = True


def render_all():
    global color_light_wall
    global color_light_ground

    # go through all tiles, and set their background color
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].blocked
            if wall:
                libtcod.console_set_char_background(0, x, y, color_dark_wall, libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(0, x, y, color_dark_ground, libtcod.BKGND_SET)
            if map[x][y].clearance >= 1:
                libtcod.console_put_char(0, x, y, str(map[x][y].clearance), libtcod.BKGND_NONE)


def make_clearance(x, y):
    global map
    incrementor = 0
    if not map[x][y].blocked:
        map[x][y].clearance = 1
        incrementor += 1
        increase = True
        while increase == True:
            for iy in range(y, (y + incrementor + 1)):
                if map[x + incrementor][iy].blocked:
                    increase = False
            for ix in range(x, (x + incrementor + 1)):
                if map[ix][y + incrementor].blocked:
                    increase = False
            if increase == True:
                map[x][y].clearance += 1
                incrementor += 1
            else:
                increase = False
                incrementor = 0

##pool = Queue.Queue()
##if not libtcod.console_is_window_closed():
if __name__ == '__main__':
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
    # generate map (at this point it's not drawn to the screen)
    make_map()
    pool = Pool(processes=4)
    start = time.time()  # timing test for later, ignore.
    ##    for x in range(4):
    ##        threadhandler().start()
    ##    for y in range(MAP_HEIGHT):
    ##        for x in range(MAP_WIDTH):
    ##            pool.put((make_clearance,(x,y)))
    ##    pool.join()
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            pool.apply_async(make_clearance, (x, y))
    print "Elapsed Time: %s" % (time.time() - start)
    # render the screen
    render_all()
    libtcod.console_flush()
    key = libtcod.console_wait_for_keypress(True)
