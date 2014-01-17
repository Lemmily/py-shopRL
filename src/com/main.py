'''
Created on 4 Mar 2013

@author: Emily
'''
import libtcodpy as libtcod
#import math
import shelve
#import random
import R
import UI
import worldMap
import entities
from R import con_char, inf#, #map_

import cProfile
import pstats
import sentient

#import numpy as np
#import numpy

SLOW_SPEED = 8
NORM_SPEED = 12
FAST_SPEED = 20
FASTEST_SPEED = 30

game_speed = NORM_SPEED
turns = 0
pause = False
traffic = False
temperature = False
continent = False


local = False

debug_mode = False

libtcod.namegen_parse('data/names.txt')
         
DAYS =  [
        ['Monday', 1],
        ['Tuesday', 2],
        ['Wednesday', 3],
        ['Thursday', 4],
        ['Friday', 5],
        ['Saturday', 6],
        ['Sunday', 7]
        ]

MONTHS = [
        ['January',1, 31],
        ['February',2, 28],
        ['March',3, 31],
        ['April',4, 30],
        ['May',5, 31],
        ['June',6, 30],
        ['July',7, 31],
        ['August',8, 31],
        ['September',9, 30],
        ['October',10, 31],
        ['November',11, 30],
        ['December',12, 31],
        ]

master_resource_list = [    "wool", "cloth", "clothes", 
                            "wood", "food", "ore", 
                            "metal", "tools", "weapons"];
                            


def new_game():
    global game_msgs, test_msgs,  ui, game_state
    global world, world_obj, cities, pois, you, selected
    global tiles, cam_x,cam_y
    global key, mouse
    global map_, local, fov_recompute
    global debug_mode
    
     
    debug_mode = False
    mouse = libtcod.Mouse()
    key = libtcod.Key()
    
    cam_x,cam_y = 0,0
    game_state = "playing"
    test_msgs = []
    world = R.world = worldMap.Map(R.MAP_WIDTH,R.MAP_HEIGHT)
    
    world_obj = R.world_obj = []
    tiles = R.tiles = world.tiles
    #make_map()
    pois = R.pois = world.pois
    cities = R.cities = world.cities
    R.ui.message(str(len(cities)) + " cities have been made!", libtcod.green)
    for city in cities: 
        #print city.name + str(city.x) + "/" +  str(city.y)
        R.ui.message(city.name + str(city.x) + "/" +  str(city.y), libtcod.light_grey)
        city.createBaseRelationships(cities)
    
#    for n in range(5):
#        city = City(name = libtcod.namegen_generate("city"), resource_list =master_resource_list)
#        cities.append(city)
#    city = None
#    for city in cities:
#        city.createBaseRelationships(cities)
    selected = []
    you = R.you = entities.Player()#name = "player") #you = entities.Player())
    R.inventory = you.inventory
    world_obj.append(you)
    for a in range(5):
        x, y = worldMap.place_on_land()
        hero = R.hero = entities.Mover(x=x,y=y,name = "hero " + str(a), pather = sentient.Pather(), ai= sentient.AI_Hero())
        world_obj.append(hero)
    render_all()
    
        
    world.connect_cities()
    world.connect_cities()
    world.connect_cities()
#    point = (0,0)
#    diction = dict()
#    diction[(0,0)] = 10
#    print str(diction[point])
    
    local = False
    fov_recompute = False
    #path = hero.pather.find_path((10,10),(0,0))
    R.ui.message("Finished init", libtcod.blue)
    
def load_game():
    global date, cities, test_msgs, game_msgs
    save_file = shelve.open("savegame", "r")
    date = save_file["date"]
    cities = save_file["cities"]
    test_msgs = save_file["test_msgs"]
    game_msgs = save_file["game_msgs"]
    save_file.close()


def save_game():
    
    save_file = shelve.open("savegame", "n")
    save_file["date"] = date
    save_file["cities"] = cities
    save_file["test_msgs"] = test_msgs
    save_file["game_msgs"] = game_msgs
    save_file.close()
    
def play_game():
    global key,mouse
    
    mouse = libtcod.Mouse()
    key = libtcod.Key()
    
        
    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)
        #render the screen
        if not local:
            render_all()
            
            ##Clear the characters from screen.
            for object_ in R.world_obj:
                object_.clear(cam_x,cam_y)
                
            for city in cities:
                for merchant in city.trade_house.caravans_out:
                    merchant.clear(cam_x,cam_y)
                  
            #handles the keys and exit if needed.
            player_action = handle_keys()
            if player_action == "exit":
                save_game()
                break         
            if not pause: #and not player_turn:
                advance_time(); 
            
            handle_mouse()
            libtcod.console_clear(R.con);
            libtcod.console_clear(R.con_char);
                
        else:
            render_local()
            
#            for object_ in R.locale_obj:
#                object_.clear(cam_x,cam_y)
#            
#            you.clear(cam_x, cam_y)
            
            #handles the keys and exit if needed.
            player_action = handle_keys()
            if player_action == "exit":
                save_game()
                break         
            
            handle_mouse()
            
        if R.msg_redraw == True:
            update_msg_bar()
        
        
        
        #update_info_bar()
        
        #erase all objectsat their old locations, before they move
        #for object in objects:
        #    object.clear(con)
          
        #handle_mouse()
        
