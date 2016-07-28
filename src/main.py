"""
Created on 4 Mar 2013

@author: Emily
"""
import threading

import src.libtcodpy as libtcod
# import math
import shelve
# import random
import src.R
import src.UI
import src.worldMap
import src.entities
# from R import con_char, inf#, #map_

import src.sentient

# import numpy as np
# import numpy

SLOW_SPEED = 8
NORM_SPEED = 12
FAST_SPEED = 20
FASTEST_SPEED = 30

game_speed = NORM_SPEED
turns = 0
pause = False

# #Render Modes##
traffic = False
temperature = False
continent = False
pathfinding = False

path_to_draw = 1

local = False

debug_mode = False

libtcod.namegen_parse('data/names.txt')

DAYS = [
    ['Monday', 1],
    ['Tuesday', 2],
    ['Wednesday', 3],
    ['Thursday', 4],
    ['Friday', 5],
    ['Saturday', 6],
    ['Sunday', 7]
]

MONTHS = [
    ['January', 1, 31],
    ['February', 2, 28],
    ['March', 3, 31],
    ['April', 4, 30],
    ['May', 5, 31],
    ['June', 6, 30],
    ['July', 7, 31],
    ['August', 8, 31],
    ['September', 9, 30],
    ['October', 10, 31],
    ['November', 11, 30],
    ['December', 12, 31],
]

master_resource_list = ["wool", "cloth", "clothes",
                        "wood", "food", "ore",
                        "metal", "tools", "weapons"]


def new_game():
    global game_msgs, test_msgs, ui, game_state
    global world, world_obj, cities, pois, you, selected, player_turn
    global tiles, cam_x, cam_y
    global key, mouse
    global map_, local, fov_recompute
    global debug_mode

    debug_mode = False
    mouse = libtcod.Mouse()
    key = libtcod.Key()

    cam_x, cam_y = 0, 0
    game_state = "playing"
    test_msgs = []
    world = src.R.world = src.worldMap.Map(src.R.MAP_WIDTH, src.R.MAP_HEIGHT)

    world_obj = src.R.world_obj = []
    tiles = src.R.tiles = world.tiles
    # make_map()
    pois = src.R.pois = world.pois
    cities = src.R.cities = world.cities
    src.R.ui.message(str(len(cities)) + " cities have been made!", libtcod.green)
    for city in cities:
        # print city.name + str(city.x) + "/" +  str(city.y)
        src.R.ui.message(city.name + str(city.x) + "/" + str(city.y), libtcod.light_grey)
        city.create_base_relationships(cities)

    # for n in range(5):
    #        city = City(name = libtcod.namegen_generate("city"), resource_list =master_resource_list)
    #        cities.append(city)
    #    city = None
    #    for city in cities:
    #        city.createBaseRelationships(cities)
    selected = []
    you = src.R.you = src.entities.Player()  # name = "player") #you = entities.Player())
    src.R.inventory = you.inventory
    world_obj.append(you)
    for a in range(5):
        x, y = src.worldMap.place_on_land()
        hero = src.R.hero = src.entities.Mover(x=x, y=y, name="hero " + str(a), pather=src.sentient.Pather(),
                                               ai=src.sentient.AI_Hero())
        world_obj.append(hero)

    # hero = entities.Mover(39,17, name="tester", ai=sentient.AI_Hero())
    # hero.ai.pather.new_find_path((hero.x,hero.y),(42,17), R.tiles)
    selected.append(hero)
    render_all()

    world.connect_cities()
    # world.connect_cities()
    # world.connect_cities()
    # world.connect_cities()
    # world.connect_cities()
    # world.connect_cities()
    #    point = (0,0)
    #    diction = dict()
    #    diction[(0,0)] = 10
    #    print str(diction[point])
    player_turn = True
    local = False
    fov_recompute = False
    # path = hero.pather.find_path((10,10),(0,0))
    src.R.ui.message("Finished init", libtcod.blue)


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
    global key, mouse, player_turn

    mouse = libtcod.Mouse()
    key = libtcod.Key()

    start_time = libtcod.sys_elapsed_seconds()
    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        delta_time = libtcod.sys_get_last_frame_length()
        # render the screen
        if not local:

            # #Clear the characters from screen.
            for object_ in src.R.world_obj:
                object_.clear(cam_x, cam_y)
            #
            # for city in cities:
            #     for merchant in city.trade_house.caravans_out:
            #         merchant.clear(cam_x, cam_y)

            # handles the keys and exit if needed.
            player_action = handle_keys()
            if player_action == "exit":
                save_game()
                break
            if not pause:  # and not player_turn:
                advance_time()
                # player_turn = True

            handle_mouse()
            render_all()

        else:

            #            for object_ in R.locale_obj:
            #                object_.clear(cam_x,cam_y)
            #
            #            you.clear(cam_x, cam_y)

            # handles the keys and exit if needed.
            player_action = handle_keys()
            if player_action == "exit":
                save_game()
                break

            handle_mouse()
            render_local()

        if src.R.msg_redraw is True:
            update_msg_bar()
            # update_info_bar()

            # erase all objectsat their old locations, before they move
            # for object in objects:
            #    object.clear(con)

            # handle_mouse()


