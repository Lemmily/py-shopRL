'''
Created on 23 Mar 2013

@author: Emily

For each class it will be noted if it is for use in macro(between cities) or micro(in the cities between people) economy, or both.


'''
import libtcodpy as libtcod
import json
import json_resources
import entities
import R
import random


data = json.loads(json_resources.raw_resources)
#city = json.loads(json_resources.city_gatherers_templates)


HIST_WINDOW_SIZE = 5 

START_VAL = 40
START_UNCERT = 10

PROFIT_MARGIN = 1.1

MIN_CERTAINTY_VALUE = 8 ## Within what range traders are limited to estimating the market price
BID_REJECTED_ADJUSTMENT = 5 # Adjust prices by this much when our bid is rejected
ASK_REJECTED_ADJUSTMENT = 5 # Adjust prices by this much when nobody buys our stuff
REJECTED_UNCERTAINTY_AMOUNT = 2 # We get this much more uncertain about a price when an offer is rejected
ACCEPTED_CERTAINTY_AMOUNT = 1  # Out uncertainty about a price decreases by this amount when an offer is accepted

P_DIF_ADJ = 3  # When offer is accepted and exceeds what we thought the price value was, adjust it upward by this amount
N_DIF_ADJ = 3  # When offer is accepted and is lower than what we thought the price value was, adjust it downward by this amount
P_DIF_THRESH = 2.5  #Threshhold at which adjustment of P_DIF_ADJ is added to the perceived value of a commodity
N_DIF_THRESH = 2.5 #Threshhold at which adjustment of P_DIF_ADJ is subtracted from the perceived value of a commodity

GRANARY_THRESH = 5
STARVATION_THRESH = 10

FOOD_BID_THRESH = 4

def setup_resources():
    global RESOURCES, RESOURCE_TYPES, GOODS, GOODS_TYPES, COMMODITY_TYPES, COMMODITY_TOKENS
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
    ### half go to the government and aren't used in the economy. Each round, if a random number
    ### between 1 and 1000 is less than break_chance, a goods made out of the resouce will be destroyed
    copper = Resource(name='copper', category='ores', resource_class='strategic', gather_amount=4, break_chance=200, app_chances=ore_app, app_amt=amt)
    bronze = Resource(name='bronze', category='ores', resource_class='strategic', gather_amount=4, break_chance=100, app_chances=ore_app, app_amt=amt)
    iron = Resource(name='iron', category='ores', resource_class='strategic', gather_amount=3,  break_chance=60, app_chances=ore_app, app_amt=amt)
    food = Resource(name='food', category='foods', resource_class='strategic', gather_amount=8, break_chance=1, app_chances=food_app, app_amt=amt)
    clay = Resource(name='clay', category='clays', resource_class='strategic', gather_amount=4, break_chance=200, app_chances=clay_app, app_amt=amt)
    silt = Resource(name='silt', category='clays', resource_class='strategic', gather_amount=4, break_chance=350, app_chances=silt_app, app_amt=amt)
    wood = Resource(name='wood', category='woods', resource_class='strategic', gather_amount=4, break_chance=180, app_chances=wood_app, app_amt=amt)
    #oak = Resource(name='oak', category='woods', resource_class='strategic', gather_amount=3, break_chance=200, app_chances=wood_app, app_amt=amt)
    flax = Resource(name='flax', category='cloths', resource_class='strategic', gather_amount=4, break_chance=250, app_chances=flax_app, app_amt=amt)
            
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
    iron_sword = FinishedGood(category='weapons', material=iron,   in_amt=2, out_amt=1, name = "iron sword")
    copper_sword = FinishedGood(category='weapons', material=copper,   in_amt=2, out_amt=1, name = "copper sword")
            
    GOODS = [copper_tools, bronze_tools, iron_tools, silt_pottery, clay_pottery, wood_furniture, flax_clothing, iron_sword, copper_sword]
    GOODS_TYPES = {}
    GOODS_BY_RESOURCE_TOKEN = {}
    ## Key = category, calue = list of resources
    for goods in GOODS:
        COMMODITY_TOKENS[goods.name] = goods
        
        if not goods.category in GOODS_TYPES: GOODS_TYPES[goods.category] = [goods]
        else:                                  GOODS_TYPES[goods.category].append(goods)
            
        if not goods.category in COMMODITY_TYPES.keys(): COMMODITY_TYPES[goods.category] = [goods]
        else:                                            COMMODITY_TYPES[goods.category].append(goods)    
        
        if not goods.category in GOODS_BY_RESOURCE_TOKEN.keys(): GOODS_BY_RESOURCE_TOKEN[goods.material.name] = [goods]
        else:                                                    GOODS_BY_RESOURCE_TOKEN[goods.material.name].append(goods)
    
    ################### AGENT TYPES ####################
    # These dicts look up agent info based on the resource or goods that the agent produces
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
                         'flax clothing':{'name':'Flax Clothier', 'finished_goods':'flax clothing', 'consumed':[], 'essential':['tools'], 'preferred':[] },
                         'iron sword':{'name':'Iron Weaponsmith', 'finished_goods':'iron sword', 'consumed':['woods'], 'essential':['tools'], 'preferred':['clothing'] },
                         'copper sword':{'name':'Copper Weaponsmith', 'finished_goods':'copper sword', 'consumed':['woods'], 'essential':['tools'], 'preferred':['clothing'] },
                         }
                         
    merchants_by_token = {'merchant':{'consumed':[], 'essential':[], 'preferred':[]}  }
                         
    CITY_RESOURCE_SLOTS = {'foods':6, 'cloths':6, 'clays':6, 'ores':4, 'woods':4}                     
    CITY_INDUSTRY_SLOTS = {'tools':3, 'clothing':5, 'pottery':5, 'furniture':3}

        
        