def advance_time():
    global date, sub_turns, turns
    
    turns += game_speed;
    if turns >= 60: #// pass an hour.11
        turns = 0
        #whenever the date/time changes:-
        #render_all()
        for objects in R.world_obj:
                if objects.ai:
                    objects.clear(cam_x,cam_y)
                    objects.ai.take_turn()
                    objects.draw(cam_x,cam_y)  
        update_info_bar()
        
        ####
        #####do any Hourly action here.
        ####
        
        date[0] += 1; #//increase hour
        #//passHour();
        #if  ( date[0] % 3 ) == 0: 
#            print "the time is ", str(date[0])
#            for city in cities:
#                for merchant in city.trade_house.caravans_out:
#                    #merchant.clear(cam_x,cam_y)
#                    merchant.ai.take_turn()
#                    #merchant.draw(cam_x,cam_y)

        if  ( date[0] % 3 ) == 0: 
            print "the time is ", str(date[0])
            city = cities[0]
            for merchant in city.trade_house.caravans_out:
                merchant.clear(cam_x,cam_y)
                merchant.ai.take_turn()
                
            for city in cities:
                city.productionRound_temp()
                
    if date[0] == 24:#// increase the day.
        
        for city in cities:
            city.productionRound_temp()
            for resource in R.resource_list:
                city.trade_house.collect_info(resource)
                other_city = city
                while other_city == city:
                    other_city = cities[libtcod.random_get_int(0, 0, len(cities)-1)]
                city.trade_house.resolve_offers_city(resource, other_city)
            #for merchant in city.trade_house.caravans_in:
                #merchant.take_turn()
                
        oldDay = date[1][1];
            
        newDay = oldDay + 1;
        if newDay > 7:
            #does this work weekly?
            newDay = 1;
        date[0] = 0; #//set hours back to 0;
        date[1][0] = DAYS[newDay - 1][0]; #increade day name
        date[1][1] = newDay; #//change day reference value
        date[1][2] += 1; #//increase the date by a day.
        
    
    if date[1][2] > date[2][2]: #// if current day is more than the months max days, increase month.
        oldMonth = date[2][1];
        newMonth = oldMonth + 1;
        
        if newMonth >= 12: 
            newMonth = 1;
        
        date[1][2] = 1;
        date[2][0] = MONTHS[newMonth - 1][0]; #/change month name
        date[2][1] = MONTHS[newMonth - 1][1]; #//change month date value
        date[2][2] = MONTHS[newMonth - 1][2]; #//change max days in month.
    
    if date[2][1] > 12: #//if the month is over 12, increase the year/
                
        date[2][0] = MONTHS[0][0]; #//change month name to first month
        date[2][1] = MONTHS[0][1]; #//change month date value to first month
        date[2][2] = MONTHS[0][2]; #//change max days in month to first month's
        date[3] += 1; #//increase year
        
        ##
        ### Do anything that needs to be the start of the year here. AND use the new year
        ## 
    update_msg_bar()
    
def scrolling_map(p, hs, s, m):
    """
    Get the position of the camera in a scrolling map:

     - p is the position of the player.
     - hs is half of the screen size
     - s is the full screen size.
     - m is the size of the map.
    """
    if p < hs or m < s:
        return 0
    elif p > m - hs:
        return m - s
    else:
        return p - hs     
                  
    
