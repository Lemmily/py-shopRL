__author__ = 'lemmily'

import random
import threading
import time

from src import R
from src.entities import Object

__author__ = 'emily'

import libtcodpy as libtcod


class Thread(threading.Thread):
    NUM = 0

    def __init__(self, target=None, args=(), name=""):
        threading.Thread.__init__(self, target=target, args=args)
        self.NUM += 1
        self.name = "Thread " + str(self.NUM)


# Game object!


class Game():
    def __init__(self, console):
        self.console = console
        self.you = R.you = Object()
        self.local = True  # zoom level
        self.render_thread = Thread(target=self.render, name="Render Thread")

        self.update_thread = None
        R.map_ = self.map = [[0 for _ in xrange(R.SCREEN_HEIGHT)] for _ in xrange(R.SCREEN_WIDTH)]

    def run(self):
        global key, mouse
        mouse = libtcod.Mouse()
        key = libtcod.Key()

        libtcod.console_set_default_foreground(self.console, libtcod.white)
        libtcod.console_print_ex(self.console, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, "hello")

        self.render_thread.start()
        while not libtcod.console_is_window_closed():
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

            self.handle_mouse()
            self.handle_keyboard()
            self.update()
            # self.render_all()
            # libtcod.console_blit(self.console, 0, 0, R.SCREEN_WIDTH, R.SCREEN_HEIGHT, 0, 0, 0, 1.0, 0.7)
            # libtcod.console_flush()

        R.playing = False

    def render(self):
        while R.playing:
            print "render"
            if self.local:
                self.render_local()
            else:
                self.render_world()
            libtcod.console_blit(self.console, 0, 0, R.MAP_VIEW_WIDTH, R.MAP_VIEW_HEIGHT, 0, 0, 0)
            # # libtcod.console_blit(con_char, 0, 0, R.MAP_VIEW_WIDTH, R.MAP_VIEW_HEIGHT, 0, 0, 0, 1.0, 0.0)
            # # libtcod.console_blit(inf, 0, 0, R.INFO_BAR_WIDTH, R.SCREEN_HEIGHT, 0, R.MAP_VIEW_WIDTH, 0)
            # # libtcod.console_blit(minmap, 0, 0, R.INFO_BAR_WIDTH, R.PANEL_HEIGHT, 0, R.MAP_VIEW_WIDTH, R.PANEL_Y)
            libtcod.console_flush()
            time.sleep(0.1)  # 1/1000 * 60)

    def render_all(self):
        global cam_x, cam_y

        # find the NEW camera position
        # cam_x = scrolling_map(self.you.x, R.MAP_VIEW_WIDTH / 2, R.MAP_VIEW_WIDTH, R.MAP_WIDTH)
        # cam_y = scrolling_map(self.you.y, R.MAP_VIEW_HEIGHT / 2, R.MAP_VIEW_HEIGHT, R.MAP_HEIGHT)
        while R.playing:
            for x in xrange(R.SCREEN_WIDTH):
                for y in xrange(R.SCREEN_HEIGHT):
                    if self.map[x][y] == 0:
                        libtcod.console_set_char(self.console, x, y, " ")
                        libtcod.console_set_char_background(self.console, x, y, libtcod.light_chartreuse,
                                                            libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char(self.console, x, y, ".")
                        libtcod.console_set_char_background(self.console, x, y, libtcod.dark_red, libtcod.BKGND_SET)
            # print "renderrrrred"
            time.sleep(0.1)  # 1/1000 * 60)

    def render_local(self):
        global cam_x, cam_y

        for x in xrange(R.SCREEN_WIDTH):
            for y in xrange(R.SCREEN_HEIGHT):
                if self.map[x][y] == 0:
                    libtcod.console_set_char(self.console, x, y, " ")
                    libtcod.console_set_char_background(self.console, x, y, libtcod.brass, libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char(self.console, x, y, "8")
                    libtcod.console_set_char_background(self.console, x, y, libtcod.dark_red, libtcod.BKGND_SET)

    def render_world(self):
        for x in xrange(R.SCREEN_WIDTH):
            for y in xrange(R.SCREEN_HEIGHT):
                if self.map[x][y] == 0:
                    libtcod.console_set_char(self.console, x, y, " ")
                    libtcod.console_set_char_background(self.console, x, y, libtcod.light_chartreuse, libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char(self.console, x, y, ".")
                    libtcod.console_set_char_background(self.console, x, y, libtcod.dark_red, libtcod.BKGND_SET)

    def handle_mouse(self):
        mouse = libtcod.mouse_get_status()

        (x, y) = (mouse.cx, mouse.cy)

        if mouse.lbutton_pressed:
            if x < len(self.map) and y < self.map[0]:
                print x, y, "tile is", self.map[x][y]
        if mouse.rbutton_pressed:
            Thread(target=func, args=self.map).start()

        if mouse.mbutton_pressed:
            # Thread(target=wipe_func, args=self.map).start()
            self.local = not self.local

    def update(self):
        print "updating"
        time.sleep(1)
        # pass

    def handle_keyboard(self):
        pass


def wipe_func(*tile_map):
    if tile_map is None:
        tile_map = R.map_

    print "Thread", id, "is wiping the map."
    for x in xrange(len(tile_map)):
        for y in xrange(len(tile_map[0])):
            tile_map[x][y] = 0


def func(*tile_map):
    if tile_map is None:
        tile_map = R.map_
    # else:
    #     tile_map = tile_map[0]
    print("Thread", id)
    time.sleep(random.random() * 1)
    x = random.randint(0, len(tile_map) - 1)
    y = random.randint(0, len(tile_map[0]) - 1)
    print x, y, "changed to 1"
    R.map_[x][y] = 1
    tile_map[x][y] = 1


def scrolling_map(p, hs, s, m):
    """
   Get the position of the camera in a scrolling map:

    - p is the position of the player.
    - hs is half of the screen size
    - s is the full screen size.
    - m is the size of the map.
   """
    if p < hs:
        return 0
    elif p > m - hs:
        return m - s
    else:
        return p - hs

        #
        # class CalculationThread(Thread):
        #     def __init__(self, p_target):
        #         super(target=p_target)