def advance_time():
    global date, sub_turns, turns

    turns += game_speed

    if turns >= 60:  # // pass an hour.11
        turns = 0
        # whenever the date/time changes:-
        # render_all()
        for objects in src.R.world_obj:
            if objects.ai:
                objects.clear(cam_x, cam_y)
                objects.ai.take_turn()
                objects.draw(cam_x, cam_y)
        update_info_bar()

        ####
        ##### do any Hourly action here.
        ####

        date[0] += 1  # //increase hour
        # //passHour();
        # if  ( date[0] % 3 ) == 0:
        #            print "the time is ", str(date[0])
        #            for city in cities:
        #                for merchant in city.trade_house.caravans_out:
        #                    #merchant.clear(cam_x,cam_y)
        #                    merchant.ai.take_turn()
        #                    #merchant.draw(cam_x,cam_y)

        if (date[0] % 3) == 0:
            print "the time is ", str(date[0])
            city = cities[0]
            for merchant in city.trade_house.caravans_out:
                merchant.clear(cam_x, cam_y)
                merchant.ai.take_turn()

            for city in cities:
                city.production_round_temp()

        if date[0] is 24:  # // increase the day.

            for city in cities:
                city.production_round_temp()
                for resource in src.R.resource_list:
                    city.trade_house.collect_info(resource)
                    other_city = city
                    while other_city == city:
                        other_city = cities[libtcod.random_get_int(0, 0, len(cities) - 1)]
                    city.trade_house.resolve_offers_city(resource, other_city)
                    # for merchant in city.trade_house.caravans_in:
                    # merchant.take_turn()

            old_day = date[1][1]

            new_day = old_day + 1
            if new_day > 7:
                # does this work weekly?
                new_day = 1
            date[0] = 0  # //set hours back to 0;
            date[1][0] = DAYS[new_day - 1][0]  # increade day name
            date[1][1] = new_day  # //change day reference value
            date[1][2] += 1  # //increase the date by a day.

        if date[1][2] > date[2][2]:  # // if current day is more than the months max days, increase month.
            oldMonth = date[2][1]
            newMonth = oldMonth + 1

            if newMonth >= 12:
                newMonth = 1

            date[1][2] = 1
            date[2][0] = MONTHS[newMonth - 1][0]  # /change month name
            date[2][1] = MONTHS[newMonth - 1][1]  # //change month date value
            date[2][2] = MONTHS[newMonth - 1][2]  # //change max days in month.

        if date[2][1] > 12:  # //if the month is over 12, increase the year/

            date[2][0] = MONTHS[0][0]  # //change month name to first month
            date[2][1] = MONTHS[0][1]  # //change month date value to first month
            date[2][2] = MONTHS[0][2]  # //change max days in month to first month's
            date[3] += 1  # increase year

            ##
            ### Do anything that needs to be the start of the year here. AND use the new year
            ##
        update_msg_bar()  # update the date.


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


class RenderThread(threading.Thread):
    def __init__(self, thread_id, name, work_queue):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.q = work_queue

    def run(self):
        print "starting"
        render()
        print "exiting"


def render():
    if local:
        render_local()
    else:
        render_all()


def render_wilderness():
    global cam_x, cam_y
    # clear the city locations using OLD cam position.
    for city in src.R.cities:
        loc = src.R.tiles[city.x][city.y]
        colour = loc.bg
        libtcod.console_set_char_background(con, cam_x + city.x, cam_y + city.y, colour, libtcod.BKGND_SET)
        libtcod.console_set_char(con, cam_x + city.x, cam_y + city.y, ord(' '))

    cam_x = scrolling_map(you.x, src.R.MAP_VIEW_WIDTH / 2, src.R.MAP_VIEW_WIDTH, src.R.MAP_WIDTH)
    cam_y = scrolling_map(you.y, src.R.MAP_VIEW_HEIGHT / 2, src.R.MAP_VIEW_HEIGHT, src.R.MAP_HEIGHT)
    # now draw the map!
    for y in range(
            min(src.R.MAP_VIEW_HEIGHT, len(src.R.world.tiles[0]))):  # this refers to the SCREEN position. NOT map.
        for x in range(min(src.R.MAP_VIEW_WIDTH, len(src.R.world.tiles))):
            map_pos_x = x + cam_x
            map_pos_y = y + cam_y
            if map_pos_x >= src.R.MAP_WIDTH:
                continue
            if map_pos_y >= src.R.MAP_HEIGHT:
                continue

            tile = src.R.world.tiles[map_pos_x][map_pos_y]
            # visible = libtcod.map_is_in_fov(fov_map, tile.x, tile.y)
            visible = True
            if not visible:
                pass  # TODO: re-do the visible/ not visible code.
                # if it"s not visible right now, the player can only see it if it"s explored
                # if tile.explored:
                # if wall:
                #    libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET)
                #    libtcod.console_set_char(con, x, y, " ")
                # else:
                #    libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)
                #    libtcod.console_set_char(con, x, y, " ")
            else:
                colour = tile.bg
                libtcod.console_set_char(con, x, y, " ")
                libtcod.console_set_char_background(con, x, y, colour, libtcod.BKGND_SET)