def render_all():
    global cam_x, cam_y
    
    #clear the city locations using OLD cam position.
    for city in R.cities:
        loc = R.tiles[city.x][city.y]
        colour = loc.bg
        libtcod.console_set_char_background(con, cam_x+city.x, cam_y+city.y, colour, libtcod.BKGND_SET )
        libtcod.console_set_char(con, cam_x+city.x, cam_y+city.y, ord(' '))
        
    cam_x = scrolling_map(you.x, R.MAP_VIEW_WIDTH/2 +1, R.MAP_VIEW_WIDTH, R.MAP_WIDTH)
    cam_y = scrolling_map(you.y, R.MAP_VIEW_HEIGHT/2, R.MAP_VIEW_HEIGHT, R.MAP_HEIGHT)
    #now draw the map!
    for y in range(min(R.MAP_VIEW_HEIGHT, len(R.world.tiles[0]))): #this refers to the SCREEN position. NOT map.
        for x in range(min(R.MAP_VIEW_WIDTH, len(R.world.tiles))):
            map_pos_x = x + cam_x
            map_pos_y = y + cam_y
            while map_pos_x >= R.MAP_WIDTH:
                map_pos_x -=  1
            while map_pos_y >= R.MAP_HEIGHT:
                map_pos_y -= 1
            
            tile = R.world.tiles[map_pos_x][map_pos_y]
             
            #visible = libtcod.map_is_in_fov(fov_map, tile.x, tile.y)
            visible = True
            #wall = tile.block_sight
                
            if not visible:
                pass #TODO: re-do the visible/ not visible code.
                #if it"s not visible right now, the player can only see it if it"s explored
                #if tile.explored:
                    #if wall:
                    #    libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET)
                    #    libtcod.console_set_char(con, x, y, " ")
                    #else:
                    #    libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)
                    #    libtcod.console_set_char(con, x, y, " ")
            else:
                #it"s visible
                if tile.POI is None:
                    if traffic: # for b&w image.
                        v = world.get_foot_traffic(map_pos_x,map_pos_y)
                        colour = libtcod.Color(v,v,v)
                        libtcod.console_set_char_background(con, x, y, colour, libtcod.BKGND_SET )
                        libtcod.console_set_char(con, x, y, " ")
                        
                    elif temperature: # for b&w image.
                        v = world.get_temperature(map_pos_x,map_pos_y)
                        v = int(v)
                        colour = libtcod.Color(v,v,v)
                        libtcod.console_set_char_background(con, x, y, colour, libtcod.BKGND_SET )
                        libtcod.console_set_char(con, x, y, " ")
                    
                    elif continent:
                        m = 255 / len(R.world.continents)
                        if tile.type != "water":
                            v = tile.continent * m 
                            colour = libtcod.Color(v,v,v)
                        else:
                            colour = tile.bg
                        libtcod.console_set_char_background(con, x, y, colour, libtcod.BKGND_SET )
                        libtcod.console_set_char(con, x, y, " ")
                    
                    else:
                        colour = tile.bg
                        libtcod.console_set_char(con, x, y, " ")
                        libtcod.console_set_char_background(con, x, y, colour, libtcod.BKGND_SET )
                    #libtcod.console_set_char_foreground(con, x, y, libtcod.black)
                    #libtcod.console_set_char(con, x, y, libtcod.CHAR_BULLET)
                else:
                    libtcod.console_set_char_background(con, x, y, tile.POI.colour, libtcod.BKGND_SET )
                    libtcod.console_set_char_foreground(con, x, y, libtcod.white)
                    libtcod.console_set_char(con, x, y, tile.POI.char)
                #since it"s visible, explore it
                tile.explored = True
    
    #now draw the mini map
    for cell_x in range(len(world.mini_map)):
        for cell_y in range(len(world.mini_map[cell_x])):
            colour = world.mini_map[cell_x][cell_y].bg
            libtcod.console_set_char_background(minmap, cell_x, cell_y, colour, libtcod.BKGND_SET )
            #libtcod.console_set_char_foreground(con, x, y, libtcod.white)

#    for char in R.world_obj:
#        if char != you:
#            char.draw(cam_x, cam_y)
    #now draw all the merchants
    for city in cities:
        for merchant in city.trade_house.caravans_out:
            merchant.draw(cam_x,cam_y)
    for objects in R.world_obj:
        if objects.ai:
            objects.clear(cam_x,cam_y)   
            objects.draw(cam_x,cam_y)        
    you.draw(cam_x, cam_y)
    
#    libtcod.console_clear(message_bar)
#    libtcod.console_set_default_foreground(message_bar, libtcod.white)
#    libtcod.console_print_ex(message_bar, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, str(date[0]) + " " + str(date[1][2]) + " " + str(date[1][0]) + " " + str(date[2][0]))
#    # print the messages, one line at a time.
#    y = 2
#    for (line, colour) in R.game_msgs:
#        libtcod.console_set_default_foreground(message_bar, colour)
#        libtcod.console_print_ex(message_bar, R.MSG_X, R.MSG_HEIGHT - y, libtcod.BKGND_NONE, libtcod.LEFT, line)
#        y += 1
#    y = 0
#    for y in range(R.MAP_HEIGHT):
#        for x in range(R.MAP_WIDTH):
#            libtcod.console_set_char_background(con, x, y, map_[x][y].bg, libtcod.BKGND_SET)
    
    #libtcod.console_print_ex(message_bar, R.SCREEN_WIDTH - R.INFO_BAR_WIDTH, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())         
    
    libtcod.console_blit(con, 0, 0, R.MAP_VIEW_WIDTH, R.MAP_VIEW_HEIGHT, 0, 0, 0)
    libtcod.console_blit(con_char, 0, 0, R.MAP_VIEW_WIDTH, R.MAP_VIEW_HEIGHT, 0, 0, 0, 1.0, 0.0)
    libtcod.console_blit(inf, 0, 0, R.INFO_BAR_WIDTH, R.SCREEN_HEIGHT, 0,R.MAP_VIEW_WIDTH,0)
    libtcod.console_blit(minmap, 0, 0, R.INFO_BAR_WIDTH, R.PANEL_HEIGHT, 0,R.MAP_VIEW_WIDTH,R.PANEL_Y)
    libtcod.console_flush()


