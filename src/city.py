"""
Created on 4 Mar 2013

@author: Emily
"""

import math
import random

import libtcodpy as libtcod
import entities
from economy import Resource, TradeHouse
import utils
import R



# master_commodity_list = [   "wool", "cloth", "clothes",
#                            "wood", "food", "ore", 
#                            "metal", "tools", "weapons"];

master_commodity_list = ["raw",
                         "produce",
                         "trade"]


class Settlement:
    def __init__(self, x, y, POI, name):
        self.POI = POI  # Contains the map object.
        self.name = name
        self.population = 0
        self.colour = libtcod.Color(20, 20, 20)
        self.char = "+"
        self.trader = None  # TODO: THIS probably needs it's own dedicated trader. not the same as just a "person" takes into account populations etc? Iuno.


class City:
    def __init__(self, x, y, POI, name="name", resource_list=[]):
        self.POI = POI
        self.x = x
        self.y = y
        self.char = "C"
        self.colour = libtcod.Color(100, 55, 55)
        self.population = libtcod.random_get_int(0, 10, 20)
        self.name = name
        if self.name == "name":
            try:
                self.name = libtcod.namegen_generate("city")
            except:
                self.name = "couldn't generate"
        self.trader = entities.Trader()
        if len(resource_list) == 0:
            self.resource_list = master_commodity_list

        self.treasury = 10000
        self.resources = self.trader.resources = {}  # these will be stroed as ["resource_name", quantity generated per hour.0]
        self.desired = {}
        # TODO: for now, void. there will be three type "raw"
        self.trader.believed_prices = {}
        for resource in R.resource_list:
            self.trader.believed_prices[resource] = [38.00, 10.00]  # name as key. then [believed price, deviance]
            self.trader.resources[resource] = [resource, 10.00]  # resource name as key, then the name and the quantity.
        self.trader.believed_prices["produce"] = [50.0, 30.0]

        self.producing = {}  # these will be stored as ["resource_name", quantity generated per hour.0]
        self.define_generation_goods()
        # self.pickGeneratedResources(resource_list) #TODO: re-initialise this.
        self.find_desired_resources()
        self.relationships = {}  # name of city, or city object.
        self.connections = {} #poi's connected by road
        self.in_city = []

        # self.productionRound()

        self.trade_house = TradeHouse(self)
        for resource in self.resource_list:
            self.trade_house.collect_info(resource)

        self.activity_log = {"produced": [], "traded": []}
        self.actions_queue = []

    def check_for_resources(self, key, needed, bonus=False):
        check = False
        if not bonus:
            for resource in needed[key][0]:
                if resource.type != "none":
                    if self.trader.resources[resource.type][1] >= resource.quantity:
                        check = True
                    else:
                        return False
                else:
                    return True
        else:
            for resource in needed[key][1]:
                if resource.type != "none" and self.trader.resources[resource.type][1] >= resource.quantity:
                    check = True
                else:
                    return False
        return check

    def produce(self, key, needed):
        #TODO: work out what this is doing properly.
        if self.check_for_resources(key, needed, True):  # check for the "bonus" item.
            for resource in needed[key][0]:
                if resource.type != "none":
                    self.trader.resources[resource.type][1] -= resource.quantity
            for resource in needed[key][1]:
                if chance_roll(20):
                    self.trader.resources[resource.type][1] -= 1

            # this is a bonus from having the "extra" item.
            self.trader.resources[key][1] += 1 * 1.25  # 1.25 is the modifier.... this could be reflected from quality?
            self.activity_log["produced"].append([self.name + " produced an excess of " + key, libtcod.gold])

        else:  # don't have or need any bonus items.
            for resource in needed[key][0]:
                if resource.type != "none":
                    self.resources[resource.type][1] -= resource.quantity
            self.trader.resources[key][1] += 1
            self.activity_log["produced"].append([self.name + " produced " + key, libtcod.amber])

    def consume(self):
        # consumption_rate = 0.0
        CR = float(self.population) / 10.0
        consumption_rate = (math.ceil(CR * 100.0) / 100.0) * 2
        for commodity in self.resources:
            if self.resources[commodity][1] > consumption_rate:
                self.resources[commodity][1] -= consumption_rate
            else:
                self.trade_house.trades["desires"][commodity].append([commodity, consumption_rate * 5])

    def sell_spare(self):
        CR = float(self.population) / 10.0
        consumption = math.ceil(CR * 100.0) / 100.0
        for commodity in R.resource_list:
            needed = 0.0
            needed += self.desired[commodity] * 3
            needed += consumption * 5
            if self.trader.resources[commodity][1] > needed:
                leftover = self.trader.resources[commodity][1] - needed
                price = self.trader.get_price(commodity, self.trade_house)
                self.trader.place_ask(self.trade_house, commodity, leftover, price)

    def production_round_temp(self):

        for key in self.producing:
            if self.producing[key][1] > 0:
                quantity = self.producing[key][1]
                for n in range(quantity):
                    if self.check_for_resources(key, master_raw_materials):
                        self.produce(key, master_raw_materials)
                if utils.roll_100() > 75:
                    self.produce("trade", master_raw_materials)
        self.consume()
        self.settle_desires()
        self.sell_spare()
        # self.trade_house.sell_spare("trade")

    def production_round(self):
        for key in self.producing:
            if self.producing[key][1] > 0:
                quantity = self.producing[key][1]
                for n in range(quantity):
                    if self.check_for_resources(key, master_raw_materials):
                        self.produce(key, master_raw_materials)

    def get_city_relationship(self, city):
        return self.relationships[city]

    def change_city_relationship(self, city, quantity):
        self.relationships[city] += quantity

    def create_base_relationships(self, city_list):
        """
        input a list of all the cities /the ones it should know.
        """
        for city in city_list:
            if city != self:
                self.relationships[city] = 0

    def define_generation_goods(self):
        self.producing["trade"] = ["trade", 0]
        self.producing["raw"] = ["raw", libtcod.random_get_int(0, 0, 16)]
        self.producing["produce"] = ["produce", libtcod.random_get_int(0, 0, 15)]

    def pick_generated_resources(self, resource_list):

        limit = len(resource_list) - 1
        # selections = {}

        print self.name
        quantity_resources = libtcod.random_get_int(0, 2, 6)
        temp = []
        for n in range(quantity_resources):
            resource = resource_list[libtcod.random_get_int(0, 0, limit)]

            temp.append(resource)

        # now consolidate so there is just one instance of a resource.
        for resource in resource_list:
            count = 0
            for test_for in temp:
                if test_for == resource:
                    count += 1

            self.producing[resource] = [resource, count]

        print "produces:-"
        for resource in self.producing:
            if self.producing[resource][1] > 0:
                print resource + str(self.producing[resource][1])
        print "\n"

        self.find_desired_resources()

    def find_desired_resources(self):
        for resource in R.resource_list:
            self.desired[resource] = 0
        temp = []
        resource = None
        for key in self.producing.keys():
            for n in range(len(master_raw_materials[key][0])):
                # resource = "what"
                resource = master_raw_materials[key][0][n]
                if resource.type != "none":
                    new_resource = Resource(type=resource.type, quantity=self.producing[key][1] * resource.quantity)
                    temp.append(new_resource)

        for name in self.resource_list:
            resource = Resource(name, 0)
            for test_for in temp:
                if test_for.type == name:
                    resource.quantity += test_for.quantity

            if resource.quantity > 0:
                self.desired[resource.type] = resource.quantity
                #        print "desires :-"
                #        for resource in self.desired:
                #            print resource.type + str(resource.quantity)
                #        print "-----------------"

    def settle_desires(self):
        trades = self.trade_house.trades
        for key in trades["desires"]:
            total_needed = 0
            for trade in trades["desires"][key]:
                total_needed += trade[1]
            actual = self.resources[key][1]
            if total_needed == 0:
                pass
            elif actual > total_needed + total_needed * 0.1:
                trades["desires"][key] = []
            else:
                quantity = self.trader.get_quantity(key, actual, total_needed, self.trade_house)
                price = self.trader.get_price(key, self.trade_house)

                if price < 0:
                    raise "error: price is a minus."
                trading = self.trader.check_for_offer(True, key, total_needed, actual, quantity, price)
                if trading < total_needed:
                    self.trader.place_bid(self.trade_house, key, quantity - trading + int(trading * 0.1), price)
                else:
                    pass