def render_all():
    global cam_x, cam_y, selected

    # clear the city locations using OLD cam position.
    for city in src.R.cities:
        loc = src.R.tiles[city.x][city.y]
        colour = loc.bg
        libtcod.console_set_char_background(con, cam_x + city.x, cam_y + city.y, colour, libtcod.BKGND_SET)
        libtcod.console_set_char(con, cam_x + city.x, cam_y + city.y, ord(' '))

    # clear position of old object
    for objects in src.R.world_obj:
        objects.clear(cam_x, cam_y)

    # find the NEW camera position
    cam_x = scrolling_map(you.x, src.R.MAP_VIEW_WIDTH / 2, src.R.MAP_VIEW_WIDTH, src.R.MAP_WIDTH)
    cam_y = scrolling_map(you.y, src.R.MAP_VIEW_HEIGHT / 2, src.R.MAP_VIEW_HEIGHT, src.R.MAP_HEIGHT)

    # now draw the map!

    # this x and y refers to the SCREEN position. NOT map.
    for y in range(min(src.R.MAP_VIEW_HEIGHT, len(src.R.world.tiles[0]))):
        for x in range(min(src.R.MAP_VIEW_WIDTH, len(src.R.world.tiles))):

            # find out *actual" map-pos
            map_pos_x = x + cam_x
            map_pos_y = y + cam_y

            # skip if out of bounds
            if map_pos_x >= src.R.MAP_WIDTH:
                continue
            if map_pos_y >= src.R.MAP_HEIGHT:
                continue

            tile = src.R.world.tiles[map_pos_x][map_pos_y]

            # visible = libtcod.map_is_in_fov(fov_map, tile.x, tile.y)
            visible = True
            # wall = tile.block_sight

            if not visible:
                pass  # TODO: re-do the visible/ not visible code.
                # if it"s not visible right the player can only see it if it"s explored
                # if tile.explored:
                # if wall:
                #    libtcod.console_set_char_backgrnow, ound(con, x, y, color_dark_wall, libtcod.BKGND_SET)
                #    libtcod.console_set_char(con, x, y, " ")
                # else:
                #    libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)
                #    libtcod.console_set_char(con, x, y, " ")
            else:
                # it"s visible
                if tile.poi is None:
                    if traffic:  # for b&w image.
                        v = world.get_foot_traffic(map_pos_x, map_pos_y)
                        colour = libtcod.Color(v, v, v)
                        libtcod.console_set_char_background(con, x, y, colour, libtcod.BKGND_SET)
                        libtcod.console_set_char(con, x, y, " ")

                    elif temperature:  # for b&w image.
                        v = world.get_temperature(map_pos_x, map_pos_y)
                        v = int(v)
                        colour = libtcod.Color(v, v, v)
                        libtcod.console_set_char_background(con, x, y, colour, libtcod.BKGND_SET)
                        libtcod.console_set_char(con, x, y, " ")

                    elif continent:
                        m = 255 / len(src.R.world.continents)
                        if tile.type != "water":
                            v = tile.continent * m
                            colour = libtcod.Color(v, v, v)
                        else:
                            colour = tile.bg
                        libtcod.console_set_char_background(con, x, y, colour, libtcod.BKGND_SET)
                        libtcod.console_set_char(con, x, y, " ")

                    elif pathfinding:
                        char = " "
                        if len(selected) > 0 and hasattr(selected[0], "ai") and selected[0].ai is not None:
                            # and selected[0].ai.pather.end is not None:

                            # TODO: this is now only drawing one path.

                            draw_path = selected[0].ai.path
                            pather = selected[0].ai.pather2

                            # if path_to_draw == 3:
                            #     draw_path = selected[0].ai.path3
                            #     pather = selected[0].ai.pather3
                            # elif path_to_draw == 2:
                            #     draw_path = selected[0].ai.path2
                            #     pather = selected[0].ai.pather2
                            # else:
                            #     draw_path = selected[0].ai.path
                            #     pather = selected[0].ai.pather

                            loc = (map_pos_x, map_pos_y)
                            loc_str = str(loc)
                            if path_to_draw < 3 and pather.node_costs.has_key(loc_str):
                                v = float(pather.node_costs[loc_str])
                                v /= pather.largest_cost
                                v = int(v * 255)
                                colour = libtcod.Color(v, v, v)

                                if loc in draw_path:
                                    char = "."  # path tile

                            elif path_to_draw == 3 and pather.node_costs.has_key(
                                    loc):  # todo: hack for old pather, remove!!!
                                v = float(pather.node_costs[loc])
                                v /= pather.largest_cost
                                v = int(v * 255)
                                colour = libtcod.Color(v, v, v)

                                if loc in draw_path:
                                    char = "."  # path tile
                            else:
                                if tile.type == "water":
                                    colour = libtcod.Color(0, 10, 100)
                                elif tile.type == "grass":
                                    colour = libtcod.Color(0, 100, 10)
                                elif tile.type == "coast":
                                    colour = libtcod.Color(50, 10, 100)
                                elif tile.type == "path":
                                    colour = libtcod.Color(10, 60, 200)
                                else:
                                    colour = libtcod.Color(100, 10, 0)
                        else:
                            if tile.type == "water":
                                colour = libtcod.Color(0, 10, 100)
                            elif tile.type == "grass":
                                colour = libtcod.Color(0, 100, 10)
                            elif tile.type == "coast":
                                colour = libtcod.Color(50, 10, 100)
                            elif tile.type == "path":
                                colour = libtcod.Color(10, 60, 200)
                            else:
                                colour = libtcod.Color(100, 10, 0)
                        libtcod.console_set_char_background(con, x, y, colour, libtcod.BKGND_SET)
                        libtcod.console_set_char(con, x, y, char)

                    else:
                        libtcod.console_set_char(con, x, y, " ")
                        libtcod.console_set_char_background(con, x, y, tile.bg, libtcod.BKGND_SET)
                        # libtcod.console_set_char_foreground(con, x, y, libtcod.black)
                        # libtcod.console_set_char(con, x, y, libtcod.CHAR_BULLET)
                else:
                    libtcod.console_set_char_background(con, x, y, tile.poi.colour, libtcod.BKGND_SET)
                    libtcod.console_set_char_foreground(con, x, y, libtcod.white)
                    libtcod.console_set_char(con, x, y, tile.poi.char)
                # since it"s visible, explore it
                tile.explored = True

    # now draw all the merchants
    for city in cities:
        for merchant in city.trade_house.caravans_out:
            merchant.draw(cam_x, cam_y)
    for objects in src.R.world_obj:
        if objects.ai:
            # objects.clear(cam_x, cam_y)
            objects.draw(cam_x, cam_y)
    you.draw(cam_x, cam_y)

    # libtcod.console_print_ex(message_bar, R.SCREEN_WIDTH - R.INFO_BAR_WIDTH, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())
    # libtcod.console_set_default_background(con, libtcod.white)
    libtcod.console_blit(con, 0, 0, src.R.MAP_VIEW_WIDTH, src.R.MAP_VIEW_HEIGHT, 0, 0, 0)
    libtcod.console_blit(con_char, 0, 0, src.R.MAP_VIEW_WIDTH, src.R.MAP_VIEW_HEIGHT, 0, 0, 0, 1.0, 0.0)
    libtcod.console_blit(inf, 0, 0, src.R.INFO_BAR_WIDTH, src.R.SCREEN_HEIGHT, 0, src.R.MAP_VIEW_WIDTH, 0)
    libtcod.console_blit(minmap, 0, 0, src.R.INFO_BAR_WIDTH, src.R.PANEL_HEIGHT, 0, src.R.MAP_VIEW_WIDTH, src.R.PANEL_Y)
    libtcod.console_flush()