def render_local():
    global map_, fov_recompute
    cam_x = scrolling_map(you.x, R.MAP_VIEW_WIDTH_HALF + 1, R.MAP_VIEW_WIDTH, R.MAP_WIDTH)
    cam_y = scrolling_map(you.y, R.MAP_VIEW_HEIGHT_HALF, R.MAP_VIEW_HEIGHT, R.MAP_HEIGHT)
    
    if fov_recompute:
        fov_recompute = False
        libtcod.map_compute_fov(R.locale.floors[you.depth].fov_map, you.x, you.y, 10, True, 0)
        
        for y in range(R.MAP_VIEW_HEIGHT): #this refers to the SCREEN position. NOT map.
            for x in range(R.MAP_VIEW_WIDTH):
                map_x = x + cam_x
                map_y = y + cam_y
                
                if map_x < len(R.map_) and map_y < len(R.map_[0]): # and x < len(R.map_) and y < len(R.map_[0]):  #if it's within the bounds of the map.
                    tile = R.locale.floors[you.depth].tiles[map_x][map_y]
                    visible = libtcod.map_is_in_fov(R.locale.floors[you.depth].fov_map, map_x, map_y)
                    
                    if not visible:
                        if tile.explored or debug_mode:
                            libtcod.console_put_char_ex(con, x, y, tile.char, libtcod.dark_green, libtcod.dark_gray)
                        else:
                            libtcod.console_put_char_ex(con, x, y, " ", libtcod.black, libtcod.black)
                        libtcod.console_set_char(con_char, x, y, " ") #clear any objects away
                        
                    else:
                        libtcod.console_put_char_ex(con, x, y, tile.char, libtcod.green, libtcod.light_grey)
                        libtcod.console_set_char(con_char, x, y, " ")
                        tile.explored = True
                else:
                    libtcod.console_put_char_ex(con, x, y, " ", libtcod.black, libtcod.black)
                    libtcod.console_set_char(con_char, x, y, " ")
                    
                    
        for objects in R.locale_obj:
            #if the tile is explored, then draw the object.
            if libtcod.map_is_in_fov(R.locale.floors[you.depth].fov_map, objects.x, objects.y):
                objects.draw(cam_x,cam_y)   
                
            elif R.locale.floors[you.depth].tiles[objects.x][objects.y].explored == True:
                objects.draw_faded(cam_x,cam_y)
        you.draw(cam_x, cam_y)
        
    libtcod.console_blit(con, 0, 0, R.MAP_VIEW_WIDTH, R.MAP_VIEW_HEIGHT, 0, 0, 0)
    libtcod.console_blit(con_char, 0, 0, R.MAP_VIEW_WIDTH, R.MAP_VIEW_HEIGHT, 0, 0, 0, 1.0, 0.0)
    libtcod.console_flush()  
    

def is_wall(x, y, map_= None):
    
    if map_== None:
        map_= R.map_
        
    if 0 <= x < len(map) and 0 <= y < len(map[x]):
        if map[x][y] != 0:
            return True
        else:
            return False
    else:
        return False
    
def clear_consoles():
    for x in range(R.MAP_VIEW_WIDTH): #this refers to the SCREEN position.
        for y in range(R.MAP_VIEW_HEIGHT):
            libtcod.console_set_char(con, x, y, " ")
            libtcod.console_set_char(con_char, x, y, " ")
            