def economy_test_run():
    native_resources = [resource.name for resource in RESOURCES]
    print native_resources
    print [resource.name for resource in GOODS]
    economy = Economy(native_resources, local_taxes=5, owner=None) 
    
    for i in xrange(6):
        for resource in RESOURCES: #raw resources
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
            if good.name == 'flax clothing': #produced resource.
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
        
        
class TempCity(object):
    def __init__(self):
        self.name = "Fulwood"
        self.treasury = 10000
        self.warehouse = {}
        
        
class TradeHouse:
    def __init__(self, parent):
        
        self.parent = parent
        
        self.caravans_in = []
        self.caravans_out = []
        self.trades = {"asks": {}, "buys": {}, "desires": {}} # self.trades["asks"]["cloth"] is then an array.
        self.supply_demand = {}
        self.successful_trades = {}
        for resource in R.resource_list:
            self.trades["asks"][resource] = []
            self.trades["buys"][resource] = []
            self.trades["desires"][resource] = []
            self.supply_demand[resource] = []
            self.successful_trades[resource] = []
        self.jobs = {"buys":[], "asks":[] }
        
    def collect_info(self, commodity = "none"):

        demand, demand_cost = self.findAverages("buys", commodity)
        supply, supply_cost = self.findAverages("asks", commodity)
        
        supply_avg, demand_avg = 0.0,0.0
        
        if demand != 0 and demand_cost != 0:
            demand_avg = round(demand_cost / demand,2)
        if supply != 0 and supply_cost != 0:
            supply_avg = round(supply_cost / supply,2)
            
            
        if demand == 0 and supply != 0:
            modifier = -(supply / 10)
            
        elif supply == 0 and demand != 0:
            modifier = demand / 10
            
        elif supply == 0 and demand == 0:
            modifier = 0.0
            
        else:
            modifier = (demand / supply)
        
        modifier = round(modifier,2)    
        self.supply_demand[commodity] = [modifier, demand, supply, demand_avg, supply_avg]
        
        
    def findAverages(self,transaction_type,commodity):
        amount = 0.0
        amount_cost = 0.0
        
        for offer in self.trades[transaction_type][commodity]:
            amount += offer.quantity;
            amount_cost += (offer.quantity * offer.price);
        
        return amount, amount_cost
        #print "%.2f" % a

    def create_offer(self,bid=False, time=5, offer_price=1, commodity="none"):
        if bid:
            #make a bid offer.
            #offer = Offer(self.parent,bid,offer_price,commodity,quantity, resources = []):
            pass
        else:
            #make a ask offer.
            pass

    def resolve_offers(self, commodity):
        buys = self.trades["buys"][commodity]
        asks = self.trades["asks"][commodity]
        
        buys = sorted(buys, key=lambda offer: offer.price)
        asks = sorted(asks, key=lambda offer: offer.price, reverse=True)
        
        while len(buys) > 0 and len(asks) > 0:
            buyer = buys[0]
            seller = asks[0]
            
            quantity_traded = min(buyer.quantity, seller.quantity)
            clearing_price = (buyer.price + seller.price) / 2
            clearing_price = round(clearing_price, 2)
            
            if quantity_traded > 0:
                seller.quantity -= quantity_traded
                buyer.quantity -= quantity_traded
                #seller.owner.sell(seller, quantity_traded, clearing_price)
                buyer.owner.buy(seller, quantity_traded, clearing_price) #pay in here?
                seller.owner.accepted_offer(commodity, clearing_price, quantity_traded)
                buyer.owner.accepted_offer(commodity, clearing_price, quantity_traded)
                
                self.successful_trades[commodity].append([quantity_traded, clearing_price])
                
            if seller.quantity <= 0:
                #asks.remove(seller)
                seller.owner.sold_out(seller, True)
                
            if buyer.quantity <= 0:
                #buys.remove(buyer)
                buyer.owner.sold_out(buyer, False)
    

    
    
    def resolve_offers_city(self, commodity, city):
        buys = self.trades["buys"][commodity] #passing these like this means the root list does not change. 
        asks = city.trade_house.trades["asks"][commodity]
        
        self.trades["buys"][commodity] = sorted(self.trades["buys"][commodity], key=lambda offer: offer.price, reverse=True)
        city.trade_house.trades["asks"][commodity] = sorted(city.trade_house.trades["asks"][commodity], key=lambda offer: offer.price)
        total_traded = 0
        while len(self.trades["buys"][commodity]) > 0 and len(city.trade_house.trades["asks"][commodity]) > 0:
            buyer = self.trades["buys"][commodity][0] #buy offer
            seller = city.trade_house.trades["asks"][commodity][0] #sell ofeer
            
            quantity_traded = min(buyer.quantity, seller.quantity)
            clearing_price = (buyer.price + seller.price) / 2
            clearing_price = round(clearing_price, 2)
            
            if quantity_traded > 0:
                #seller.owner.sell(seller, quantity_traded, clearing_price)
                buyer.owner.buy(buyer, seller, quantity_traded, clearing_price) #pay in here?
                seller.owner.accepted_offer(commodity, clearing_price, quantity_traded)
                buyer.owner.accepted_offer(commodity, clearing_price, quantity_traded)
                
                self.successful_trades[commodity].append([quantity_traded, clearing_price])
                
            if seller.quantity <= 0:
                seller.owner.trades["asks"][commodity].remove(seller) #removes from trader. 
                city.trade_house.trades["asks"][commodity].remove(seller) #removes from trade-house
                #seller.sold_out(self)
                
            if buyer.quantity <= 0:
                buyer.owner.trades["buys"][commodity].remove(buyer)
                self.trades["buys"][commodity].remove(buyer)
            
            self.check_for_time_out(city.trade_house.trades["asks"][commodity],self.trades["buys"][commodity],self,city)
            
            total_traded += quantity_traded
            seller = None
            buyer = None
        
        print self.parent.name, ": the total ", commodity, " traded with", city.name, "was: ", total_traded
