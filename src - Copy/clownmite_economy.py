

from __future__ import division
import xml.etree.ElementTree as etree
import random
import cProfile
import pstats
import os

try:
    import numpy as np
except:
    print 'Can\'t load numpy - no access to graphs'
    
try:
    from matplotlib.pyplot import plot, title, legend, show, grid, figure
except:
    print 'Can\'t load matplotlib - no access to graphs'

XML_DIRECTORY = os.getcwd() + '\\XML\\'

HIST_WINDOW_SIZE = 5 # Amount of trades auctions keep in memory to determine avg price (used by agents)
MAX_INVENTORY_SIZE = 15 # A not-really-enforced max inventory limit

PROFIT_MARGIN = 1.1 # Won't sell an item for lower than this * normalized production cost
STARTING_GOLD = 1000 # How much gold each agent starts with

MIN_CERTAINTY_VALUE = 8 ## Within what range traders are limited to estimating the market price
BID_REJECTED_ADJUSTMENT = 5 # Adjust prices by this much when our bid is rejected
ASK_REJECTED_ADJUSTMENT = 5 # Adjust prices by this much when nobody buys our stuff
REJECTED_UNCERTAINTY_AMOUNT = 2 # We get this much more uncertain about a price when an offer is rejected
ACCEPTED_CERTAINTY_AMOUNT = 1  # Out uncertainty about a price decreases by this amount when an offer is accepted

P_DIF_ADJ = 3  # When offer is accepted and exceeds what we thought the price value was, adjust it upward by this amount
N_DIF_ADJ = 3  # When offer is accepted and is lower than what we thought the price value was, adjust it downward by this amount
P_DIF_THRESH = 2.5  #Threshhold at which adjustment of P_DIF_ADJ is added to the perceived value of a commodity
N_DIF_THRESH = 2.5 #Threshhold at which adjustment of P_DIF_ADJ is subtracted from the perceived value of a commodity

START_VAL = 40 # Arbitrary value that sets the starting price of good (in gold) 
START_UNCERT = 10 # Arbitrary uncertainty value (agent believes price is somewhere between (mean-this, mean+this)

FOOD_BID_THRESHHOLD = 4 # Will bid on food when lower than this amount
GRANARY_THRESH = 5 # # of turns before we can get free food from the granary
STARVATION_THRESH = 10 # # of turns before we starve
########################### New stuff ###########################


def setup_resources():
    global RESOURCES, RESOURCE_TYPES, GOODS, GOOD_TYPES, COMMODITY_TYPES, COMMODITY_TOKENS
    global gatherers_by_token, producers_by_token, merchants_by_token, STRATEGIC_TYPES, CITY_RESOURCE_SLOTS, CITY_INDUSTRY_SLOTS, GOODS_BY_RESOURCE_TOKEN
    amt = 2000
    
    ### Chances of resources appearing in each biome.
    ore_app = {'mountain':0, 'tundra':5, 'taiga':8, 'temperate forest':10, 'temperate steppe':10, 'rain forest':5, 'tree savanna':12, 'grass savanna':15, 'dry steppe':20, 
                        'semi-arid desert':20, 'arid desert':20, 'river':0}
    food_app = {'mountain':0, 'tundra':0, 'taiga':0, 'temperate forest':1, 'temperate steppe':5, 'rain forest':0, 'tree savanna':12, 'grass savanna':20, 'dry steppe':20, 
                        'semi-arid desert':0, 'arid desert':0, 'river':5}
    clay_app = {'mountain':0, 'tundra':0, 'taiga':0, 'temperate forest':0, 'temperate steppe':0, 'rain forest':10, 'tree savanna':0, 'grass savanna':10, 'dry steppe':20, 
                        'semi-arid desert':20, 'arid desert':20, 'river':5}        
    silt_app = {'mountain':0, 'tundra':0, 'taiga':0, 'temperate forest':0, 'temperate steppe':0, 'rain forest':0, 'tree savanna':0, 'grass savanna':0, 'dry steppe':0, 
                        'semi-arid desert':0, 'arid desert':0, 'river':500}    
    wood_app = {'mountain':0, 'tundra':0, 'taiga':1000, 'temperate forest':1000, 'temperate steppe':0, 'rain forest':1000, 'tree savanna':1000, 'grass savanna':0, 'dry steppe':0, 
                        'semi-arid desert':0, 'arid desert':0, 'river':0}                
    flax_app = {'mountain':0, 'tundra':0, 'taiga':0, 'temperate forest':0, 'temperate steppe':10, 'rain forest':0, 'tree savanna':0, 'grass savanna':20, 'dry steppe':20, 
                        'semi-arid desert':5, 'arid desert':0, 'river':0}        
    
    ### define the actual resources. gather_amount is how many resources are gathered per round - 
    ### half go to the government and aren't used in the other. Each round, if a random number
    ### between 1 and 1000 is less than break_chance, a good made out of the resouce will be destroyed
    copper = Resource(name='copper', category='ores', resource_class='strategic', gather_amount=4, break_chance=200, app_chances=ore_app, app_amt=amt)
    bronze = Resource(name='bronze', category='ores', resource_class='strategic', gather_amount=4, break_chance=100, app_chances=ore_app, app_amt=amt)
    iron = Resource(name='iron', category='ores', resource_class='strategic', gather_amount=4,  break_chance=60, app_chances=ore_app, app_amt=amt)
    food = Resource(name='food', category='foods', resource_class='strategic', gather_amount=8, break_chance=1, app_chances=food_app, app_amt=amt)
    clay = Resource(name='clay', category='clays', resource_class='strategic', gather_amount=4, break_chance=200, app_chances=clay_app, app_amt=amt)
    silt = Resource(name='silt', category='clays', resource_class='strategic', gather_amount=4, break_chance=200, app_chances=silt_app, app_amt=amt)
    wood = Resource(name='wood', category='woods', resource_class='strategic', gather_amount=4, break_chance=200, app_chances=wood_app, app_amt=amt)
    #oak = Resource(name='oak', category='woods', resource_class='strategic', gather_amount=3, break_chance=200, app_chances=wood_app, app_amt=amt)
    flax = Resource(name='flax', category='cloths', resource_class='strategic', gather_amount=4, break_chance=200, app_chances=flax_app, app_amt=amt)
            
    RESOURCES = [copper, bronze, iron, clay, silt, wood, flax, food]        
    RESOURCE_TYPES = {}
    STRATEGIC_TYPES = {}
    ##
    COMMODITY_TYPES = {}
    COMMODITY_TOKENS = {}
    ## Key = category, value = list of resources
    for resource in RESOURCES:
        COMMODITY_TOKENS[resource.name] = resource
        
        if not resource.category in RESOURCE_TYPES: RESOURCE_TYPES[resource.category] = [resource]
        else:                                          RESOURCE_TYPES[resource.category].append(resource)
        
        if not resource.category in COMMODITY_TYPES.keys(): COMMODITY_TYPES[resource.category] = [resource]
        else:                                                            COMMODITY_TYPES[resource.category].append(resource)

        if resource.resource_class == 'strategic':
            if not resource.resource_class in STRATEGIC_TYPES.keys(): STRATEGIC_TYPES[resource.category] = [resource]
            else:                                                      STRATEGIC_TYPES[resource.category].append(resource)
        
    #### Goods made from resources. in_amt is how many resources it consumers to create the # of items specified by out_amt
    copper_tools = FinishedGood(category='tools', material=copper, in_amt=2, out_amt=1)
    bronze_tools = FinishedGood(category='tools', material=bronze, in_amt=2, out_amt=1)
    iron_tools   = FinishedGood(category='tools', material=iron,   in_amt=2, out_amt=1)
    silt_pottery = FinishedGood(category='pottery', material=silt, in_amt=1, out_amt=1)
    clay_pottery = FinishedGood(category='pottery', material=clay, in_amt=1, out_amt=1)
    wood_furniture = FinishedGood(category='furniture', material=wood, in_amt=1, out_amt=1)
    #oak_furniture = FinishedGood(category='furniture', material=oak, in_amt=1, out_amt=1)
    flax_clothing = FinishedGood(category='clothing', material=flax, in_amt=1, out_amt=1)
            
    GOODS = [copper_tools, bronze_tools, iron_tools, silt_pottery, clay_pottery, wood_furniture, flax_clothing]
    GOOD_TYPES = {}
    GOODS_BY_RESOURCE_TOKEN = {}
    ## Key = category, calue = list of resources
    for good in GOODS:
        COMMODITY_TOKENS[good.name] = good
        
        if not good.category in GOOD_TYPES: GOOD_TYPES[good.category] = [good]
        else:                                  GOOD_TYPES[good.category].append(good)
            
        if not good.category in COMMODITY_TYPES.keys(): COMMODITY_TYPES[good.category] = [good]
        else:                                            COMMODITY_TYPES[good.category].append(good)    
        
        if not good.category in GOODS_BY_RESOURCE_TOKEN.keys(): GOODS_BY_RESOURCE_TOKEN[good.material.name] = [good]
        else:                                                    GOODS_BY_RESOURCE_TOKEN[good.material.name].append(good)
    
    ################### AGENT TYPES ####################
    # These dicts look up agent info based on the resource or good that the agent produces
    #
    # Consumed items are consumed each turn, regardless of whether they produce anything..
    # Essential items are required in order to do their jobs, but are not consumed (but have a chance of breaking each turn)
    # Preferred items are not required to do their jobs, but an agent will still try to purchase them if there are none in inventory
    #
    # Raw resource gatherers
    gatherers_by_token = {
                         'food':{'name':'Food Farmer', 'consumed':[], 'essential':['tools'], 'preferred':['clothing', 'furniture', 'pottery'] },
                         'flax':{'name':'Flax Farmer', 'consumed':[], 'essential':['tools'], 'preferred':['furniture', 'pottery'] },
                         'copper':{'name':'Copper Miner', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] },
                         'bronze':{'name':'Bronze Miner', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] },
                         'iron':{'name':'Iron Miner', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] },
                         'clay':{'name':'Clay Gatherer', 'consumed':[], 'essential':[], 'preferred':['clothing'] },
                         'silt':{'name':'Silt Gatherer', 'consumed':[], 'essential':[], 'preferred':['clothing'] },
                         'wood':{'name':'Woodcutter', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] },
                         #'oak':{'name':'Oak Woodcutter', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] }
                         }
    # Good producers
    producers_by_token = {                     
                         'copper tools':{'name':'Copper Blacksmith', 'finished_goods':'copper tools', 'consumed':['woods'], 'essential':[], 'preferred':['clothing'] },
                         'bronze tools':{'name':'Bronze Blacksmith', 'finished_goods':'bronze tools', 'consumed':['woods'], 'essential':[], 'preferred':['clothing'] },
                         'iron tools':{'name':'Iron Blacksmith', 'finished_goods':'iron tools', 'consumed':['woods'], 'essential':[], 'preferred':['clothing'] },
                         'silt pottery':{'name':'Silt Potter', 'finished_goods':'silt pottery', 'consumed':[], 'essential':[], 'preferred':['clothing'] },
                         'clay pottery':{'name':'Clay Potter', 'finished_goods':'clay pottery', 'consumed':[], 'essential':[], 'preferred':['clothing'] },
                         'wood furniture':{'name':'Wood Carptenter', 'finished_goods':'wood furniture', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] },
                         #'oak furniture':{'name':'Wood Carptenter', 'finished_goods':'wood furniture', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] },
                         'flax clothing':{'name':'Flax Clothier', 'finished_goods':'flax clothing', 'consumed':[], 'essential':['tools'], 'preferred':[] }
                         }
                         
    merchants_by_token = {'merchant':{'consumed':[], 'essential':[], 'preferred':[]}  }
                         
    CITY_RESOURCE_SLOTS = {'foods':6, 'cloths':6, 'clays':6, 'ores':4, 'woods':4}                     
    CITY_INDUSTRY_SLOTS = {'tools':3, 'clothing':5, 'pottery':5, 'furniture':3}
                         
                         
