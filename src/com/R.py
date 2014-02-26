'''
Created on 16 Mar 2013

@author: Emily
'''


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60

LIMIT_FPS = 20


INFO_BAR_WIDTH = 25

MAP_VIEW_WIDTH = SCREEN_WIDTH - INFO_BAR_WIDTH
MAP_VIEW_WIDTH_HALF = MAP_VIEW_WIDTH / 2
MAP_VIEW_HEIGHT = 40
MAP_VIEW_HEIGHT_HALF = 20

MAP_WIDTH = 200  
MAP_HEIGHT = 120

#BAR_WIDTH = 20
PANEL_HEIGHT = SCREEN_HEIGHT - MAP_VIEW_HEIGHT
PANEL_WIDTH = SCREEN_WIDTH - INFO_BAR_WIDTH
#PANEL_X = SCREEN_WIDTH - PANEL_WIDTH
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
msg_redraw = False
game_msgs = []

you = None #the player
inventory = []

cities = []
pois = []

world = None
map_ = []
tiles = []
world_obj = []
locale = None
locale_obj = []
player_pos = (0,0)

resource_list = [   "raw",
                    "produce",
                    "trade"]

skill_list = [ #// 0_name:string, 1_attribute, 2_needTraining:Boolean, 3_desc:String,[4_dependsOn],[5_dependants]
                ["Appraise", "int", False, "Used to analyse an item for monetary value, and contributing factors",["none"],["none"]],
                ["Armour", "str", False, "How well you can wear armour. Negates some of the penalties of heavier armour",["none"],["none"]],
                ["Dodge", "dex", False, "Improves your chance of dodging attacks and traps",["none"],["none"]],
                ["Fighting", "dex", False, "Improves your chance of hitting and your damage in melee",["none"],["none"]],
                ]