def render_minimap():
    # draw the mini map
    for cell_x in range(len(world.mini_map)):
        for cell_y in range(len(world.mini_map[cell_x])):
            colour = world.mini_map[cell_x][cell_y].bg
            libtcod.console_set_char_background(minmap, cell_x, cell_y, colour, libtcod.BKGND_SET)

            #    for char in R.world_obj:
            #        if char != you:
            #            char.draw(cam_x, cam_y)


def render_local():
    global map_, fov_recompute, cam_x, cam_y

    if len(src.R.active_map) > src.R.MAP_VIEW_WIDTH:
        cam_x = scrolling_map(you.x, src.R.MAP_VIEW_WIDTH_HALF + 1, src.R.MAP_VIEW_WIDTH, src.R.MAP_WIDTH)
    else:
        cam_x = 0
    if len(src.R.active_map[0]) > src.R.MAP_VIEW_HEIGHT:
        cam_y = scrolling_map(you.y, src.R.MAP_VIEW_HEIGHT_HALF, src.R.MAP_VIEW_HEIGHT, src.R.MAP_HEIGHT)
    else:
        cam_y = 0

    # cam_x = scrolling_map(you.x, R.MAP_VIEW_WIDTH / 2, R.MAP_VIEW_WIDTH, R.MAP_WIDTH)
    # cam_y = scrolling_map(you.y, R.MAP_VIEW_HEIGHT / 2, R.MAP_VIEW_HEIGHT, R.MAP_HEIGHT)

    if fov_recompute:
        fov_recompute = False
        libtcod.map_compute_fov(src.R.locale.floors[you.depth].fov_map, you.x, you.y, 10, True, 0)

        for sc_y in range(src.R.MAP_VIEW_HEIGHT):  # this refers to the SCREEN position. NOT map.
            for sc_x in range(src.R.MAP_VIEW_WIDTH):
                x = sc_x + cam_x
                y = sc_y + cam_y

                if sc_x < len(src.R.active_map) and sc_y < len(src.R.active_map[0]):
                    # and x < len(R.map_) and y < len(R.map_[0]):  #if it's within the bounds of the map.
                    tile = src.R.locale.floors[you.depth].tiles[x][y]
                    visible = libtcod.map_is_in_fov(src.R.locale.floors[you.depth].fov_map, x, y)
                    if not visible:
                        if tile.explored or debug_mode:
                            libtcod.console_put_char_ex(con, x, y, tile.char, libtcod.dark_green, libtcod.dark_gray)
                        else:
                            libtcod.console_put_char_ex(con, x, y, " ", libtcod.black, libtcod.black)
                        libtcod.console_set_char(con_char, x, y, " ")

                    else:
                        libtcod.console_put_char_ex(con, x, y, tile.char, libtcod.green, libtcod.light_grey)
                        libtcod.console_set_char(con_char, x, y, " ")
                        tile.explored = True
                else:
                    libtcod.console_put_char_ex(con, x, y, " ", libtcod.black, libtcod.black)

        for objects in src.R.locale_obj:
            # if the tile is explored, then draw the object.
            if libtcod.map_is_in_fov(src.R.locale.floors[you.depth].fov_map, objects.x, objects.y):
                objects.draw(cam_x, cam_y)
            # if it's explored but out of sight range - draw faded!
            elif src.R.locale.floors[you.depth].tiles[objects.x][objects.y].explored:
                objects.draw_faded(cam_x, cam_y)
        you.draw(cam_x, cam_y)

    libtcod.console_blit(con, 0, 0, src.R.MAP_VIEW_WIDTH, src.R.MAP_VIEW_HEIGHT, 0, 0, 0)
    libtcod.console_blit(con_char, 0, 0, src.R.MAP_VIEW_WIDTH, src.R.MAP_VIEW_HEIGHT, 0, 0, 0, 1.0, 0.0)
    libtcod.console_blit(inf, 0, 0, src.R.INFO_BAR_WIDTH, src.R.SCREEN_HEIGHT, 0, src.R.MAP_VIEW_WIDTH, 0)
    libtcod.console_flush()