def economy_test_run():                         
    native_resources = [resource.name for resource in RESOURCES]
    print native_resources
    economy = Economy(native_resources=native_resources, local_taxes=5, owner=None)        
    
    for i in xrange(6):
        for resource in RESOURCES:
            if resource.name != 'food' and resource.name != 'flax':
                economy.add_resource_gatherer(resource.name)
                economy.add_resource_gatherer(resource.name)
            elif resource.name == 'flax':
                economy.add_resource_gatherer(resource.name)
                economy.add_resource_gatherer(resource.name)
                economy.add_resource_gatherer(resource.name)
            else:
                economy.add_resource_gatherer(resource.name)
                economy.add_resource_gatherer(resource.name)
                economy.add_resource_gatherer(resource.name)
                economy.add_resource_gatherer(resource.name)
                economy.add_resource_gatherer(resource.name)
                economy.add_resource_gatherer(resource.name)
                
    for i in xrange(4):            
        for good in GOODS:
            if good.name == 'flax clothing':
                economy.add_goods_producer(good.name)
                economy.add_goods_producer(good.name)
                economy.add_goods_producer(good.name)
            else:
                economy.add_goods_producer(good.name)
                economy.add_goods_producer(good.name)
        
    for i in xrange(20):
        print '------------', i, '--------------'
        economy.run_simulation()
        
    for token, auction in economy.auctions.iteritems():
        print token, auction.price_history
        
def check_strategic_resources(nearby_resources):
    # Checks a set of resources to see if there's enough types of strategic resources
    unavailable_types = []
    for resource_type, resource_token_list in STRATEGIC_TYPES.iteritems():
        has_token = False
        for resource_token in resource_token_list:
            if resource_token.name in nearby_resources:
                has_token = True
                break            
        if not has_token:
            unavailable_types.append(resource_type)
    return unavailable_types
    
def list_goods_from_strategic(strategic_resources):
    goods_we_can_make = []
    for resource in strategic_resources:
        if resource in GOODS_BY_RESOURCE_TOKEN.keys():
            for good_class in GOODS_BY_RESOURCE_TOKEN[resource]:
                goods_we_can_make.append(good_class.name)
    return goods_we_can_make
    
        
class Resource(object):
    def __init__(self, name, category, resource_class, gather_amount, break_chance, app_chances, app_amt):
        self.name = name
        self.category = category
        self.resource_class = resource_class
        self.gather_amount = gather_amount
        self.break_chance = break_chance
        self.app_chances = app_chances
        self.app_amt = app_amt