#         if commodity == "raw":
#             if len(self.caravans_in) > 0:
#                 merchant = self.caravans_in[0]
#                 
#             else:
#                 merchant = entities.Object(x=self.parent.x, y=self.parent.y, char=libtcod.CHAR_POUND, name="merchant", colour=libtcod.orange, blocks=False, always_visible=False,
#                                            pather=entities.Pather(), ai=entities.cityTrader(self))
#             self.give_trade_mission(merchant.ai,city)
#             self.caravans_in.append(merchant)
#             self.caravans_out.append(merchant)
        

    def check_for_time_out(self, asks, buys, city = None, other_city = None):
        for i in range(len(asks)):
            asks[i].time -= 1
            
        for i in range(len(buys)):
            buys[i].time -= 1
        removables = []   
        for i in range(len(asks)):
            if asks[i].time <= 0:
                offer = asks[i]
                removables.append(offer)
                offer.owner.trades["asks"][offer.commodity].remove(offer)
                offer.time_out()
        
        for offers in removables:
            asks.remove(offers)
                
        removables = []
        for i in range(len(buys)):
            if buys[i].time <= 0:
                offer = buys[i]
                removables.append(offer)
                offer.owner.trades["buys"][offer.commodity].remove(offer)
                offer.time_out()
                
        for offers in removables:
            buys.remove(offers)
                
    def give_trade_mission(self, trader, city):
        
        trader.goal_city = city
        trader.trading_for = 5
        #TODO
       
