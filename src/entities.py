"""
Created on 16 Mar 2013

@author: Emily
"""
import math

import libtcodpy as libtcod
import R
import sentient


class Object:
    def __init__(self, x=0, y=0, char="@", name="blob", colour=libtcod.white, blocks=False, always_visible=False,
                 item=None, type="object"):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.type = type
        self.colour = colour
        self.blocks = blocks
        self.always_visible = always_visible

    def clear(self, cam_x=0, cam_y=0):
        # erase the character that represents this object
        libtcod.console_put_char(R.con_char, self.x - cam_x, self.y - cam_y, " ", libtcod.BKGND_NONE)

    def draw_faded(self, cam_x, cam_y):
        pos_x = self.x - cam_x
        pos_y = self.y - cam_y

        colour = libtcod.Color(self.colour.r, self.colour.g, self.colour.b)
        libtcod.color_scale_HSV(colour, 0.7, 0.7)  # hopefully 80% saturation.
        libtcod.console_set_default_foreground(R.con_char, colour)
        libtcod.console_put_char(R.con_char, pos_x, pos_y, self.char, libtcod.BKGND_NONE)  # ADDALPHA(0.0))

    #
    def draw(self, cam_x, cam_y):
        #
        # if self.x >= cam_x and self.x < R.MAP_VIEW_WIDTH and self.y >= cam_y and self.y < R.MAP_VIEW_HEIGHT:
        #
        pos_x = self.x - cam_x
        pos_y = self.y - cam_y

        libtcod.console_set_default_foreground(R.con_char, self.colour)
        libtcod.console_put_char(R.con_char, pos_x, pos_y, self.char, libtcod.BKGND_NONE)


class Mover(Object):
    def __init__(self, x=0, y=0, char="@", name="blob", colour=libtcod.white, blocks=False, always_visible=False,
                 fighter=None, you=None, pather=None, ai=None):
        Object.__init__(self, x, y, char, name, colour, blocks, always_visible)
        self.direction = "S"

        self.activity_log = {"history": [], "kills": [], "travels": [], "transactions": []}

        self.fighter = fighter
        if fighter:
            self.fighter.parent = self

        self.inventory = sentient.Inventory()  # not entirely sure where this needs to go.

        self.you = you  # WHAT
        if you:
            self.you.parent = self

        # THIS HAS BEEN MOVED INTO AI. AS thIS IS WHERE IT WILL BE USED.
        self.pather = pather
        if pather:
            self.pather.parent = self

        self.ai = ai
        if ai:
            self.ai.parent = self


    def move(self, dx, dy):
        # move by the given quantity, if the destination is not blocked
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            return True
        return False

    def move_p(self, dx, dy):
        # move by the given quantity
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y):
        # vector from this object to the other and the distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance(self, x, y):
        # return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


def is_blocked(x, y):
    # first test the map tile
    if x > len(R.tiles) - 1 or x < 0:
        return True
    if y > len(R.tiles[x]) - 1 or y < 0:
        return True
    if R.world.tiles[x][y].blocked:
        return True
    #now check for any blocking objects
    for object_ in R.world_obj:
        if object_.blocks and object_.x == x and object_.y == y:
            return True
    return False