class FinishedGood(object):
    def __init__(self, category, material, in_amt, out_amt):
        # Type, i.e. tools
        self.category = category
        # The resource type that makes this specific good
        self.material = material
        self.break_chance = self.material.break_chance
        
        self.name = self.material.name + ' ' + self.category
        
        # How many of the input materials produce how many of this good
        self.in_amt = in_amt
        self.out_amt = out_amt

        
class Agent(object):
    def pay_taxes(self):
        # Pay taxes. If the other has an owner, pay the taxes to that treasury
        self.gold -= self.economy.local_taxes
        # other owner - should be the city
        if self.economy.owner:
            self.economy.owner.treasury += self.economy.local_taxes
        
    def has_token(self, type_of_item):
        # Test whether or not we have a token of an item
        for token_of_item in COMMODITY_TYPES[type_of_item]:
            if token_of_item.name in self.inventory:
                return True
        return False
        
    def place_bid(self, token_to_bid):
        ## Place a bid in the other
        est_price = self.perceived_values[token_to_bid].center
        uncertainty = self.perceived_values[token_to_bid].uncertainty
        bid_price = roll(est_price - uncertainty, est_price + uncertainty)
        
        if bid_price > self.gold:
            bid_price = self.gold
            
        quantity = roll(1, 2)
        #quantity = 1
        #print self.name, 'bidding for', quantity, token_to_bid
        self.last_turn.append('Bid on ' + str(quantity) + ' ' + token_to_bid + ' for ' + str(bid_price))
        self.economy.auctions[token_to_bid].bids.append(Offer(owner=self, commodity=token_to_bid, price=bid_price, quantity=quantity))
        
    def create_sell(self, sell_item, prod_adj_amt):
        # Determines how many items to sell, and at what cost
        production_cost = self.check_production_cost()
        min_sale_price = int(round( (production_cost/prod_adj_amt)*PROFIT_MARGIN ) )
        ## Prevent our beliefs from getting too out of whack
        if min_sale_price > self.perceived_values[sell_item].center * 2:
            self.perceived_values[sell_item].center = min_sale_price
        
        est_price = self.perceived_values[sell_item].center
        uncertainty = self.perceived_values[sell_item].uncertainty
        # won't go below what they paid for it    
        sell_price = max(roll(est_price - uncertainty, est_price + uncertainty), min_sale_price)

        quantity_to_sell = self.inventory.count(sell_item)
        #print self.name, 'selling', quantity_to_sell, sell_item
        if quantity_to_sell > 0:
            self.last_turn.append('Offered to sell ' + str(quantity_to_sell) + ' ' + sell_item + ' for ' + str(sell_price))
            self.last_turn.append('Prod: ' + str(production_cost) + '; min: ' + str(min_sale_price))
            self.economy.auctions[sell_item].sells.append( Offer(owner=self, commodity=sell_item, price=sell_price, quantity=quantity_to_sell) )
        else:
            self.last_turn.append('Tried to sell ' + sell_item + ' but had none in inventory')
            
    def eval_trade_accepted(self, type_of_item, price):    
        # Then, adjust our belief in the price
        if self.perceived_values[type_of_item].uncertainty >= MIN_CERTAINTY_VALUE:
            self.perceived_values[type_of_item].uncertainty -= ACCEPTED_CERTAINTY_AMOUNT
        
        our_mean = (self.perceived_values[type_of_item].center)
        
        if price > our_mean * P_DIF_THRESH:
            self.perceived_values[type_of_item].center += P_DIF_ADJ
        elif price < our_mean * N_DIF_THRESH:
            # We never let it's worth drop under a certain % of tax money.
            self.perceived_values[type_of_item].center = \
                max(self.perceived_values[type_of_item].center - N_DIF_ADJ, (self.economy.local_taxes) + self.perceived_values[type_of_item].uncertainty)

            
    def eval_bid_rejected(self, type_of_item, price=None):
        # What to do when we've bid on something and didn't get it
        if self.economy.auctions[type_of_item].supply: 
            if price == None:
                self.perceived_values[type_of_item].center += BID_REJECTED_ADJUSTMENT
                self.perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT
            else:
                # Radical re-evaluation of the price
                self.perceived_values[type_of_item].center = price + self.perceived_values[type_of_item].uncertainty
                self.perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT    
        
        