class Offer:
    def __init__(self,owner,commodity="raw",price=1, quantity=1, time=5):
#         if bid:
#             self.bid = True
#             self.ask = False
#         else:
#             self.ask = True
#             self.bid = False
        
        self.owner = owner
        self.commodity = commodity
        self.price = price
        if quantity < 0:
            quantity = 1 #TODO: find out why this can be negative. - probably th emodifier
        self.quantity = quantity
        self.time = time
        #self.resources = resources
        
    def time_out(self):
        self.owner.rejected_offer(self.commodity,self.price,self.quantity)
                
       
class Resource(object):
    
    def __init__(self, name="", category="", resource_class="", gather_amount=0, break_chance=0, app_chances=0, app_amt=0, type = "none",quantity = 0.0):
        self.name = name
        self.category = category
        self.resource_class = resource_class
        self.gather_amount = gather_amount
        self.break_chance = break_chance
        self.app_chances = app_chances
        self.app_amt = app_amt
        
        self.type = type
        self.quantity = quantity
        self.bought_for = 0.0 
        self.supplyDemand = 0.0
        self.raw_materials = [] 
        self.raw_costs = 0.0 #how much it cost to make   
        
        
class Cargo(Resource):
    def __init__(self, type="none", quantity=0.0):
                 
        self.type = type
        self.quantity = quantity
        self.bought_for = 0.0 
        self.supplyDemand = 0.0
        self.raw_materials = [] 
        self.raw_costs = 0.0 #how much it cost to make   
        
    def buy(self,price):
        self.bought_for = price # stored as a per 1 quantity.
        
    
    def splitStack(self,quantity):
            '''
            quantity is what's needed for NEW stack. returns the new resource.
            '''
            resource = Resource(self.name,0);
            
            if self.quantity > quantity:
                self.quantity -= quantity
                resource.quantity = quantity
                resource.rawMatsCost = self.raw_costs
                resource.boughtFor = self.bought_for
                return resource
            
            return None
        
class FinishedGood(object):
    def __init__(self, category, material, in_amt, out_amt, name = ""):
        # Type, i.e. tools
        self.category = category
        # The resource type that makes this specific good
        self.material = material
        self.break_chance = self.material.break_chance
        
        self.name = name
        if self.name == "":
            self.name = self.material.name + " " + self.category
        
        # How many of the input materials produce how many of this good
        self.in_amt = in_amt
        self.out_amt = out_amt    
        
            
class Agent(object):
    #base class for members of the economy.
    def pay_taxes(self):
        if self.economy != None:
            self.gold -= self.economy.local_taxes
            if self.economy.owner:
                self.economy.owner.treasury += self.economy.local_taxes
    
    def has_token(self, type_of_item):
        # Test whether or not we have a token of an item
        for token_of_item in COMMODITY_TYPES[type_of_item]:
            if token_of_item.name in self.inventory:
                return True
        return False
    
    def check_for_needed_items(self):
        # Make a list of items we need to produce items
        critical_items = [type_of_item for type_of_item in self.consumed + self.essential if not self.has_token(type_of_item)]
        other_items = [type_of_item for type_of_item in self.preferred if not self.has_token(type_of_item)]
        return critical_items, other_items         
         
    def place_bid(self, token_to_bid):
        price_est = self.perceived_values[token_to_bid].center
        uncertainty = self.perceived_values[token_to_bid].uncertainty
        bid_price = roll(price_est - uncertainty, price_est + uncertainty)
        
        if bid_price > self.gold:
            bid_price = self.gold
        
        quantity = roll(1,2)
        
        self.last_turn.append("Bid on " + str(quantity) + " " + token_to_bid + " for " + str(bid_price))
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
    
    def eval_sell_rejected(self, type_of_item):
        # What to do when we put something up for sale and nobody bought it. Only adjust if there was a demand
        if self.economy.auctions[type_of_item].demand: 
            production_cost = self.check_production_cost()
            min_sale_price = int(round((production_cost/self.in_amt)*PROFIT_MARGIN))
            
            #self.perceived_values[type_of_item].center = max(self.perceived_values[type_of_item].center - ASK_REJECTED_ADJUSTMENT, min_sale_price + self.perceived_values[type_of_item].uncertainty)
            self.perceived_values[type_of_item].center = self.perceived_values[type_of_item].center - ASK_REJECTED_ADJUSTMENT
            self.perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT
    