def is_wall(x, y, active_map=None):
    if active_map is None:
        active_map = src.R.active_map

    if 0 <= x < len(active_map) and 0 <= y < len(active_map[x]):
        if active_map[x][y] != 0:
            return True
        else:
            return False
    else:
        return False


def is_blocked(x, y, active_map=None):
    if active_map is None:
        active_map = src.R.active_map

    if 0 <= x < len(active_map) and 0 <= y < len(active_map[x]):
        # Check the map first
        if active_map[x][y] != 0:
            return True
        else:
            # now check for objects that block.
            for item in src.R.locale_obj:
                if item.x == you.x and item.y == you.y and item.blocks == True:
                    return True
            return False
    else:
        return False


def clear_consoles():
    libtcod.console_clear(con)
    libtcod.console_clear(con_char)


def update_msg_bar():
    libtcod.console_clear(message_bar)
    libtcod.console_set_default_foreground(message_bar, libtcod.white)
    libtcod.console_print_ex(message_bar, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             str(date[0]) + " " + str(date[1][2]) + " " + str(date[1][0]) + " " + str(date[2][0]))
    # print the messages, one line at a time.
    y = 2
    for (line, colour) in src.R.game_msgs:
        libtcod.console_set_default_foreground(message_bar, colour)
        libtcod.console_print_ex(message_bar, src.R.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1
    libtcod.console_blit(message_bar, 0, 0, src.R.PANEL_WIDTH, src.R.PANEL_HEIGHT, 0, 0, src.R.PANEL_Y)
    libtcod.console_flush()
    src.R.msg_redraw = False


def update_info_bar():
    # TODO: seperate the UI updating into THIS function. the rest of the game updates in the render_all.
    # Fetch all the code into this function basically.
    # TODO: make a function for the ui to prin a message in this area.
    # Possibly with choices whether to wipe it first or add to it.

    libtcod.console_clear(inf)
    y = 2

    if len(selected) > 0:
        for sel in selected:
            libtcod.console_print_ex(inf, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, sel.name)
            libtcod.console_print_ex(inf, 0, y + 1, libtcod.BKGND_NONE, libtcod.LEFT, sel.type)
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
    # y = 1
    #    for (line, colour) in test_msgs:
    #        libtcod.console_set_default_foreground(inf, colour)
    #        libtcod.console_print_ex(inf, 2, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
    #        y += 1

    libtcod.console_blit(inf, 0, 0, src.R.INFO_BAR_WIDTH, src.R.SCREEN_HEIGHT, 0, src.R.MAP_VIEW_WIDTH, 0)
    libtcod.console_flush()


# def get_names_under_mouse():
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
    global selected, mouse
    mouse = libtcod.mouse_get_status()

    (x, y) = (mouse.cx, mouse.cy)

    # if x > R.MAP_WIDTH - 1:
    #     x = R.MAP_WIDTH - 1
    # if y > R.MAP_HEIGHT - 1:
    #     y = R.MAP_HEIGHT - 1
    # if x < 0:
    #     x = 0
    # if y < 0:
    #     y = 0

    if mouse.lbutton_pressed:
        selected = []
        print "mouse", x, y, "world", x + cam_x, y + cam_y
        found = False
        for poi in src.R.pois:
            if poi.x == x + cam_x and poi.y == y + cam_y:
                selected.append(poi)
                update_info_bar()
                found = True
                #
                #        for city in R.cities:
                #            if city.x == x + cam_x and city.y == y + cam_y:
                #                selected = city
                #                update_info_bar()
                #                found = True

        for obj in src.R.world_obj:
            if obj.x == cam_x + x and obj.y == cam_y + y:
                selected.append(obj)
                update_info_bar()
                found = True
                # if found == False and R.world.w >= (x + cam_x) and R.world.h >= (y + cam_y):
                #     print str(R.world.tiles[x + cam_x][y + cam_y].temperature) + "/" + str(
                #         R.world.tiles[x + cam_x][y + cam_y].elevation)


def handle_keys():
    global keys, player_turn, pause, game_speed, fov_recompute

    global debug_mode, traffic, temperature, continent, local, pathfinding, path_to_draw

    # key = libtcod.console_check_for_keypress()  #real-time
    # key = libtcod.console_wait_for_keypress(True)  #turn-based

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return "exit"  # exit game

    elif key.vk == libtcod.KEY_SPACE:
        if pause:
            pause = False
        elif not pause:
            pause = True
            # return "pause"  #exit game

    elif key.vk == libtcod.KEY_0:  # increase Speed.
        if game_speed == SLOW_SPEED:
            game_speed = NORM_SPEED
        elif game_speed == NORM_SPEED:
            game_speed = FAST_SPEED
        elif game_speed == FAST_SPEED:
            game_speed = FASTEST_SPEED
        elif game_speed == FASTEST_SPEED:
            src.R.ui.message("can't go no fasterer! :)", libtcod.light_grey)

    elif key.vk == libtcod.KEY_9:  # decrease speed
        if game_speed == SLOW_SPEED:
            src.R.ui.message("can't go no slower-er! :)", libtcod.light_grey)
        elif game_speed == NORM_SPEED:
            game_speed = SLOW_SPEED
        elif game_speed == FAST_SPEED:
            game_speed = NORM_SPEED
        elif game_speed == FASTEST_SPEED:
            game_speed = FAST_SPEED

    if game_state == "playing":
        # movement keys

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
            pass  # do nothing ie wait for the monster to come to you
        else:
            # test for other keys
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

            elif key_char == "q":
                pathfinding = not pathfinding

            elif key_char == "c":
                city_menu()

            elif key_char == "v":
                city_production_menu()

            elif key_char == "t":
                # debug mode to look at temperature
                if temperature is False:
                    temperature = True
                elif temperature is True:
                    temperature = False

            elif key_char == "f":
                # debug key to look at traffic maps.
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
                    you.x = src.R.player_pos[0]
                    you.y = src.R.player_pos[1]
                    clear_consoles()
                    local = False
                    src.R.ui.message("DEBUG: Jumped to surface", colour=libtcod.light_flame)

            if pathfinding:
                if key_char == "1":
                    path_to_draw = 1
                elif key_char == "2":
                    path_to_draw = 2
                elif key_char == "3":
                    path_to_draw = 3


def player_action():
    global player_turn

    player_turn = not player_turn


def player_move_or_attack(dx, dy):
    global fov_recompute

    # the coordinates the player is moving to/attacking
    x = you.x + dx
    y = you.y + dy

    if not local:
        you.move_p(dx, dy)
        fov_recompute = True

        if you.x > src.R.MAP_WIDTH - 1:
            you.x = src.R.MAP_WIDTH - 1
        if you.y > src.R.MAP_HEIGHT - 1:
            you.y = src.R.MAP_HEIGHT - 1

        src.R.world.add_foot_traffic(you.x, you.y)
        # if R.world.tiles[x][y].blocked == False:
        # you.move(dx, dy)
        # fov_recompute = True
        # if player:
        #    advance_time()
    else:
        you.move_p(dx, dy)
        fov_recompute = True

        if you.x > len(src.R.active_map) - 1:
            you.x = len(src.R.active_map) - 1
        if you.y > len(src.R.active_map[0]) - 1:
            you.y = len(src.R.active_map[0]) - 1

    clear_consoles()
    player_action()


def go_up():
    """Go up"""
    global local, fov_recompute
    if local is True:
        if you.x == src.R.locale.floors[you.depth].up[0] and you.y == src.R.locale.floors[you.depth].up[1]:
            if you.depth == 0:
                you.x = src.R.player_pos[0]
                you.y = src.R.player_pos[1]
                clear_consoles()
                local = False
            else:
                you.depth -= 1
                you.x = src.R.locale.floors[you.depth].down[0]
                you.y = src.R.locale.floors[you.depth].down[1]

                src.R.active_map = src.R.locale.floors[you.depth].map
                src.R.locale_obj = src.R.locale.floors[you.depth].objects
                fov_recompute = True
    else:
        src.R.ui.message("You jumped, That didn't really achieve much...", colour=libtcod.white)

    player_action()


def go_down():
    global local, you, fov_recompute
    if local is True:
        if you.x == src.R.locale.floors[you.depth].down[0] and you.y == src.R.locale.floors[you.depth].down[1]:
            if you.depth < len(src.R.locale.floors) - 1:
                you.depth += 1
                you.x = src.R.locale.floors[you.depth].up[0]
                you.y = src.R.locale.floors[you.depth].up[1]

                src.R.active_map = src.R.locale.floors[you.depth].map
                src.R.locale_obj = src.R.locale.floors[you.depth].objects
                fov_recompute = True

            else:
                src.R.ui.message("You can't go down anymore!", colour=libtcod.white)

    else:
        # check to see if the player is stood on a visitable local POI. Atm, just dungeons.
        on_dun = False
        for dungeon in src.R.world.dungeons:
            if dungeon.x == you.x and dungeon.y == you.y:
                src.R.active_map = dungeon.floors[0].map
                src.R.locale = dungeon
                src.R.locale_obj = dungeon.floors[0].objects
                src.R.player_pos = (you.x, you.y)
                you.x = dungeon.floors[0].up[0]
                you.y = dungeon.floors[0].up[1]
                you.depth = 0
                on_dun = True
                local = True

        if not on_dun or (src.R.active_map is None or len(src.R.active_map) <= 0):
            src.R.ui.message("There's nothing here!", colour=libtcod.white)
    player_action()


def pick_up():
    for item in src.R.locale_obj:
        if item.item is not None:
            src.R.locale_obj.remove(item)
            src.R.you.inventory.store_item(item)
            src.R.ui.message("You just picked up " + item.name, libtcod.amber)

    player_action()


def inventory_menu():
    items = []
    for item in src.R.you.inventory.contents:
        items.append(item.name)
    picked = src.R.ui.menu("inventory contents:", items, 15)
    try:
        print src.R.inventory.contents[picked].name
    except:
        print "no item exists!"


def player_menu():
    options = []
    for key in you.skills.dict.keys():
        line = you.skills.dict[key].name + " - " + str(you.skills.dict[key].exp)
        options.append(line)

    src.R.ui.menu("Skills:", options, 15)


def city_production_menu():
    width, height = src.R.MAP_VIEW_WIDTH - 4, src.R.MAP_VIEW_HEIGHT - 4
    city_select_pop = libtcod.console_new(width, height)
    selected_city = None
    limit = len(cities) - 1

    pos_x = src.R.MAP_VIEW_WIDTH / 2 - width / 2
    pos_y = src.R.MAP_VIEW_HEIGHT / 2 - height / 2
    for a in range(src.R.MAP_VIEW_WIDTH - 4):  # clear screen, colour dark grey, every cycle
        for b in range(src.R.MAP_VIEW_HEIGHT - 4):
            # libtcod.console_print_rect(window, a, b,
            libtcod.console_print_rect_ex(city_select_pop, a, b, src.R.MAP_VIEW_WIDTH - 4, src.R.MAP_VIEW_HEIGHT - 4,
                                          libtcod.BKGND_NONE, libtcod.LEFT, " ")

    libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
    libtcod.console_flush()
    offset = 0

    while True:
        libtcod.console_clear(city_select_pop)
        libtcod.console_set_default_foreground(city_select_pop, libtcod.yellow)
        libtcod.console_set_default_foreground(city_select_pop, libtcod.light_yellow)
        # city_length = len(cities)
        for city in range(len(cities)):  # picks the smaller of the two.
            location = cities[city]
            resources = "\n"
            for resource in location.producing:
                supply_demand = location.trade_house.supply_demand[resource]
                resources += resource + " " + str(location.producing[resource][1]) + "   \t   " + str(
                    supply_demand[0]) + " " + str(supply_demand[1]) + ", " + str(supply_demand[2]) + "\n"

            libtcod.console_print_ex(city_select_pop, 1, 1 + offset, libtcod.BKGND_NONE, libtcod.LEFT,
                                     location.name + "   " + resources)
            offset += 6
        libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
        libtcod.console_flush()

        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_BACKSPACE or key.vk == libtcod.KEY_ESCAPE:
            break


def city_menu():
    width, height = src.R.MAP_VIEW_WIDTH - 4, src.R.MAP_VIEW_HEIGHT - 4
    city_select_pop = libtcod.console_new(width, height)
    selected_city = None
    limit = len(cities) - 1

    pos_x = src.R.MAP_VIEW_WIDTH / 2 - width / 2
    pos_y = src.R.MAP_VIEW_HEIGHT / 2 - height / 2
    for a in range(src.R.MAP_VIEW_WIDTH - 4):  # clear screen, colour dark grey, every cycle
        for b in range(src.R.MAP_VIEW_HEIGHT - 4):
            # libtcod.console_print_rect(window, a, b,
            libtcod.console_print_rect_ex(city_select_pop, a, b, src.R.MAP_VIEW_WIDTH - 4, src.R.MAP_VIEW_HEIGHT - 4,
                                          libtcod.BKGND_NONE, libtcod.LEFT, " ")

    libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
    libtcod.console_flush()
    offset = 0

    key = libtcod.console_check_for_keypress()
    while selected_city is None:  # or key.vk != libtcod.KEY_ENTER:
        libtcod.console_clear(city_select_pop)
        libtcod.console_set_default_foreground(city_select_pop, libtcod.yellow)
        libtcod.console_print_ex(city_select_pop, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, "Select the city")
        libtcod.console_set_default_foreground(city_select_pop, libtcod.light_yellow)
        # city_length = len(cities)
        for lines in range(min(len(cities), 10)):  # picks the smaller of the two.
            libtcod.console_print_ex(city_select_pop, 2, 3 + lines, libtcod.BKGND_NONE, libtcod.LEFT,
                                     chr(48 + lines) + ": " + cities[lines + offset].name)

        libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
        libtcod.console_flush()

        key = libtcod.console_wait_for_keypress(True)

        max_key = 48 + min(len(cities) - 1, 10)  # and again, picks the smaller f the two values.
        # to prevent it trying to be longer than amount of cities

        if key.c == 122:  # z
            offset -= 1
            if offset < 0:
                offset = 0
        elif key.c == 120:  # x
            offset += 1
            if 9 + offset > limit:
                offset = limit - 10

        elif key.c == 48:  # 0
            selected_city = cities[0 + offset]
        elif key.c == 49:  # 1
            if max_key >= 49:
                selected_city = cities[1 + offset]
                # I want to interact with the item in the '1' slot in the interface
        elif key.c == 50:  # 2
            if max_key >= 50:
                selected_city = cities[2 + offset]
        elif key.c == 51:  # 3
            if max_key >= 51:
                selected_city = cities[3 + offset]
        elif key.c == 52:  # 4
            if max_key >= 52:
                selected_city = cities[4 + offset]
        elif key.c == 53:  # 5
            if max_key >= 53:
                selected_city = cities[5 + offset]
        elif key.c == 54:  # 6
            if max_key >= 54:
                selected_city = cities[6 + offset]
        elif key.c == 55:  # 7
            if max_key >= 55:
                selected_city = cities[7 + offset]
        elif key.c == 56:  # 8
            if max_key >= 56:
                selected_city = cities[8 + offset]
        elif key.c == 57:  # 9
            if max_key >= 57:
                selected_city = cities[9 + offset]

        elif key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_BACKSPACE or key.vk == libtcod.KEY_ESCAPE:
            break
        else:
            pass

        libtcod.console_blit(city_select_pop, 0, 0, width, height, 0, pos_x, pos_y, 1.0, 0.9)
        libtcod.console_flush()

    for a in range(src.R.MAP_WIDTH - 4):  # clear screen, colour dark grey, every cycle
        for b in range(src.R.MAP_HEIGHT - 4):
            # libtcod.console_print_rect(window, a, b,
            libtcod.console_print_rect_ex(city_select_pop, a, b, src.R.MAP_VIEW_WIDTH - 4, src.R.MAP_VIEW_HEIGHT - 4,
                                          libtcod.BKGND_NONE, libtcod.LEFT, " ")
    if selected_city is not None:
        key = libtcod.console_check_for_keypress()
        while not key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_BACKSPACE:
            current_offset = offset
            # clear screen, colour dark grey, every cycle
            for a in range(src.R.MAP_WIDTH - 4):
                for b in range(src.R.MAP_HEIGHT - 4):
                    # libtcod.console_print_rect(window, a, b,
                    libtcod.console_put_char(city_select_pop, a, b, ' ', libtcod.BKGND_NONE)
            # print the header with auto-wrap
            libtcod.console_set_default_foreground(city_select_pop, libtcod.white)
            libtcod.console_print_rect_ex(city_select_pop, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT,
                                          selected_city.name + " stats!")

            libtcod.console_print_ex(city_select_pop, 2, 5, libtcod.BKGND_NONE, libtcod.LEFT, "-----------------")
            libtcod.console_print_ex(city_select_pop, 3, 6, libtcod.BKGND_NONE, libtcod.LEFT, "produces:-")
            y = 8
            for resource in selected_city.producing:
                if selected_city.producing[resource][1] > 0:
                    libtcod.console_print_ex(city_select_pop, 4, y, libtcod.BKGND_NONE, libtcod.LEFT, resource)
                    libtcod.console_print_ex(city_select_pop, 13, y, libtcod.BKGND_NONE, libtcod.LEFT,
                                             str(selected_city.producing[resource][1]))
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
                libtcod.console_print_ex(city_select_pop, 20, y, libtcod.BKGND_NONE, libtcod.LEFT, resource)
                libtcod.console_print_ex(city_select_pop, 30, y, libtcod.BKGND_NONE, libtcod.LEFT,
                                         str(supply_demand[0]))
                libtcod.console_print_ex(city_select_pop, 37, y, libtcod.BKGND_NONE, libtcod.LEFT,
                                         ", " + str(supply_demand[1]))
                libtcod.console_print_ex(city_select_pop, 44, y, libtcod.BKGND_NONE, libtcod.LEFT,
                                         ", " + str(supply_demand[2]))
                # libtcod.console_print_ex(window, 30, y, libtcod.BKGND_NONE, libtcod.LEFT, str(resource.quantity))
                # libtcod.console_print_ex(window, 30, y, libtcod.BKGND_NONE, libtcod.LEFT, str(resource.quantity))
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
        # now show the imageAt twice the size.

        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, src.R.SCREEN_WIDTH / 2, src.R.SCREEN_HEIGHT / 2 - 4, libtcod.BKGND_NONE,
                                 libtcod.CENTER,
                                 'Trader-RL')
        libtcod.console_print_ex(0, src.R.SCREEN_WIDTH / 2, src.R.SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.CENTER,
                                 'By Lemmily')

        choice = src.R.ui.menu("", ["Play a new game", "Continue last game", "Quit"], 24)

        if choice == 0:  # new game
            # game_screen_init()
            new_game()
            play_game()
            # msgbox("Hey there")
        elif choice == 1:
            try:
                load_game()
            except:
                src.R.ui.msgbox("\n No saved game to load. \n", 24)
                continue
            play_game()

        elif choice == 2:
            break