class ResourceGatherer(Agent):
    def __init__(self, name, economy, resource, gather_amount, consumed, essential, preferred):
        self.name = name
        self.economy = economy
        self.resource = resource
        self.gather_amount = gather_amount
        self.consumed = consumed
        self.essential = essential
        self.preferred = preferred
        
        self.turns_since_food = 0
        self.turns_alive = 0
        self.buys = 0
        self.sells = 0
        
        self.able_to_produce = 1
        
        self.gold = 1000
        self.inventory = ['food']
        self.inventory_size = 20
        for i in xrange(gather_amount):
            self.inventory.append(resource)
            
        self.last_turn = []    
        
        ##### dict of what we believe the true price of an item is, for each token of an item we can possibly use
        self.perceived_values = {resource:Value(START_VAL, START_UNCERT)}
        for type_of_item in consumed + essential + preferred:
            for token_of_item in COMMODITY_TYPES[type_of_item]:
                self.perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)
            for token_of_item in COMMODITY_TYPES['foods']:
                self.perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)    
            for i in xrange(roll(0, 1)):
                self.inventory.append(token_of_item.name)
        ##################################################################################
        
    def take_turn(self):
        self.last_turn = []
        #print self.name, 'have:', self.inventory, 'selling:', self.gold
        if self.gold < 0:
            self.economy.resource_gatherers.remove(self)
            if self.economy.owner: self.economy.owner.former_agents.append(self)
            self.economy.add_agent_based_on_token( self.economy.find_most_profitable_agent_token() )
            return None
            
        self.consume_food()    
        self.check_production_ability() # <- will gather resources
        self.eval_need()
        self.pay_taxes()
        self.create_sell(sell_item=self.resource, prod_adj_amt=self.gather_amount) # <- will check to make sure we have items to sell...
        self.turns_alive += 1    
        
    def consume_food(self):
        '''Eat and bid on foods - exclude farmers'''
        if 'Farmer' in self.name and self.able_to_produce:
            self.turns_since_food = 0
            
        else:
            for token_of_item in self.economy.available_types['foods']:
                if token_of_item in self.inventory:
                    self.inventory.remove(token_of_item)
                    self.turns_since_food = 0
                    break
            
            else:
                self.turns_since_food += 1
                if self.turns_since_food > GRANARY_THRESH:
                    self.economy.starving_agents.append(self)
                if self.turns_since_food > STARVATION_THRESH:
                    self.starve()
                    
            ## Bid on food if we have less than a certain stockpile
            if self.inventory.count('food') < FOOD_BID_THRESHHOLD:
                self.place_bid(token_to_bid=random.choice(self.economy.available_types['foods']))
            
    def starve(self):
        '''What happens when we run out of food'''
        print self.name, 'has starved', self.inventory, self.gold, 'gold'
        self.economy.resource_gatherers.remove(self)
        if self.economy.owner: self.economy.owner.former_agents.append(self)
        
    def check_production_ability(self):
        # Check whether we have the right items to gather resources
        critical_items, other_items = self.check_for_needed_items()
        if critical_items == []:
            self.gather_resources()
            
    def eval_need(self):
        critical_items, other_items = self.check_for_needed_items()
        for type_of_item in critical_items + other_items:
            # For now, place a bid for a random item available to use of that type
            token_of_item = random.choice(self.economy.available_types[type_of_item])
            self.place_bid(token_to_bid=token_of_item)    
        
    def gather_resources(self):
        # Gather resources, consume items, and account for breaking stuff
        amount = max(self.inventory_size - len(self.inventory), 0)
        if amount > 0:
            # Add the resource to our own inventory. The government takes half our production for now
            for i in xrange(min(int(self.gather_amount/2), amount)):
                self.inventory.append(self.resource)
            ## Add it to the warehouse, and track how much we have contributed to it this turn    
            if self.economy.owner:
                self.economy.owner.warehouses[self.resource].add(self.resource, int(self.gather_amount/2))
                self.economy.auctions[self.resource].warehouse_contribution += int(self.gather_amount/2)
                
            # Consume any consumables (food is seperate), and then check for other things breaking    
            for type_of_item in self.consumed:
                for token_of_item in self.economy.available_types[type_of_item]:
                    if token_of_item in self.inventory:
                        self.inventory.remove(token_of_item)    
                        break    
            
            for type_of_item in self.preferred + self.essential:
                for token_of_item in self.economy.available_types[type_of_item]:
                    if token_of_item in self.inventory and roll(1, 1000) <= COMMODITY_TOKENS[token_of_item].break_chance:
                        self.inventory.remove(token_of_item)
                        break
                        
            self.last_turn.append('Gathered ' + str(min(self.gather_amount, amount)) + ' ' + str(self.resource))
        #else:
        #    print self.name, '- inventory too large to gather resources:', self.inventory
        
    def check_for_needed_items(self):
        # Make a list of items we need to gather resources
        critical_items = [type_of_item for type_of_item in self.consumed + self.essential if not self.has_token(type_of_item)]
        other_items = [type_of_item for type_of_item in self.preferred if not self.has_token(type_of_item)]
        return critical_items, other_items
        
    def check_production_cost(self):
        production_cost = 0
        # These items are required for production, but not used. Find the item's cost * (break chance/1000) to find avg cost
        for type_of_item in self.essential + self.preferred:
            for token_of_item in self.economy.available_types[type_of_item]:
                if token_of_item in self.inventory:
                    production_cost += int(round(self.economy.auctions[token_of_item].mean_price * (COMMODITY_TOKENS[token_of_item].break_chance/1000)))
                    break
            
        for type_of_item in self.consumed:
            for token_of_item in self.economy.available_types[type_of_item]:
                if token_of_item in self.inventory:
                    production_cost += int(round(self.economy.auctions[token_of_item].mean_price * (COMMODITY_TOKENS[token_of_item].break_chance/1000)))
                    break

        for token_of_item in self.economy.available_types['foods']:
            if token_of_item in self.inventory:
                production_cost += int(round(self.economy.auctions[token_of_item].mean_price * (COMMODITY_TOKENS[token_of_item].break_chance/1000)))
                break            
        # Take into account the taxes we pay
        production_cost += (self.economy.local_taxes)
        
        return production_cost
        
    def eval_sell_rejected(self, type_of_item):
        # What to do when we put something up for sale and nobody bought it. Only adjust if there was a demand
        if self.economy.auctions[type_of_item].demand:
            production_cost = self.check_production_cost()
            min_sale_price = int(round((production_cost/self.gather_amount)*PROFIT_MARGIN))
            
            self.perceived_values[type_of_item].center = max(self.perceived_values[type_of_item].center - ASK_REJECTED_ADJUSTMENT, min_sale_price + self.perceived_values[type_of_item].uncertainty)
            #self.perceived_values[type_of_item].center = self.perceived_values[type_of_item].center - ASK_REJECTED_ADJUSTMENT
            self.perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT
                
        