class Resource_Gatherer(Agent):
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
            if self.inventory.count('food') < FOOD_BID_THRESH:
                self.place_bid(token_to_bid=random.choice(self.economy.available_types['foods']))
                
    def starve(self):
        R.ui.message( self.name + " has starved!",libtcod.dark_sea, R.date)   
        self.economy.resource_gatherers.remove(self)
        if self.economy.owner: self.economy.owner.former_agents.append(self)      
    
            
    def eval_need(self):
        critical_items, other_items = self.check_for_needed_items()
        for type_of_item in critical_items + other_items:
            # For now, place a bid for a random item available to use of that type
            token_of_item = random.choice(self.economy.available_types[type_of_item])
            self.place_bid(token_to_bid=token_of_item)  
                  
    def check_production_ability(self):
        # Check whether we have the right items to gather resources
        critical_items, other_items = self.check_for_needed_items()
        if critical_items == []:
            self.gather_resources()  
        #else:
            #check for bids for each item, and if not already buying, put out a bid.
            #else ignore.      
#     def check_for_needed_items(self):
#         # Make a list of items we need to gather resources
#         critical_items = [type_of_item for type_of_item in self.consumed + self.essential if not self.has_token(type_of_item)]
#         other_items = [type_of_item for type_of_item in self.preferred if not self.has_token(type_of_item)]
#         return critical_items, other_items
    
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
    
    def gather_resources(self):
        # Gather resources, consume items, and account for breaking stuff
        amount = max(self.inventory_size - len(self.inventory), 0)
        if amount > 0:
            # Add the resource to our own inventory. The government takes half our production for now
            for i in xrange(min(int(self.gather_amount/2), amount)):
                self.inventory.append(self.resource)
            ## Add it to the warehouse, and track how much we have contributed to it this turn    
            if self.economy.owner:
                self.economy.owner.warehouse[self.resource].add(self.resource, int(self.gather_amount/2))
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
    def eval_sell_rejected(self, type_of_item):
        if self.economy.auctions[type_of_item].demand:
            production_cost = self.check_production_cost()
            min_sale_price = int(round((production_cost/self.gather_amount)*PROFIT_MARGIN))
            
            self.perceived_values[type_of_item].center = max(self.perceived_values[type_of_item].center - ASK_REJECTED_ADJUSTMENT, min_sale_price + self.perceived_values[type_of_item].uncertainty)
            #self.perceived_values[type_of_item].center = self.perceived_values[type_of_item].center - ASK_REJECTED_ADJUSTMENT
            self.perceived_values[type_of_item].uncertainty += REJECTED_UNCERTAINTY_AMOUNT
              
class Goods_Producer(Agent):
    
    def __init__(self, name, economy, finished_goods, consumed, essential, preferred):
        self.name = name
        self.economy = economy
        self.finished_goods = finished_goods
        self.consumed = consumed
        self.essential = essential
        self.preferred = preferred
        
        self.in_amt = finished_goods.in_amt
        self.out_amt = finished_goods.out_amt
        
        self.input = finished_goods.material.name
        self.output = finished_goods.name
        
        self.turns_since_food = 0
        self.turns_alive = 0
        self.buys = 0
        self.sells = 0
        
        self.last_turn = []
        
        self.gold = 1000
        self.inventory = ['food', 'food', 'food', self.input, self.input, finished_goods.name, finished_goods.name]
        self.inventory_size = 20
        
        self.perceived_values = {finished_goods.name:Value(START_VAL, START_UNCERT), self.input:Value(START_VAL, START_UNCERT)}
        for type_of_item in consumed + essential + preferred:
            for token_of_item in COMMODITY_TYPES[type_of_item]:
                self.perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)
            for token_of_item in COMMODITY_TYPES['foods']:
                self.perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)        
                
            for i in xrange(1):
                self.inventory.append(token_of_item.name)
                
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
        if self.inventory.count('food') < FOOD_BID_THRESH:
            self.place_bid(token_to_bid=random.choice(self.economy.available_types['foods']))
            
    def starve(self):
        R.ui.message( self.name + " has starved!",libtcod.dark_han, R.date)   
        self.economy.goods_producers.remove(self)
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
        
    def eval_need(self):
        critical_items, other_items = self.check_for_needed_items()

        for type_of_item in critical_items + other_items:
            # For now, place a bid for a random item available to use of that type
            token_of_item = random.choice(self.economy.available_types[type_of_item])
            self.place_bid(token_to_bid=token_of_item)    
        
        if self.inventory.count(self.input) <= self.in_amt*2:
            self.place_bid(token_to_bid=self.input)
         
                 
