'''
Created on 16 Mar 2013

@author: Emily
'''

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 80

LIMIT_FPS = 20

INFO_BAR_WIDTH = 25

MAP_VIEW_WIDTH = SCREEN_WIDTH - INFO_BAR_WIDTH
MAP_VIEW_HEIGHT = 40

MAP_WIDTH = 200
MAP_HEIGHT = 180

# BAR_WIDTH = 20
PANEL_HEIGHT = SCREEN_HEIGHT - MAP_VIEW_HEIGHT
PANEL_WIDTH = SCREEN_WIDTH - INFO_BAR_WIDTH
# PANEL_X = SCREEN_WIDTH - PANEL_WIDTH
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = 2
MSG_WIDTH = SCREEN_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

con = None
con_char = None
message_bar = None
inf = None
minmap = None

SLOW_SPEED = 8
NORM_SPEED = 12
FAST_SPEED = 20

game_speed = NORM_SPEED
date = []
turns = 0
pause = False

ui = None

game_msgs = []
cities = []

world = None
tiles = []
world_obj = []

resource_list = ["raw",
                 "produce",
                 "trade"]