class GoodProducer(Agent):
    def __init__(self, name, economy, finished_good, consumed, essential, preferred):    
        self.name = name
        self.economy = economy
        self.finished_goods = finished_good
        self.consumed = consumed
        self.essential = essential
        self.preferred = preferred
        
        self.in_amt = finished_good.in_amt
        self.out_amt = finished_good.out_amt
        
        self.input = finished_good.material.name
        self.output = finished_good.name
        
        self.turns_since_food = 0
        self.turns_alive = 0
        self.buys = 0
        self.sells = 0
        
        self.last_turn = []
        
        self.gold = 1000
        self.inventory = ['food', 'food', 'food', self.input, self.input, finished_good.name, finished_good.name]
        self.inventory_size = 20
        
        self.perceived_values = {finished_good.name:Value(START_VAL, START_UNCERT), self.input:Value(START_VAL, START_UNCERT)}
        for type_of_item in consumed + essential + preferred:
            for token_of_item in COMMODITY_TYPES[type_of_item]:
                self.perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)
            for token_of_item in COMMODITY_TYPES['foods']:
                self.perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)        
                
            for i in xrange(1):
                self.inventory.append(token_of_item.name)
    #end init.           
    #########################################################            
                
    def take_turn(self):
        self.last_turn = []
        #print self.name, 'have:', self.inventory, 'selling:', self.gold
        if self.gold < 0:
            self.economy.good_producers.remove(self)
            if self.economy.owner: self.economy.owner.former_agents.append(self)
            self.economy.add_agent_based_on_token( self.economy.find_most_profitable_agent_token() )
            return None
            
        self.consume_food()    
        self.check_production_ability() # <- will gather resources
        self.eval_need()
        self.pay_taxes()
        self.create_sell(sell_item=self.finished_goods.name, prod_adj_amt=self.out_amt) # <- will check to make sure we have items to sell...
        self.turns_alive += 1    
        
    def consume_food(self):
        '''Eat and bid on foods'''
        for token_of_item in self.economy.available_types['foods']:
            if token_of_item in self.inventory:
                ## Only consume food every ~5 turns
                if roll(1, 5) == 1:
                    self.inventory.remove(token_of_item)
                    self.turns_since_food = 0
                    break
                else:
                    self.turns_since_food = 0
                    break
        
        else:
            self.turns_since_food += 1
            if self.turns_since_food > GRANARY_THRESH * 5:
                self.economy.starving_agents.append(self)
            if self.turns_since_food > STARVATION_THRESH * 5:
                self.starve()
                
        ## Bid on food if we have less than a certain stockpile
        if self.inventory.count('food') < FOOD_BID_THRESHHOLD:
            self.place_bid(token_to_bid=random.choice(self.economy.available_types['foods']))
            
    def starve(self):
        '''What happens when we run out of food'''
        print self.name, 'has starved'
        self.economy.good_producers.remove(self)
        if self.economy.owner: self.economy.owner.former_agents.append(self)                
                
                
    def check_production_ability(self):
        # Check whether we have the right input item, and the other necessary items        
        has_required_input = False
        if self.inventory.count(self.input) >= self.in_amt:
            has_required_input = True
        
        critical_items, other_items = self.check_for_needed_items()
        if critical_items == [] and has_required_input and (self.inventory_size - len(self.inventory) > 0):
            self.produce_items()
        #else:
        #    print self.name, '- not producing because: critical items-', critical_items, 'required_input', has_required_input, 'inventory:', self.inventory
            
    def eval_need(self):
        critical_items, other_items = self.check_for_needed_items()

        for type_of_item in critical_items + other_items:
            # For now, place a bid for a random item available to use of that type
            token_of_item = random.choice(self.economy.available_types[type_of_item])
            self.place_bid(token_to_bid=token_of_item)    
        
        if self.inventory.count(self.input) <= self.in_amt*2:
            self.place_bid(token_to_bid=self.input)
        
    def produce_items(self):
        # Gather resources, consume items, and account for breaking stuff
        for i in xrange(self.in_amt):
            self.inventory.remove(self.input)
            
        for i in xrange(self.out_amt):
            self.inventory.append(self.output)            
        
        for type_of_item in self.consumed:
            for token_of_item in self.economy.available_types[type_of_item]:
                if token_of_item in self.inventory:
                    self.inventory.remove(token_of_item)
                    break    
        
        for type_of_item in self.essential + self.preferred:
            for token_of_item in self.economy.available_types[type_of_item]:
                if token_of_item in self.inventory and roll(1, 1000) <= COMMODITY_TOKENS[token_of_item].break_chance:
                    self.inventory.remove(token_of_item)    
                    break
                    
        self.last_turn.append('Produced ' + str(self.out_amt) + ' ' + self.output)
        
    def check_for_needed_items(self):
        # Make a list of items we need to produce items
        critical_items = [type_of_item for type_of_item in self.consumed + self.essential if not self.has_token(type_of_item)]
        other_items = [type_of_item for type_of_item in self.preferred if not self.has_token(type_of_item)]
        return critical_items, other_items
        
    def check_production_cost(self):
        production_cost = 0
        # Cost of input is historical mean * the amount we use (since they are used up every 
        # time we need to make something, we're using the full value of the items)
        production_cost += (self.economy.auctions[self.input].mean_price * self.in_amt)
        # These items are required for production, but not used. 
        # Find the item's cost * (break chance/1000) to find avg cost
        for type_of_item in self.essential + self.preferred:
            for token_of_item in self.economy.available_types[type_of_item]:
                if token_of_item in self.inventory:
                    production_cost += int(round(self.economy.auctions[token_of_item].mean_price * (COMMODITY_TOKENS[token_of_item].break_chance/1000)))
                    break
            
        for type_of_item in self.consumed:
            for token_of_item in self.economy.available_types[type_of_item]:
                if token_of_item in self.inventory:
                    production_cost += int(round(self.economy.auctions[token_of_item].mean_price * (COMMODITY_TOKENS[token_of_item].break_chance/1000)))
                    break
                    
        for token_of_item in self.economy.available_types['foods']:
            if token_of_item in self.inventory:
                production_cost += int(round(self.economy.auctions[token_of_item].mean_price * (COMMODITY_TOKENS[token_of_item].break_chance/1000)))
                break                    

        # Take into account the taxes we pay
        production_cost += (self.economy.local_taxes)
        
        return production_cost    
        
    def eval_sell_rejected(self, type_of_item):
        # What to do when we put something up for sale and nobody bought it. Only adjust if there was a demand
        if self.economy.auctions[type_of_item].demand: 
            production_cost = self.check_production_cost()
            min_sale_price = int(round((production_cost/self.in_amt)*PROFIT_MARGIN))
            
            #self.perceived_values[type_of_item].center = max(self.perceived_values[type_of_item].center - ASK_REJECTED_ADJUSTMENT, min_sale_price + self.perceived_values[type_of_item].uncertainty)
            self.perceived_values[type_of_item].center = self.perceived_values[type_of_item].center - ASK_REJECTED_ADJUSTMENT
            self.perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT
    
        