class Merchant(object):
    def __init__(self, name, home_economy, traded_item, consumed, essential, preferred, attached):
        self.turns_alive = 0
        self.buys = 0
        self.sells = 0
        
        self.gold = 10000
        self.inventory = ["food","food"]
        
        self.last_turn = []
        
        self.current_location = home_economy
        self.time_here = roll(1, 3)
        self.cycle_length = 4
        
        self.buy_perceived_values = {traded_item:Value(START_VAL, START_UNCERT)} 
        self.sell_perceived_values = {traded_item:Value(START_VAL*2, START_UNCERT)}
        
        for type_of_item in consumed + essential + preferred:
            for token_of_item in COMMODITY_TYPES[type_of_item]:
                if token_of_item != traded_item:
                    self.buy_perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)
                    self.sell_perceived_values[token_of_item.name] = Value(START_VAL-1, START_UNCERT+1)
            self.append(token_of_item.name)
        for token_of_item in COMMODITY_TYPES["food"]:
            if token_of_item != traded_item:
                self.buy_perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)
                self.sell_perceived_values[token_of_item.name] = Value(START_VAL, START_UNCERT)  
    
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
        if self.inventory.count('food') < FOOD_BID_THRESH:
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
        # Pay taxes. If the economy has an owner, pay the taxes to that treasury
        self.gold -= economy.local_taxes
        # economy owner - should be the city
        if economy.owner:
            economy.owner.treasury += economy.local_taxes
        
    def has_token(self, type_of_item):
        # Test whether or not we have a token of an item
        for token_of_item in COMMODITY_TYPES[type_of_item]:
            if token_of_item.name in self.inventory:
                return True
        return False
        
    def place_bid(self, economy, token_to_bid):
        ## Place a bid in the economy
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
    return libtcod.random_get_int(0,a,b)
       
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