def update_msg_bar():
    
    libtcod.console_clear(message_bar)
    libtcod.console_set_default_foreground(message_bar, libtcod.white)
    libtcod.console_print_ex(message_bar, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_date())
    # print the messages, one line at a time.
    y = 2
    for (line, colour) in R.game_msgs:
        libtcod.console_set_default_foreground(message_bar, colour)
        libtcod.console_print_ex(message_bar, R.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1          
    libtcod.console_blit(message_bar, 0, 0, R.PANEL_WIDTH, R.PANEL_HEIGHT, 0 , 0, R.PANEL_Y)
    libtcod.console_flush()  
    R.msg_redraw = False
        
        
def get_date():
    return str(date[0]) + " " + str(date[1][0]) + " " + str(date[1][2]) + " " + str(date[2][0])

def update_info_bar():
    
    #TODO: seperate the UI updating into THIS function. the rest of the game updates in the render_all.
    # Fetch all the code into this function basically.
    #TODO: make a function for the ui to prin a message in this area. Possibly with choices whether to wipe it first or add to it.
              
    libtcod.console_clear(inf)
    y = 2 
            
    if len(selected) > 0:
        for sel in selected:
            libtcod.console_print_ex(inf, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, sel.name)
            libtcod.console_print_ex(inf, 0, y+1, libtcod.BKGND_NONE, libtcod.LEFT, sel.type)
            y += 2
            
            try: 
                if sel.component.trade_house:
                    libtcod.console_print_ex(inf, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, sel.char)
                    resources = [obj + " " + str(sel.component.resources[obj][1]) for obj in sel.component.resources] 
                    
                    resources = "\n".join(resources)
                    libtcod.console_print_ex(inf, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, resources)
                    y += 1
            except:
                libtcod.console_print_ex(inf, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, sel.char)
        
        y += 4
    for (line, colour) in test_msgs:
        
        libtcod.console_set_default_foreground(inf, colour)
        libtcod.console_print_ex(inf, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1
#    y = 1 
#    for (line, colour) in test_msgs:
#        libtcod.console_set_default_foreground(inf, colour)
#        libtcod.console_print_ex(inf, 2, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
#        y += 1

    libtcod.console_blit(inf, 0, 0, R.INFO_BAR_WIDTH, R.SCREEN_HEIGHT, 0,R.MAP_VIEW_WIDTH,0)
    libtcod.console_flush()
   
#def get_names_under_mouse():
#    global mouse
#
#    (x, y) = (mouse.cx, mouse.cy)
#    x += cam_x
#    y += cam_y
#    
#    names = [obj.name for obj in R.cities
#        if obj.x == x and obj.y == y] #and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]
#    if len(names) > 0:
#        names = ", ".join(names)
#        return names.capitalize() + str(x) + " " + str(y)
#    else:
#        return str(R.world.tiles[x][y].temperature)# 
#    
 
def handle_mouse():
    global selected, cam_x, cam_y
    mouse = libtcod.mouse_get_status()
    
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        if not local:
            if x > R.MAP_WIDTH - 1:
                x = R.MAP_WIDTH - 1
            if y > R.MAP_HEIGHT -  1:
                y = R.MAP_HEIGHT - 1
            if x < 0:
                x = 0
            if y < 0:
                y = 0
                
            selected = []
            print "boop"
            found = False
            for poi in R.pois:
                if poi.x == x +cam_x and poi.y == y + cam_y:
                    selected.append(poi)
                    update_info_bar()
                    found = True
    #                
    #        for city in R.cities:
    #            if city.x == x + cam_x and city.y == y + cam_y:
    #                selected = city
    #                update_info_bar()
    #                found = True
                    
            for obj in R.world_obj:
                if obj.x == x and obj.y == y:
                    selected.append(obj)
                    update_info_bar()
                    found = True
            if found == False and R.world.w >= (x + cam_x) and R.world.h >= (y + cam_y):
                print str(R.world.tiles[x + cam_x][y + cam_y].temperature) + "/" + str(R.world.tiles[x + cam_x][y + cam_y].elevation)
                
        else:
            if x > len(R.map_) - 1:
                x =len(R.map_)- 1
            if y > len(R.map_[0]) -  1:
                y = len(R.map_[0]) - 1
            if x < 0:
                x = 0
            if y < 0:
                y = 0
                
            print cam_x, cam_y, " player: ", you.x, you.y
                
    
              
def player_move_or_attack(dx, dy):
    global fov_recompute

    #the coordinates the player is moving to/attacking
    x = you.x + dx
    y = you.y + dy
    
    if not local:
        you.move_p(dx, dy)
        fov_recompute = True
        
        if you.x > R.MAP_WIDTH - 1:
            you.x = R.MAP_WIDTH - 1
        if you.y > R.MAP_HEIGHT -  1:
            you.y = R.MAP_HEIGHT - 1
            
        R.world.add_foot_traffic(you.x,you.y)
        #if R.world.tiles[x][y].blocked == False:
            #you.move(dx, dy)
            #fov_recompute = True 
        #if player:
        #    advance_time()
    else:
        if you.x + dx > 0 and you.y + dy > 0 and you.x + dx < len(R.map_) and you.y + dy < len(R.map_[0]):
            you.move_p(dx, dy)
            fov_recompute = True
            
            if you.x > len(R.map_) - 1:
                you.x = len(R.map_) - 1
            if you.y > len(R.map_[0]) -  1:
                you.y = len(R.map_[0]) - 1
        else:
            R.ui.message("oops hit the edge", libtcod.light_grey)
        


def handle_keys():
    global keys, player_turn, pause, game_speed, traffic, temperature, continent, local, fov_recompute
    global debug_mode

    #key = libtcod.console_check_for_keypress()  #real-time
    #key = libtcod.console_wait_for_keypress(True)  #turn-based
     
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return "exit"  #exit game
    
    elif key.vk == libtcod.KEY_SPACE:
        if pause:
            pause = False
        elif not pause:
            pause = True
        #return "pause"  #exit game
        
    elif key.vk == libtcod.KEY_0: #increase Speed.
        if game_speed == SLOW_SPEED:
            game_speed = NORM_SPEED
        elif game_speed == NORM_SPEED:
            game_speed = FAST_SPEED
        elif game_speed == FAST_SPEED:
            game_speed = FASTEST_SPEED
        elif game_speed == FASTEST_SPEED:
            R.ui.message("can't go no fasterer! :)", libtcod.light_grey)
            
    elif key.vk == libtcod.KEY_9: #decrease speed
        if game_speed == SLOW_SPEED:
            R.ui.message("can't go no slower-er! :)", libtcod.light_grey)
        elif game_speed == NORM_SPEED:
            game_speed = SLOW_SPEED
        elif game_speed == FAST_SPEED:
            game_speed = NORM_SPEED
        elif game_speed == FASTEST_SPEED:
            game_speed = FAST_SPEED
            
    if game_state == "playing":
        #movement keys
 
        if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            you.direction = "N"
            player_move_or_attack(0, -1)
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            you.direction = "S"
            player_move_or_attack(0, 1)
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            you.direction = "E"
            player_move_or_attack(-1, 0)
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            you.direction = "W"
            player_move_or_attack(1, 0)
        elif key.vk == libtcod.KEY_HOME or key.vk == libtcod.KEY_KP7:
            you.direction = "NW"
            player_move_or_attack(-1, -1)
        elif key.vk == libtcod.KEY_PAGEUP or key.vk == libtcod.KEY_KP9:
            you.direction = "NE"
            player_move_or_attack(1, -1)
        elif key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_KP1:
            you.direction = "SW"
            player_move_or_attack(-1, 1)
        elif key.vk == libtcod.KEY_PAGEDOWN or key.vk == libtcod.KEY_KP3:
            you.direction = "SE"
            player_move_or_attack(1, 1)
            
        elif key.vk == libtcod.KEY_KP5:
            player_move_or_attack(0, 0)
            pass  #do nothing ie wait for the monster to come to you
        else:
            #test for other keys
            key_char = chr(key.c)
            
            if key_char == "d":
                if debug_mode:
                    debug_mode = False
                else:
                    debug_mode = True
            
            elif key_char == "i":
                inventory_menu()
            
            elif key_char == "p":
                player_menu()
            
            elif key_char == "c":
                city_menu()
            
            elif key_char == "v":
                city_production_menu()
            
            elif key_char == "t":
                #debug mode to look at temperature
                if temperature is False:
                    temperature = True
                elif temperature is True:
                    temperature = False
                    
            elif key_char == "f":
                #debug key to look at traffic maps.
                if traffic is False:
                    traffic = True
                elif traffic is True:
                    traffic = False
                    
            elif key_char == "k":
                if continent is False:
                    continent = True
                elif continent is True:
                    continent = False
                    
            elif key_char == ",":
                pick_up()
                  
            elif key_char == "<":
                go_up()
            elif key_char == ">":
                """Go Down"""
                go_down()
                
            if debug_mode:
                if key_char == "#":
                    you.depth = 0
                    you.x = R.player_pos[0]
                    you.y = R.player_pos[1]
                    go_up()
                    clear_consoles()
                    local = False
                    R.ui.message("TESTING MODE: jumped to surface", colour = libtcod.light_flame)
                    render_all()

def go_up():
    """Go up"""
    global local, fov_recompute
    if local == True:
        if you.x == R.locale.floors[you.depth].up[0] and you.y == R.locale.floors[you.depth].up[1]:
            if you.depth == 0:
                you.x = R.player_pos[0]
                you.y = R.player_pos[1]
                clear_consoles()
                local = False
            else:
                you.depth -= 1
                you.x = R.locale.floors[you.depth].down[0]
                you.y = R.locale.floors[you.depth].down[1]
                
                R.map_= R.locale.floors[you.depth].map
                R.locale_obj = R.locale.floors[you.depth].objects
                fov_recompute = True
    else:
        R.ui.message("You jumped, That didn't really achieve much...", colour = libtcod.white)

def go_down():
    global local, you, fov_recompute
    if local == True:
        if you.x == R.locale.floors[you.depth].down[0] and you.y == R.locale.floors[you.depth].down[1]:
            if you.depth < len(R.locale.floors)-1:
                you.depth += 1
                you.x = R.locale.floors[you.depth].up[0]
                you.y = R.locale.floors[you.depth].up[1]
                
                R.map_= R.locale.floors[you.depth].map
                R.locale_obj = R.locale.floors[you.depth].objects
                fov_recompute = True
                
            else:
                R.ui.message("You can't go down anymore!", colour = libtcod.white)
            
    else:
        ## check to see if the player is stood on a visitable local POI. Atm, just dungeons.
        on_dun = False
        for dungeon in R.world.dungeons:
            if dungeon.x == you.x and dungeon.y == you.y:
                R.map_= dungeon.floors[0].map
                R.locale = dungeon
                R.locale_obj = dungeon.floors[0].objects
                R.player_pos = (you.x, you.y)
                you.x = dungeon.floors[0].up[0]
                you.y = dungeon.floors[0].up[1]
                you.depth = 0
                on_dun = True
                local = True
                
        if not on_dun or (R.map_== None or len(R.map_) <= 0):
            R.ui.message("There's nothing here!", colour = libtcod.white)

def pick_up():
    for item in R.locale_obj:
        if item.item != None:
            R.locale_obj.remove(item)
            R.you.inventory.store_item(item)
            R.ui.message("You just picked up " + item.name, libtcod.amber)

def inventory_menu():
    items = []
    for item in R.you.inventory.contents:
        items.append(item.name) 
    print R.inventory.contents[R.ui.menu("inventory contents:", items, 15)].name 
    #TODO: put in a quit clause.
    
def player_menu():
    options = []
    for key in you.skills.dict.keys():
        line = you.skills.dict[key].name + " - " + str(you.skills.dict[key].exp)
        options.append(line)
    
    R.ui.menu("Skills:", options, 15)
    
def city_production_menu():
    
    width,height = R.MAP_VIEW_WIDTH - 4, R.MAP_VIEW_HEIGHT - 4
    city_select_pop = libtcod.console_new(width,height)
    selected_city = None
    limit = len(cities) -1
    
    pos_x = R.MAP_VIEW_WIDTH/2 - width/2
    pos_y = R.MAP_VIEW_HEIGHT/2 - height/2
    for a in range(R.MAP_VIEW_WIDTH - 4): #clear screen, colour dark grey, every cycle
        for b in range(R.MAP_VIEW_HEIGHT - 4):
            #libtcod.console_print_rect(window, a, b, 
            libtcod.console_print_rect_ex(city_select_pop, a, b, R.MAP_VIEW_WIDTH-4,R.MAP_VIEW_HEIGHT-4,libtcod.BKGND_NONE,libtcod.LEFT, " ")
    
    libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
    libtcod.console_flush()     
    offset = 0      
    
    while True:
        libtcod.console_clear(city_select_pop)
        libtcod.console_set_default_foreground(city_select_pop, libtcod.yellow)    
        libtcod.console_set_default_foreground(city_select_pop, libtcod.light_yellow)
        #city_length = len(cities)
        for city in range(len(cities)): # picks the smaller of the two.
            location = cities[city]
            resources = "\n"
            for resource in location.producing:
                supply_demand = location.trade_house.supply_demand[resource]
                resources += resource + " " + str(location.producing[resource][1]) + "   \t   " + str(supply_demand[0])+ " " + str(supply_demand[1]) + ", " + str(supply_demand[2]) + "\n" 
            
            libtcod.console_print_ex(city_select_pop, 1, 1 + offset, libtcod.BKGND_NONE, libtcod.LEFT,location.name + "   " + resources)   
            offset += 6   
        libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
        libtcod.console_flush()
        
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_BACKSPACE or key.vk == libtcod.KEY_ESCAPE:
            break
        
def city_menu():
    
    width,height = R.MAP_VIEW_WIDTH - 4, R.MAP_VIEW_HEIGHT - 4
    city_select_pop = libtcod.console_new(width,height)
    selected_city = None
    limit = len(cities) -1
    
    pos_x = R.MAP_VIEW_WIDTH/2 - width/2
    pos_y = R.MAP_VIEW_HEIGHT/2 - height/2
    for a in range(R.MAP_VIEW_WIDTH - 4): #clear screen, colour dark grey, every cycle
        for b in range(R.MAP_VIEW_HEIGHT - 4):
            #libtcod.console_print_rect(window, a, b, 
            libtcod.console_print_rect_ex(city_select_pop, a, b, R.MAP_VIEW_WIDTH-4,R.MAP_VIEW_HEIGHT-4,libtcod.BKGND_NONE,libtcod.LEFT, " ")
    
    libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
    libtcod.console_flush()     
    offset = 0
    
    key = libtcod.console_check_for_keypress()
    while selected_city == None: #or key.vk != libtcod.KEY_ENTER:
        libtcod.console_clear(city_select_pop)
        libtcod.console_set_default_foreground(city_select_pop, libtcod.yellow)    
        libtcod.console_print_ex(city_select_pop, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, "Select the city")
        libtcod.console_set_default_foreground(city_select_pop, libtcod.light_yellow)
        #city_length = len(cities)
        for lines in range(min(len(cities),10)): # picks the smaller of the two.
            libtcod.console_print_ex(city_select_pop, 2, 3 + lines, libtcod.BKGND_NONE, libtcod.LEFT, chr(48 + lines) + ": " + cities[lines + offset].name)
        
        libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
        libtcod.console_flush()
        
        key = libtcod.console_wait_for_keypress(True)
        
        max_key = 48 + min(len(cities)-1,10) # and again, picks the smaller f the two values. 
                                                #to prevent it trying to be longer than amount of cities
        
        if key.c == 122: #z
            offset -= 1
            if offset < 0:
                offset = 0
        elif key.c == 120: #x
            offset += 1
            if 9 + offset > limit:
                offset = limit - 10
                
        elif key.c == 48: # 0
                selected_city = cities[0+offset]
        elif key.c == 49: # 1
            if max_key >= 49:
                selected_city = cities[1+offset]
            #I want to interact with the item in the '1' slot in the interface
        elif key.c == 50: # 2
            if max_key >=  50:
                selected_city = cities[2+offset]
        elif key.c == 51: #3
            if max_key >=  51:
                selected_city = cities[3+offset]
        elif key.c == 52: #4
            if max_key >=  52:
                selected_city = cities[4+offset]
        elif key.c == 53: #5
            if max_key >=  53:
                selected_city = cities[5+offset]
        elif key.c == 54: #6
            if max_key >=  54:
                selected_city = cities[6+offset]
        elif key.c == 55: #7
            if max_key >=  55:
                selected_city = cities[7+offset]
        elif key.c == 56: #8
            if max_key >=  56:
                selected_city = cities[8+offset]
        elif key.c == 57: #9
            if max_key >=  57:
                selected_city = cities[9+offset]
                
        elif key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_BACKSPACE or key.vk == libtcod.KEY_ESCAPE:
            break
        else:
            pass
        
        libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
        libtcod.console_flush()
        
    for a in range(R.MAP_WIDTH - 4): #clear screen, colour dark grey, every cycle
        for b in range(R.MAP_HEIGHT - 4):
            #libtcod.console_print_rect(window, a, b, 
            libtcod.console_print_rect_ex(city_select_pop, a, b, R.MAP_VIEW_WIDTH-4,R.MAP_VIEW_HEIGHT-4,libtcod.BKGND_NONE,libtcod.LEFT, " ")
    if selected_city != None:
        key = libtcod.console_check_for_keypress()
        while not key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_BACKSPACE:
            current_offset = offset
            
            for a in range(R.MAP_WIDTH - 4): #clear screen, colour dark grey, every cycle
                for b in range(R.MAP_HEIGHT - 4):
                    #libtcod.console_print_rect(window, a, b, 
                    libtcod.console_put_char(city_select_pop, a, b, ' ', libtcod.BKGND_NONE)
            #print the header with auto-wrap
            libtcod.console_set_default_foreground(city_select_pop, libtcod.white)
            libtcod.console_print_rect_ex(city_select_pop, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, selected_city.name + " stats!")
            
            libtcod.console_print_ex(city_select_pop, 2, 5, libtcod.BKGND_NONE, libtcod.LEFT, "-----------------")   
            libtcod.console_print_ex(city_select_pop, 3, 6, libtcod.BKGND_NONE, libtcod.LEFT, "produces:-") 
            y = 8              
            for resource in selected_city.producing: 
                if selected_city.producing[resource][1] > 0:
                    libtcod.console_print_ex(city_select_pop, 4, y, libtcod.BKGND_NONE, libtcod.LEFT, resource)
                    libtcod.console_print_ex(city_select_pop, 13, y, libtcod.BKGND_NONE, libtcod.LEFT, str(selected_city.producing[resource][1]))
                    y += 1
                    
            libtcod.console_print_ex(city_select_pop, 2, y, libtcod.BKGND_NONE, libtcod.LEFT, "\n")
            y += 1
            libtcod.console_print_ex(city_select_pop, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, "desires:-")
            y += 2
            for resource in selected_city.desired: 
                desire = selected_city.desired[resource]
                libtcod.console_print_ex(city_select_pop, 4, y, libtcod.BKGND_NONE, libtcod.LEFT, resource)
                libtcod.console_print_ex(city_select_pop, 13, y, libtcod.BKGND_NONE, libtcod.LEFT, str(desire))
                y += 1
            libtcod.console_print_ex(city_select_pop, 2, y, libtcod.BKGND_NONE, libtcod.LEFT, "-----------------")                  
            
            for resource in selected_city.trade_house.supply_demand: 
                supply_demand = selected_city.trade_house.supply_demand[resource]
                libtcod.console_print_ex(city_select_pop, 30, y, libtcod.BKGND_NONE, libtcod.LEFT, resource)
                libtcod.console_print_ex(city_select_pop, 40, y, libtcod.BKGND_NONE, libtcod.LEFT, str(supply_demand[0]))
                libtcod.console_print_ex(city_select_pop, 47, y, libtcod.BKGND_NONE, libtcod.LEFT, ", " + str(supply_demand[1]))
                libtcod.console_print_ex(city_select_pop, 54, y, libtcod.BKGND_NONE, libtcod.LEFT, ", " + str(supply_demand[2]))
                #libtcod.console_print_ex(window, 30, y, libtcod.BKGND_NONE, libtcod.LEFT, str(resource.quantity))
                #libtcod.console_print_ex(window, 30, y, libtcod.BKGND_NONE, libtcod.LEFT, str(resource.quantity))
                y += 1
            libtcod.console_print_ex(city_select_pop, 2, y, libtcod.BKGND_NONE, libtcod.LEFT, "-----------------")                  
            
            libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
            libtcod.console_flush()
            
            key = libtcod.console_wait_for_keypress(True)
        
    libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
    libtcod.console_flush()
        
def main_menu():
    
    main_init()
    
    while not libtcod.console_is_window_closed():    
        #now show the imageAt twice the size.

        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, R.SCREEN_WIDTH/2, R.SCREEN_HEIGHT/2-4, libtcod.BKGND_NONE, libtcod.CENTER,
            'Trader-RL')
        libtcod.console_print_ex(0, R.SCREEN_WIDTH/2, R.SCREEN_HEIGHT-2, libtcod.BKGND_NONE, libtcod.CENTER,
            'By Lemmily')

        choice = R.ui.menu("", ["Play a new game", "Continue last game", "Quit"], 24)

        if choice == 0: #new game
            #game_screen_init()
            new_game()
            play_game()
            #msgbox("Hey there")
        elif choice == 1:
            try: 
                load_game()
            except:
                R.ui.msgbox("\n No saved game to load. \n", 24)
                continue
            play_game()

        elif choice == 2:
            break
       
       
def main_init():
    global con, con_char, inf,minmap, message_bar, date, ui, game_msgs
    #libtcod.console_set_custom_font("dejavu16x16.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_set_custom_font("data/ont_big.png",libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(R.SCREEN_WIDTH, R.SCREEN_HEIGHT, "Trader-RL", False)
    libtcod.sys_set_fps(R.LIMIT_FPS)
    
    con = R.con = libtcod.console_new(R.MAP_WIDTH, R.MAP_HEIGHT)
    con_char = R.con_char = libtcod.console_new(R.MAP_WIDTH, R.MAP_HEIGHT)
    inf = R.inf = libtcod.console_new(R.INFO_BAR_WIDTH, R.SCREEN_HEIGHT - R.PANEL_HEIGHT)
    minmap = R.minmap = libtcod.console_new(R.INFO_BAR_WIDTH, R.PANEL_HEIGHT)
    message_bar = R.message_bar = libtcod.console_new(R.PANEL_WIDTH, R.PANEL_HEIGHT)
    
    game_msgs = R.game_msgs = []
    ui = R.ui = UI.UI(con,game_msgs)
    date = R.date = [0, [DAYS[0][0], 1, 1], [MONTHS[0][0], 1, 31], 1000];

#UNCOMMENT FOR PROFILING.
#profiler = cProfile.run("main_menu()","profile")

#PRINTS OUT PROFILE INFO
#p = pstats.Stats("profile")
#p.sort_stats("calls", "cumulative")
#p.print_stats()


main_menu()