class Merchant(object):
    def __init__(self, name, buy_economy, sell_economy, traded_item, consumed, essential, preferred, attached_to=None):
        self.name = name
        self.buy_economy = buy_economy
        self.sell_economy = sell_economy
        self.traded_item = traded_item
        self.consumed = consumed
        self.essential = essential
        self.preferred = preferred
        
        self.attached_to = attached_to
        if self.attached_to != None:
            self.attached_to.sapient.economy_agent = self
        
        self.turns_alive = 0
        self.buys = 0
        self.sells = 0
        
        self.gold = 10000
        self.INVENTORY_SIZE = 20
        self.inventory = ['food', 'food', traded_item, traded_item]
        
        self.last_turn = []
        
        self.current_location = random.choice([buy_economy, sell_economy])
        if self.current_location == self.sell_economy:
            for i in xrange(10):
                self.inventory.append(self.traded_item)
        self.time_here = roll(1, 3)
        self.cycle_length = 4
        
        ##### dict of what we believe the true price of an item is, for each token of an item we can possibly use
        self.buy_perceived_values = {traded_item:Value(START_VAL, START_UNCERT)} 
        self.sell_perceived_values = {traded_item:Value(START_VAL*2, START_UNCERT)}
        
        for type_of_item in consumed + essential + preferred:
            for token_of_item in COMMODITY_TYPES[type_of_item]:
                if token_of_item != self.traded_item:
                    self.buy_perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)
                    self.sell_perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)
                self.inventory.append(token_of_item.name)
                
        for token_of_item in COMMODITY_TYPES['foods']:
            if token_of_item != self.traded_item:
                self.buy_perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)
                self.sell_perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)        

        ##################################################################################
    def consume_food(self):
        '''Eat and bid on foods'''
        for token_of_item in self.current_location.available_types['foods']:
            if token_of_item in self.inventory:
                ## Only consume food every ~5 turns
                if roll(1, 5) == 1:
                    self.inventory.remove(token_of_item)
                    self.turns_since_food = 0
                    break
                else:
                    self.turns_since_food = 0
                    break
        
        else:
            self.turns_since_food += 1
            if self.turns_since_food > GRANARY_THRESH * 5:
                self.current_location.starving_agents.append(self)
            if self.turns_since_food > STARVATION_THRESH * 5:
                self.starve()
                
        ## Bid on food if we have less than a certain stockpile
        if self.inventory.count('food') < FOOD_BID_THRESHHOLD:
            self.place_bid(economy=self.current_location, token_to_bid=random.choice(self.current_location.available_types['foods']))
            
    def starve(self):
        '''What happens when we run out of food'''
        self.buy_economy.buy_merchants.remove(self)
        self.sell_economy.sell_merchants.remove(self)
        if self.economy.owner: self.economy.owner.former_agents.append(self)        
        
        
    def bankrupt(self):
        self.buy_economy.buy_merchants.remove(self)
        self.sell_economy.sell_merchants.remove(self)
        
    def increment_cycle(self):
        self.time_here += 1
        if (self.current_location == self.buy_economy and len(self.inventory) > self.INVENTORY_SIZE - 2) or \
            (self.current_location == self.sell_economy and self.inventory.count(self.traded_item) == 0):
            self.time_here = 0
            ## if it's part of the game, add to a list of departing merchants so they can create a caravan
            if self.current_location.owner:
                if self.current_location == self.buy_economy:      destination = self.sell_economy.owner
                elif self.current_location == self.sell_economy: destination = self.buy_economy.owner
                #print self.attached_to.sapient.caravan.name, 'heading to', destination.name
                self.current_location.owner.departing_merchants.append((self.attached_to.sapient.caravan, destination))
                self.current_location = None
                
            else:            
                if self.current_location == self.buy_economy:    self.current_location = self.sell_economy
                elif self.current_location == self.sell_economy: self.current_location = self.buy_economy
            
    def pay_taxes(self, economy):
        # Pay taxes. If the other has an owner, pay the taxes to that treasury
        self.gold -= economy.local_taxes
        # other owner - should be the city
        if economy.owner:
            economy.owner.treasury += economy.local_taxes
        
    def has_token(self, type_of_item):
        # Test whether or not we have a token of an item
        for token_of_item in COMMODITY_TYPES[type_of_item]:
            if token_of_item.name in self.inventory:
                return True
        return False
        
    def place_bid(self, economy, token_to_bid):
        ## Place a bid in the other
        if self.current_location == self.buy_economy:
            est_price = self.buy_perceived_values[token_to_bid].center
            uncertainty = self.buy_perceived_values[token_to_bid].uncertainty            
        elif self.current_location == self.sell_economy:    
            est_price = self.sell_perceived_values[token_to_bid].center
            uncertainty = self.sell_perceived_values[token_to_bid].uncertainty
        
        bid_price = roll(est_price - uncertainty, est_price + uncertainty)
        if bid_price > self.gold:
            bid_price = self.gold
            
        if token_to_bid == self.traded_item: quantity = self.INVENTORY_SIZE - (len(self.inventory) + 1)
        else:                                  quantity = roll(1, 2)
        #print self.name, 'bidding on', quantity, token_to_bid, 'for', bid_price, 'at', self.current_location.owner.name
        #print self.name, 'bidding for', quantity, token_to_bid
        if quantity > 0:
            self.last_turn.append('Bid on ' + str(quantity) + ' ' + token_to_bid + ' for ' + str(bid_price))
            economy.auctions[token_to_bid].bids.append(Offer(owner=self, commodity=token_to_bid, price=bid_price, quantity=quantity))
        else:
            self.last_turn.append('Tried to bid on ' + token_to_bid + ' but quantity not > 0')
        
    def create_sell(self, economy, sell_item):
        # Determines how many items to sell, and at what cost
        production_cost = self.check_min_sell_price()
        min_sale_price = int(round( production_cost*PROFIT_MARGIN ) )
        
        est_price = self.sell_perceived_values[sell_item].center
        uncertainty = self.sell_perceived_values[sell_item].uncertainty
        # won't go below what they paid for it    
        sell_price = max(roll(est_price - uncertainty, est_price + uncertainty), min_sale_price)

        quantity_to_sell = self.inventory.count(sell_item)
        #print self.name, 'selling', quantity_to_sell, sell_item
        if quantity_to_sell > 0:
            #print self.name, 'selling', quantity_to_sell, sell_item, 'for', sell_price, 'at', self.current_location.owner.name
            self.last_turn.append('Offered to sell ' + str(quantity_to_sell) + ' ' + sell_item + ' for ' + str(sell_price))
            economy.auctions[sell_item].sells.append( Offer(owner=self, commodity=sell_item, price=sell_price, quantity=quantity_to_sell) )
        else:
            self.last_turn.append('Tried to sell ' + sell_item + ' but inventory was empty')
            
    def eval_trade_accepted(self, type_of_item, price):    
        # Then, adjust our belief in the price
        if self.current_location == self.buy_economy:
            if self.buy_perceived_values[type_of_item].uncertainty >= MIN_CERTAINTY_VALUE:
                self.buy_perceived_values[type_of_item].uncertainty -= ACCEPTED_CERTAINTY_AMOUNT
            
            our_mean = (self.buy_perceived_values[type_of_item].center)
            
            if price > our_mean * P_DIF_THRESH:
                self.buy_perceived_values[type_of_item].center += P_DIF_ADJ
            elif price < our_mean * N_DIF_THRESH:
                # We never let it's worth drop under a certain % of tax money.
                self.buy_perceived_values[type_of_item].center = \
                    max(self.buy_perceived_values[type_of_item].center - N_DIF_ADJ, (self.buy_economy.local_taxes) + self.buy_perceived_values[type_of_item].uncertainty)
        
        elif self.current_location == self.sell_economy:
            if self.sell_perceived_values[type_of_item].uncertainty >= MIN_CERTAINTY_VALUE:
                self.sell_perceived_values[type_of_item].uncertainty -= ACCEPTED_CERTAINTY_AMOUNT
            
            our_mean = (self.sell_perceived_values[type_of_item].center)
            
            if price > our_mean * P_DIF_THRESH:
                self.sell_perceived_values[type_of_item].center += P_DIF_ADJ
            elif price < our_mean * N_DIF_THRESH:
                # We never let it's worth drop under a certain % of tax money.
                self.sell_perceived_values[type_of_item].center = \
                    max(self.sell_perceived_values[type_of_item].center - N_DIF_ADJ, (self.sell_economy.local_taxes) + self.sell_perceived_values[type_of_item].uncertainty)

                    
    def eval_bid_rejected(self, type_of_item, price=None):
        # What to do when we've bid on something and didn't get it
        if self.current_location.auctions[type_of_item].supply:
            if self.current_location == self.buy_economy:
                if price == None:
                    self.buy_perceived_values[type_of_item].center += BID_REJECTED_ADJUSTMENT
                    self.buy_perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT
                else:
                    # Radical re-evaluation of the price
                    self.buy_perceived_values[type_of_item].center = price + self.buy_perceived_values[type_of_item].uncertainty
                    self.buy_perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT        
            
            elif self.current_location == self.sell_economy:
                if price == None:
                    self.sell_perceived_values[type_of_item].center += BID_REJECTED_ADJUSTMENT
                    self.sell_perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT
                else:
                    # Radical re-evaluation of the price
                    self.sell_perceived_values[type_of_item].center = price + self.sell_perceived_values[type_of_item].uncertainty
                    self.sell_perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT    
            
    def eval_need(self):
        # bid for food if we have < 5 units:
        if self.inventory.count('food') <= 5:
            self.place_bid(economy=self.current_location, token_to_bid='food')
        
        critical_items, other_items = self.check_for_needed_items()
        for type_of_item in critical_items + other_items:
            if type_of_item != 'foods':
                # For now, place a bid for a random item available to use of that type
                token_of_item = random.choice(self.current_location.available_types[type_of_item])
                self.place_bid(economy=self.current_location, token_to_bid=token_of_item.name)
        
    def check_for_needed_items(self):
        # Make a list of items we need 
        critical_items = [type_of_item for type_of_item in self.consumed + self.essential if not self.has_token(type_of_item)]
        other_items = [type_of_item for type_of_item in self.preferred if not self.has_token(type_of_item)]
        return critical_items, other_items
        
    def check_min_sell_price(self):
        production_cost = self.buy_perceived_values[self.traded_item].center
        # These items are required for production, but not used. Find the item's cost * (break chance/1000) to find avg cost
        for type_of_item in self.consumed + self.essential + self.preferred:
            for token_of_item in COMMODITY_TYPES[type_of_item]:
                if token_of_item in self.inventory:
                    production_cost += int(round(self.buy_economy.auctions[token_of_item].mean_price * (COMMODITY_TOKENS[token_of_item].break_chance/1000)))
                    break
        # Take into account the taxes we pay
        production_cost += (self.buy_economy.local_taxes)        
        return production_cost
        

    def eval_sell_rejected(self, type_of_item):
        # What to do when we put something up for sale and nobody bought it
        if self.current_location.auctions[type_of_item].demand:
            production_cost = self.check_min_sell_price()
            min_sale_price = int(round(production_cost*PROFIT_MARGIN))
            if self.current_location == self.buy_economy:
                #self.perceived_values[type_of_item].center = max(self.perceived_values[type_of_item].center - ASK_REJECTED_ADJUSTMENT, min_sale_price + self.perceived_values[type_of_item].uncertainty)
                self.buy_perceived_values[type_of_item].center = self.buy_perceived_values[type_of_item].center - ASK_REJECTED_ADJUSTMENT
                self.buy_perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT        
            elif self.current_location == self.sell_economy:
                self.sell_perceived_values[type_of_item].center = self.sell_perceived_values[type_of_item].center - ASK_REJECTED_ADJUSTMENT
                self.sell_perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT    
            
        