class Economy(object): 
    def __init__(self, native_resources, local_taxes, owner=None):
        self.native_resources = native_resources
        self.available_types = {}
        # Should be the city where this economy is located
        self.owner = owner
        #if self.owner == None:
        #     self.owner = TempCity()
        
        # Agents belonging to this economy
        self.resource_gatherers = []
        self.goods_producers = []
        self.buy_merchants = []
        self.sell_merchants = []
        
        self.starving_agents = []
        # Auctions that take place in this economy
        self.auctions = {}
        self.prices = {}
        
        # Amount of gold paid in taxes each turn
        self.local_taxes = local_taxes
    
    def add_commodity_to_economy(self, commodity):
        #sets up the auctions and avilable for trade in the economy.
        category = COMMODITY_TOKENS[commodity].category
        if category in self.available_types.keys():
            if commodity not in self.available_types[category]:
                self.available_types[category].append(commodity)
                self.auctions[commodity] = Auction(commodity)
        else:
            self.available_types[category] = [commodity]
            self.auctions[commodity] = Auction(commodity)
            
    def add_resource_gatherer(self, resource):
        info = gatherers_by_token[resource]
        gatherer = Resource_Gatherer(name=info['name'], economy=self, resource=resource, gather_amount=COMMODITY_TOKENS[resource].gather_amount, consumed=info['consumed'], essential=info['essential'], preferred=info['preferred'] )
        self.resource_gatherers.append(gatherer)
        # Test if it's in the economy and add it if not
        self.add_commodity_to_economy(resource)
        
    def add_goods_producer(self, goods):
        info = producers_by_token[goods]
        producer = Goods_Producer(name=info['name'], economy=self, finished_goods=COMMODITY_TOKENS[goods], consumed=info['consumed'], essential=info['essential'], preferred=info['preferred'] )
        self.goods_producers.append(producer)
        # Test if it's in the economy and add it if not
        self.add_commodity_to_economy(goods)
    
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
        for agent in self.goods_producers:
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
        
        for gatherer in self.resource_gatherers[:]:
            gatherer.take_turn()
        
        for producer in self.goods_producers[:]:
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
                
        for commodity, auction in self.auctions.iteritems():
            auction.iterations += 1
            
            auction.bids = sorted(auction.bids, key=lambda attr: attr.price, reverse=True)
            ## Sort the sells by price (lowest to hghest) ##
            auction.sells = sorted(auction.sells, key=lambda attr: attr.price)
            
            self.prices[commodity] = []    
            
            num_bids = len(auction.bids)
            num_sells = len(auction.sells)
            
            if num_bids > 0 or num_sells > 0 :
                auction.supply = sum(offer.quantity for offer in auction.sells)
                auction.demand = sum(offer.quantity for offer in auction.bids)
                
            while not len(auction.bids) == 0 and not len(auction.sells) == 0:
                buyer = auction.bids[0]
                seller = auction.sells[0]
                
                ## Allow the buyer to make some radical readjustments the first few turns it's alive
                if buyer.price < seller.price and (buyer.owner.turns_alive < 10 or seller.owner.turns_alive < 10):
                    buyer.price = int(round(seller.price*1.5))
                    buyer.owner.eval_bid_rejected(commodity,int(round(seller.price *1.5)))
                    
                ## If the price is still lower than the seller
                if buyer.price < seller.price:
                    buyer.owner.eval_bid_rejected(commodity, seller.price)
                    buyer.quantity = 0                
                
                else:     
                    #decide privce amount
                    quantity = min(buyer.quantity, seller.quantity)
                    price = int(round(buyer.price + seller.price)/2) #this is where powers of persuasion could come into play.
                    
                    buyer.owner.eval_trade_accepted(buyer.commodity, price)
                    seller.owner.eval_trade_accepted(seller.commodity, price)
                    
                    #updating the inventories and wealth
                    for i in xrange(quantity):
                        buyer.owner.inventory.append(buyer.commodity)
                        buyer.quantity -= 1
                        seller.owner.inventory.append(seller.commodity)
                        seller.quantity -= 1
                    
                    buyer.owner.gold -= (price*quantity)
                    seller.owner.gold += (price * quantity)
                    
                    buyer.owner.buys += quantity
                    buyer.owner.last_turn.append('Bought ' + str(quantity) + ' ' + commodity + ' from ' + seller.owner.name + ' at ' + str(price))
                    seller.owner.sells += quantity
                    seller.owner.last_turn.append('Sold ' + str(quantity) + ' ' + commodity + ' to ' + buyer.owner.name + ' at ' + str(price))
                    
                    self.prices[commodity].append(price)   
                if seller.quantity == 0: del auction.sells[0]
                if buyer.quantity == 0: del auction.bids[0]
        
            #re-evaluate prices. For some reason?
            if len(auction.bids) > 0:
                for buyer in auction.bids:
                    buyer.owner.eval_bid_rejected(buyer.commodity)
                self.auctions[commodity].bids = []
            
            # All sellers re-evaluate prices - too simplistic as well
            elif len(auction.sells) > 0:
                for seller in auction.sells:    
                    seller.owner.eval_sell_rejected(seller.commodity)    
                self.auctions[commodity].sells = []
                
            #Average prices
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
#         for merchant in self.buy_merchants + self.sell_merchants:
#             if merchant.current_location == self:
#                 merchant.increment_cycle()
        ## Add some information to the city's food supply/demand
        if self.owner:        
            del self.owner.food_supply[0]
            del self.owner.food_demand[0]
            self.owner.food_supply.append(self.auctions['food'].supply)
            self.owner.food_demand.append(self.auctions['food'].demand)