def main_init():
    global con, con_char, inf, minmap, message_bar, date, ui, game_msgs
    # libtcod.console_set_custom_font("dejavu16x16.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_set_custom_font("data/ont_big.png", libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(src.R.SCREEN_WIDTH, src.R.SCREEN_HEIGHT, "Trader-RL", False)
    libtcod.sys_set_fps(src.R.LIMIT_FPS)

    con = src.R.con = libtcod.console_new(src.R.MAP_WIDTH, src.R.MAP_HEIGHT)
    con_char = src.R.con_char = libtcod.console_new(src.R.MAP_WIDTH, src.R.MAP_HEIGHT)
    inf = src.R.inf = libtcod.console_new(src.R.INFO_BAR_WIDTH, src.R.SCREEN_HEIGHT - src.R.PANEL_HEIGHT)
    minmap = src.R.min_map = libtcod.console_new(src.R.INFO_BAR_WIDTH, src.R.PANEL_HEIGHT)
    message_bar = src.R.message_bar = libtcod.console_new(src.R.PANEL_WIDTH, src.R.PANEL_HEIGHT)

    game_msgs = src.R.game_msgs = []
    ui = src.R.ui = src.UI.UI(con, game_msgs)
    # initialising to January
    date = src.R.date = [0, [DAYS[0][0], 1, 1], [MONTHS[0][0], 1, 31], 1000]


# UNCOMMENT FOR PROFILING.
# profiler = cProfile.run("main_menu()","profile")

# PRINTS OUT PROFILE INFO
# p = pstats.Stats("profile")
# p.sort_stats("calls", "cumulative")
# p.print_stats()


main_menu()