class Action:
    def __init__(self, turns):
        self.turns = turns
        # possible way of managing how the city does things.


class Component:
    def __init__(self, parent_settlement):
        self.parent = parent_settlement


class ProductionComponent(Component):
    """Component for each material produced there? they can be added and removed then."""

    def __init__(self, parent_settlement):
        Component.__init__(self, parent_settlement)


def chance_roll(chance=50):
    if chance <= 0:
        return False
    elif chance >= 100:
        return True
    else:
        if random.random() * 100 >= chance:
            return False
        else:
            return True


master_raw_materials = {"wool": [[Resource("none", 0)], [Resource("tools", 1)]],
                        "cloth": [[Resource("wool", 4)], [Resource("none", 0)]],
                        "clothes": [[Resource("cloth", 2), Resource("wool", 1)], [Resource("none", 0)]],
                        "wood": [[Resource("none", 0)], [Resource("tools", 1)]],
                        "food": [[Resource("wood", 1)], [Resource("tools", 1)]],
                        "ore": [[Resource("none", 0)], [Resource("tools", 2)]],
                        "metal": [[Resource("ore", 2), Resource("wood", 1)], [Resource("tools", 1)]],
                        "tools": [[Resource("metal", 2), Resource("wood", 1)], [Resource("none", 0)]],
                        "weapons": [[Resource("metal", 3), Resource("wood", 1)], [Resource("none", 0)]],
                        "raw": [[Resource("none", 0)], [Resource("none", 0)]],
                        "produce": [[Resource("raw", 2)], [Resource("none", 0)]],
                        "trade": [[Resource("produce", 1)], [Resource("none", 0)]]

                        }