class City_Economy(object): 
    def __init__(self, native_resources, local_taxes, owner=None):
        self.native_resources = native_resources
        self.available_types = {}
        # Should be the city where this economy is located
        self.owner = owner
        #if self.owner == None:
        #     self.owner = TempCity()
        
        # Agents belonging to this economy
        self.resource_gatherers = []
        self.goods_producers = []
        self.buy_merchants = []
        self.sell_merchants = []
        
        self.starving_agents = []
        # Auctions that take place in this economy
        self.auctions = {}
        self.prices = {}
        
        # Amount of gold paid in taxes each turn
        self.local_taxes = local_taxes
    
    def add_commodity_to_economy(self, commodity):
        #sets up the auctions and avilable for trade in the economy.
        category = COMMODITY_TOKENS[commodity].category
        if category in self.available_types.keys():
            if commodity not in self.available_types[category]:
                self.available_types[category].append(commodity)
                self.auctions[commodity] = Auction(commodity)
        else:
            self.available_types[category] = [commodity]
            self.auctions[commodity] = Auction(commodity)
            
    def add_resource_gatherer(self, resource):
        info = gatherers_by_token[resource]
        gatherer = Resource_Gatherer(name=info['name'], economy=self, resource=resource, gather_amount=COMMODITY_TOKENS[resource].gather_amount, consumed=info['consumed'], essential=info['essential'], preferred=info['preferred'] )
        self.resource_gatherers.append(gatherer)
        # Test if it's in the economy and add it if not
        self.add_commodity_to_economy(resource)
        
    def add_goods_producer(self, goods):
        info = producers_by_token[goods]
        producer = Goods_Producer(name=info['name'], economy=self, finished_goods=COMMODITY_TOKENS[goods], consumed=info['consumed'], essential=info['essential'], preferred=info['preferred'] )
        self.goods_producers.append(producer)
        # Test if it's in the economy and add it if not
        self.add_commodity_to_economy(goods)
    
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
        for agent in self.goods_producers:
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
        
        for gatherer in self.resource_gatherers[:]:
            gatherer.take_turn()
        
        for producer in self.goods_producers[:]:
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
                
        for commodity, auction in self.auctions.iteritems():
            auction.iterations += 1
            
            auction.bids = sorted(auction.bids, key=lambda attr: attr.price, reverse=True)
            ## Sort the sells by price (lowest to hghest) ##
            auction.sells = sorted(auction.sells, key=lambda attr: attr.price)
            
            self.prices[commodity] = []    
            
            num_bids = len(auction.bids)
            num_sells = len(auction.sells)
            
            if num_bids > 0 or num_sells > 0 :
                auction.supply = sum(offer.quantity for offer in auction.sells)
                auction.demand = sum(offer.quantity for offer in auction.bids)
                
            while not len(auction.bids) == 0 and not len(auction.sells) == 0:
                buyer = auction.bids[0]
                seller = auction.sells[0]
                
                ## Allow the buyer to make some radical readjustments the first few turns it's alive
                if buyer.price < seller.price and (buyer.owner.turns_alive < 10 or seller.owner.turns_alive < 10):
                    buyer.price = int(round(seller.price*1.5))
                    buyer.owner.eval_bid_rejected(commodity,int(round(seller.price *1.5)))
                    
                ## If the price is still lower than the seller
                if buyer.price < seller.price:
                    buyer.owner.eval_bid_rejected(commodity, seller.price)
                    buyer.quantity = 0                
                
                else:     
                    #decide privce amount
                    quantity = min(buyer.quantity, seller.quantity)
                    price = int(round(buyer.price + seller.price)/2) #this is where powers of persuasion could come into play.
                    
                    buyer.owner.eval_trade_accepted(buyer.commodity, price)
                    seller.owner.eval_trade_accepted(seller.commodity, price)
                    
                    #updating the inventories and wealth
                    for i in xrange(quantity):
                        buyer.owner.inventory.append(buyer.commodity)
                        buyer.quantity -= 1
                        seller.owner.inventory.append(seller.commodity)
                        seller.quantity -= 1
                    
                    buyer.owner.gold -= (price*quantity)
                    seller.owner.gold += (price * quantity)
                    
                    buyer.owner.buys += quantity
                    buyer.owner.last_turn.append('Bought ' + str(quantity) + ' ' + commodity + ' from ' + seller.owner.name + ' at ' + str(price))
                    seller.owner.sells += quantity
                    seller.owner.last_turn.append('Sold ' + str(quantity) + ' ' + commodity + ' to ' + buyer.owner.name + ' at ' + str(price))
                    
                    self.prices[commodity].append(price)   
                if seller.quantity == 0: del auction.sells[0]
                if buyer.quantity == 0: del auction.bids[0]
        
            #re-evaluate prices. For some reason?
            if len(auction.bids) > 0:
                for buyer in auction.bids:
                    buyer.owner.eval_bid_rejected(buyer.commodity)
                self.auctions[commodity].bids = []
            
            # All sellers re-evaluate prices - too simplistic as well
            elif len(auction.sells) > 0:
                for seller in auction.sells:    
                    seller.owner.eval_sell_rejected(seller.commodity)    
                self.auctions[commodity].sells = []
                
            #Average prices
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
#         for merchant in self.buy_merchants + self.sell_merchants:
#             if merchant.current_location == self:
#                 merchant.increment_cycle()
        ## Add some information to the city's food supply/demand
        if self.owner:        
            del self.owner.food_supply[0]
            del self.owner.food_demand[0]
            self.owner.food_supply.append(self.auctions['food'].supply)
            self.owner.food_demand.append(self.auctions['food'].demand)
        
def main():
    setup_resources()
    economy_test_run()
    
def setup_city_economy():
    pass
   
# main()     