def roll(a, b):
    return random.randint(a, b)
    
class Value:
    # Agents' perceived values of objects
    def __init__(self, center, uncertainty):
        self.center = center + roll(-2, 2)
        self.uncertainty = uncertainty + roll(-2, 2)
        
class Auction:
    # Seperate "auction" for each commodity
    # Runs each round of bidding, as well as archives historical price info
    def __init__(self, commodity):
        self.commodity = commodity
        self.bids = []
        self.sells = []
        self.price_history = [START_VAL]
        self.mean_price = START_VAL
        self.iterations = 0
        
        self.supply = None
        self.demand = None
        self.warehouse_contribution = 0
    
    def update_mean_price(self):
        # update the mean price for this commodity by averaging over the last HIST_WINDOW_SIZE items
        self.mean_price = int(round(sum(self.price_history[-HIST_WINDOW_SIZE:])/len(self.price_history[-HIST_WINDOW_SIZE:])))
        
class Offer:
    # An offer that goes into the auction's "bids" or "sells".
    # Bids and sells are then compared against each other and agents meet at the middle
    def __init__(self, owner, commodity, price, quantity):
        self.owner = owner
        self.commodity = commodity
        self.price = price
        self.quantity = quantity        
        
class Economy:
    def __init__(self, native_resources, local_taxes, owner=None):
        self.native_resources = native_resources
        self.available_types = {}
        # Should be the city where this other is located
        self.owner = owner
        
        # Agents belonging to this other
        self.resource_gatherers = []
        self.good_producers = []
        self.buy_merchants = []
        self.sell_merchants = []
        
        self.starving_agents = []
        # Auctions that take place in this other
        self.auctions = {}
        self.prices = {}
        
        # Amount of gold paid in taxes each turn
        self.local_taxes = local_taxes
            
    def add_commodity_to_economy(self, commodity):
        category = COMMODITY_TOKENS[commodity].category
        if category in self.available_types.keys():
            if commodity not in self.available_types[category]:
                self.available_types[category].append(commodity)
                self.auctions[commodity] = Auction(commodity)
        else:
            self.available_types[category] = [commodity]
            self.auctions[commodity] = Auction(commodity)
                
    def add_random_agent(self):
        if roll(0, 1):
            commodity = random.choice(RESOURCES)
            self.add_resource_gatherer(commodity.name)
        else:
            commodity = random.choice(GOODS)
            self.add_goods_producer(commodity.name)
                
    def add_resource_gatherer(self, resource):
        info = gatherers_by_token[resource]
        gatherer = ResourceGatherer(name=info['name'], economy=self, resource=resource, gather_amount=COMMODITY_TOKENS[resource].gather_amount, consumed=info['consumed'], essential=info['essential'], preferred=info['preferred'] )
        self.resource_gatherers.append(gatherer)
        # Test if it's in the other and add it if not
        self.add_commodity_to_economy(resource)
        
    def add_goods_producer(self, good):
        info = producers_by_token[good]
        producer = GoodProducer(name=info['name'], economy=self, finished_good=COMMODITY_TOKENS[good], consumed=info['consumed'], essential=info['essential'], preferred=info['preferred'] )
        self.good_producers.append(producer)
        # Test if it's in the other and add it if not
        self.add_commodity_to_economy(good)
        
    def add_merchant(self, sell_economy, traded_item, attached_to=None):
        info = merchants_by_token['merchant']
        merchant = Merchant(name=traded_item + ' merchant', buy_economy=self, sell_economy=sell_economy, traded_item=traded_item, consumed=info['consumed'], essential=info['essential'], preferred=info['preferred'], attached_to=attached_to)
        
        self.buy_merchants.append(merchant)
        sell_economy.sell_merchants.append(merchant)
        # Test if it's in the other and add it if not
        self.add_commodity_to_economy(traded_item)
        sell_economy.add_commodity_to_economy(traded_item)
        return merchant
        
    def add_agent_based_on_token(self, token):
        ''' If we only have a token and don't know whether it's a resource or a commodity,
        this function helps us figure out which method to call'''
        for resource in RESOURCES:
            if resource.name == token:
                self.add_resource_gatherer(token)
                return None
        for good in GOODS:
            if good.name == token:
                self.add_goods_producer(token)
                return None
        
    def find_most_profitable_agent_token(self):
        ### First build a dict of agents, their gold, and the # of agents
        # key = commodity, value = [gold, #_of_agents]
        tokens_of_commodity = {}
        for agent in self.resource_gatherers:
            if agent.resource in tokens_of_commodity.keys(): 
                tokens_of_commodity[agent.resource][0] += agent.gold
                tokens_of_commodity[agent.resource][1] += 1
            else:                                                     
                tokens_of_commodity[agent.resource] = [agent.gold, 1]
        for agent in self.good_producers:
            if agent.output in tokens_of_commodity.keys(): 
                tokens_of_commodity[agent.output][0] += agent.gold
                tokens_of_commodity[agent.output][1] += 1
            else:                                           
                tokens_of_commodity[agent.output] = [agent.gold, 1]

        ### Now choose the best one based off of the ratio of gold to agents
        best_ratio = 0
        best_commodity = None
        for commodity, [gold, agent_num] in tokens_of_commodity.iteritems():
            if gold/agent_num > best_ratio:
                best_commodity, best_ratio = commodity, gold/agent_num
                
        return best_commodity
        
    def run_simulation(self):
        ''' Run a simulation '''
        # First, each agent does what they do
        for resource_gatherer in self.resource_gatherers[:]:
            resource_gatherer.take_turn()
                
        for producer in self.good_producers[:]:
            producer.take_turn()
            
        for merchant in self.buy_merchants[:]:
            merchant.last_turn = []
            if merchant.current_location == self:
                if merchant.gold < 0:
                    merchant.bankrupt()
                    break
                merchant.consume_food()
                merchant.eval_need()
                merchant.pay_taxes(self)
                merchant.place_bid(economy=self, token_to_bid=merchant.traded_item) # <- will bid max amt we can
                merchant.turns_alive += 1
            
        for merchant in self.sell_merchants[:]:
            merchant.last_turn = []
            if merchant.current_location == self:
                if merchant.gold < 0:
                    merchant.bankrupt()
                    break
                merchant.consume_food()
                merchant.eval_need()
                merchant.pay_taxes(self)    
                merchant.create_sell(economy=self, sell_item=merchant.traded_item)
                merchant.turns_alive += 1
                    
        if self.owner:
            for agent in self.starving_agents:
                if self.owner.warehouses['food'] > 1:
                    self.owner.warehouses['food'].remove('food', 1)
                    agent.inventory.append('food')
                    
        ## Run the auction
        for commodity, auction in self.auctions.iteritems():
            auction.iterations += 1
            ## Sort the bids by price (highest to lowest) ##
            auction.bids = sorted(auction.bids, key=lambda attr: attr.price, reverse=True)
            ## Sort the sells by price (lowest to hghest) ##
            auction.sells = sorted(auction.sells, key=lambda attr: attr.price)
            
            self.prices[commodity] = []
            
            num_bids = len(auction.bids)
            num_sells = len(auction.sells)
            
            if num_bids > 0 or num_sells > 0:
                auction.supply = sum(offer.quantity for offer in auction.sells)
                auction.demand = sum(offer.quantity for offer in auction.bids)
            #print commodity + ': ' + str(num_bids) + ' bids, ' + str(num_sells) + ' sells'
            #for x in range(min(num_bids, num_sells)):
                #if auction.bids[x].price > auction.sells[x].price:
                #print(commodity + ': ' + str(auction.bids[x].price) + ', ' + str(auction.sells[x].price))
            while not len(auction.bids) == 0 and not len(auction.sells) == 0:    
                buyer = auction.bids[0]
                seller = auction.sells[0]
                ## Allow the buyer to make some radical readjustments the first few turns it's alive
                if buyer.price < seller.price and (buyer.owner.turns_alive < 10 or (commodity == 'food' and buyer.owner.turns_since_food > 2)):
                    buyer.price = int(round(seller.price * 1.5))
                    buyer.owner.eval_bid_rejected(commodity, int(round(seller.price * 1.5)))
                
                ## If the price is still lower than the seller
                if buyer.price < seller.price:
                    buyer.owner.eval_bid_rejected(commodity, seller.price)
                    buyer.quantity = 0                
                    
                else:
                    # Determine price/amount
                    quantity = min(buyer.quantity, seller.quantity)
                    price = int(round((buyer.price + seller.price)/2))
                            
                    if quantity > 0:
                        #print buyer.owner.name, 'bought', quantity, commodity, 'from', seller.owner.name, 'at', price
                        # Adjust buyer/seller requested amounts
                        buyer.quantity -= quantity
                        seller.quantity -= quantity
                        
                        buyer.owner.eval_trade_accepted(buyer.commodity, price)                                
                        seller.owner.eval_trade_accepted(buyer.commodity, price)
                        
                        ## Update inventories and gold counts
                        for i in xrange(quantity):
                            buyer.owner.inventory.append(buyer.commodity)                            
                            seller.owner.inventory.remove(seller.commodity)
                                
                        buyer.owner.gold -= (price*quantity)
                        seller.owner.gold += (price*quantity)
                        
                        buyer.owner.buys += quantity
                        buyer.owner.last_turn.append('Bought ' + str(quantity) + ' ' + commodity + ' from ' + seller.owner.name + ' at ' + str(price))
                        seller.owner.sells += quantity
                        seller.owner.last_turn.append('Sold ' + str(quantity) + ' ' + commodity + ' to ' + buyer.owner.name + ' at ' + str(price))
                        
                        # Add to running tally of prices this turn
                        self.prices[commodity].append(price)
                
                # Now that a transaction has occured, bump out the buyer or seller if either is satasfied
                if seller.quantity == 0: del auction.sells[0]
                if buyer.quantity == 0: del auction.bids[0]
                    
            # All bidders re-evaluate prices - currently too simplistic
            if len(auction.bids) > 0:
                for buyer in auction.bids:
                    buyer.owner.eval_bid_rejected(buyer.commodity)
                self.auctions[commodity].bids = []
            
            # All sellers re-evaluate prices - too simplistic as well
            elif len(auction.sells) > 0:
                for seller in auction.sells:    
                    seller.owner.eval_sell_rejected(seller.commodity)    
                self.auctions[commodity].sells = []
            
            ## Average prices        
            if len(self.prices[commodity]) > 0:
                self.price_mean = int(round(sum(self.prices[commodity])/len(self.prices[commodity])))
                auction.price_history.append(self.price_mean)
                # Track mean price for last N turns
                auction.update_mean_price()
                #print (auction.commodity + ': ' + str(auction.mean_price) + '. This round: ' + 
                #str(len(prices[commodity])) + ' ' + commodity + ' averaged at $' + str(price_mean) +
                #' (' + str(num_bids) + ' bids, ' + str(num_sells) + ' sells)')
            elif auction.commodity is not 'nothing':
                auction.price_history.append(auction.price_history[-1])
                #print (commodity + ' was not sold this round (' + str(num_bids) + ' bids, ' + str(num_sells) + ' sells)')
                
            ## Add information about how much stuff we've taken into that warehouse
            if self.owner:
                del self.owner.warehouses[commodity].in_history[0]
                self.owner.warehouses[commodity].in_history.append(auction.warehouse_contribution)
            auction.warehouse_contribution = 0    
                
            
        ## Merchants evaluate whether or not to move on to the next city
        for merchant in self.buy_merchants + self.sell_merchants:
            if merchant.current_location == self:
                merchant.increment_cycle()
        ## Add some information to the city's food supply/demand
        if self.owner:        
            del self.owner.food_supply[0]
            del self.owner.food_demand[0]
            self.owner.food_supply.append(self.auctions['food'].supply)
            self.owner.food_demand.append(self.auctions['food'].demand)
            
    def graph_results(self, solid, dot):
        # Spit out some useful info    about the other
        overall_history = []
        # Bad hack to transpose matix so plot() works correctly
        for i in xrange(len(self.auctions['food'].price_history)):
            overall_history.append([])
            for auction in self.auctions.itervalues():
                overall_history[i].append(auction.price_history[i])
            
        # Split in half so graph is easier to read
        if len(dot) == 0:
            half_items = int(round(len(solid)/2))
            dot = solid[:-half_items]
            solid = solid[-half_items:]
                    
        ## Solid lines
        for item in solid:
            plot(self.auctions[item].price_history, lw=3.0, alpha=.6)
            
        ## Dotted lines
        for item in dot:
            plot(self.auctions[item].price_history, '--', lw=3.0, alpha=.6)
            
        ## Legend for graph
        glegend = []
        for thing in solid:
            glegend.append(thing)
        for thing in dot:
            glegend.append(thing)
            
        ## Add legend and show graph
        legend(glegend, loc=2, prop={'size':7})
        grid(True)
        show()
            
        ## Show agent nums
        agent_nums = {}
        for agent in self.agents:
            try: agent_nums[agent.name] += 1
            except: agent_nums[agent.name] = 1
        
        print str(len(self.agents)), agent_nums
        
    
def main():
    setup_resources()
    economy_test_run()
    
if __name__ == '__main__':
    main()
    