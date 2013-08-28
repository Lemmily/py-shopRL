'''
Created on 16 Mar 2013

@author: Emily
'''
import libtcodpy as libtcod
import R
import math
import city
import economy
from R import cities
from random import choice

STRAIGHT = 5
DIAG = math.sqrt(2*STRAIGHT)*STRAIGHT

GRASS = 15
MOUNTAIN = 40
PATH = 5


MOTIVATIONS = ["none", "health", "wealth", "buy", "sell", "adventure", "comfort"] 


class Object:
    
    def __init__(self, x=0, y=0, char="@", name="blob", colour=libtcod.white, blocks=False, always_visible=False,
                    item=None):
        
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.type = "object"
        self.colour = colour
        self.blocks = blocks
        self.always_visible = always_visible
        
        
        self.item = item
        if item:
            self.item.parent = self

    
    def _set_x(self,x):
        self.x = x
    def _set_y(self,y):
        self.y = y
    def _get_x(self):
        return self.x
    def _get_y(self):
        return self.y
        
    def clear(self, cam_x = 0, cam_y =0): 
        #erase the character that represents this object
        libtcod.console_put_char(R.con_char, self.x -cam_x, self.y- cam_y, " ", libtcod.BKGND_NONE)
        #libtcod.console_set_default_foreground(con, color_light_ground)
        #libtcod.console_put_char(con, x, y, libtcod.CHAR_BLOCK2, libtcod.black)
        
    def draw_faded(self, cam_x, cam_y): 
        pos_x = self.x - cam_x
        pos_y = self.y - cam_y
        
        colour = libtcod.Color(self.colour.r,self.colour.g,self.colour.b)
        libtcod.color_scale_HSV(colour, 0.7, 0.7) #hopefully 80% saturation.
        libtcod.console_set_default_foreground(R.con_char, colour)
        libtcod.console_put_char(R.con_char, pos_x, pos_y, self.char, libtcod.BKGND_NONE)#ADDALPHA(0.0))
#             
    def draw(self, cam_x, cam_y): 
        
        if self.x >= cam_x and self.x < cam_x + R.MAP_VIEW_WIDTH and self.y >= cam_y and self.y < cam_y + R.MAP_VIEW_HEIGHT:
            
            pos_x = self.x - cam_x
            pos_y = self.y - cam_y
            
            libtcod.console_set_default_foreground(R.con_char, self.colour)
            #libtcod.console_set_default_background(R.con_char, libtcod.white)
            libtcod.console_put_char(R.con_char, pos_x, pos_y, self.char, libtcod.BKGND_NONE)#ADDALPHA(0.0))
#            if (libtcod.map_is_in_fov(R.fov_map, self.x, self.y) or
#                (self.always_visible and R.world.tiles[self.x][self.y].explored)):
#                #set the color and then draw the character that represents this object at its position
#                libtcod.console_set_default_foreground(R.con_char, self.colour)
#                libtcod.console_set_default_background(R.con_char, libtcod.white)
#                libtcod.console_put_char(R.con_char, pos_x, pos_y, self.char, libtcod.BKGND_NONE)#ADDALPHA(0.0))


#    def move(self, dx, dy):
#        #move by the given quantity, if the destination is not blocked
#        if not is_blocked(self.x + dx, self.y + dy):
#            self.x += dx
#            self.y += dy
#            return True
#        return False
#     
#    def move_p(self, dx, dy):
#        #move by the given quantity
#        self.x += dx
#        self.y += dy
#       
#    def move_towards(self, target_x, target_y):
#        #vector from this object to the other and the distance
#        dx = target_x - self.x
#        dy = target_y - self.y
#        distance = math.sqrt(dx ** 2 + dy ** 2)
#
#        dx = int(round(dx / distance))
#        dy = int(round(dy / distance))
#        self.move(dx, dy)
#
#    def distance(self, x, y):
#        #return the distance to some coordinates
#        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
#
#    def distance_to(self, other):
#        dx = other.x - self.x
#        dy = other.y - self.y
#        return math.sqrt(dx ** 2 + dy ** 2)


class Mover(Object):
    def __init__(self, x=0, y=0, char="@", name="blob", colour=libtcod.white, blocks=False, always_visible=False,
                        fighter=None, you=None, pather=None, ai=None):
        Object.__init__(self, x, y, char, name, colour, blocks, always_visible)
        self.direction = "S"
        
        self.activity_log = {"history": [], "kills": [], "travels": [], "transactions":[]}
        
        self.fighter = fighter
        if fighter:
            self.fighter.parent = self

        
        self.you = you
        if you:
            self.you.parent = self
            
        #THIS HAS BEEN MOVED INTO AI. AS thIS IS WHERE IT WILL BE USED.
        self.pather = pather
        if pather:
            self.pather.parent = self
         
        self.ai = ai   
        if ai:
            self.ai.parent = self
        

    def move(self, dx, dy):
        #move by the given quantity, if the destination is not blocked
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            return True
        return False
     
    def move_p(self, dx, dy):
        #move by the given quantity
        self.x += dx
        self.y += dy
       
    def move_towards(self, target_x, target_y):
        #vector from this object to the other and the distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance(self, x, y):
        #return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    


class Player:
    
    def __init__(self, d_l = 0):
        self.dungeon_level = d_l
        

def is_blocked(x, y):
    #first test the map tile
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

class Item():
    def __init__(self, use_function = None):
        self.use_function = use_function
        self.parent = None

class Hero():
    def __init__(self):
        self.dungeon_level = 0
        self.inventory = [] #stuff being carried
        self.equipment = [] #attempts to have one armour one weapon one clothing. (to start with)
    
    #unsure as to what needs to go here.
        
class Trader:
    def __init__(self, wealth = 1000):
        self.wealth = wealth
        self.believed_prices = {}
        self.resources = {}
        self.trades = {"asks": {}, "buys": {}} # self.trades["asks"]["cloth"] is then an array.
        
        for resource in R.resource_list:
            #self.believed_prices[resource] = [35.00,10.00] #name as key. then [believed price, deviance]
            self.resources[resource] = [resource, 10.00] #resource as key, then the name and the quantity.
            
        for resource in R.resource_list:
            self.trades["asks"][resource] = []
            self.trades["buys"][resource] = []
    
    def buy(self, offer, seller,quantity,price):
        seller.quantity -= quantity 
        offer.quantity -= quantity
        
        seller.owner.resources[offer.commodity][1] -= quantity
        self.resources[offer.commodity][1] += quantity
        
        self.wealth -= round(quantity * price, 2)
        seller.owner.wealth += round(quantity * price, 2)
    
    def accepted_offer(self,commodity,price,quantity):  
        
        believed = self.believed_prices[commodity][0]
        deviance = self.believed_prices[commodity][1]
        change = 0.0
        if price > believed:
            change = price - believed
            change = (change * 0.1) * quantity
            believed += change
        elif price < believed:
            change = believed - price
            change = (change * 0.1) * quantity
            believed -= change
            
        deviance -= (deviance *0.1)
        self.believed_prices[commodity][0] = round(believed, 2)   
        self.believed_prices[commodity][0] = round(deviance, 2)  

    def rejected_offer(self,commodity,price,quantity, ):  
        believed = self.believed_prices[commodity][0]
        deviance = self.believed_prices[commodity][1]
        #change = 0.0
#         if bid:
#             believed += (believed * 0.1) * quantity
#             
#         else:
        believed -= (believed *0.02) * quantity
        deviance += deviance *0.05
        self.resources[commodity][1] += quantity #TODO: here would just be pushing the resource object back into the array.
            
        deviance += (deviance *0.1)
        self.believed_prices[commodity][0] = round(believed, 2)   
        self.believed_prices[commodity][0] = round(deviance,2)  
            
         
    def place_bid(self,trade_house,commodity,quantity,offerprice,time=5):
        #trade_house
        offer = economy.Offer(self,price=offerprice,commodity=commodity,quantity=quantity)#, time=time)
        self.trades["buys"][commodity].append(offer)
        trade_house.trades["buys"][commodity].append(offer)
        

    def place_ask(self,trade_house,commodity,quantity,price,time=5):
        
        if price < 0:
            print "uh-oh a minus."
        offer = economy.Offer(self,price=price,commodity=commodity,quantity=quantity) #time=time)
        self.trades["asks"][commodity].append(offer)
        trade_house.trades["asks"][commodity].append(offer)
    
    def get_quantity(self, commodity, actual, total_needed, trade_house):
        
        modifier = trade_house.supply_demand[commodity][0]
        quantity = 0.0
        if actual < total_needed + total_needed*0.1 and actual > total_needed:
            quantity = round(total_needed*0.25,2) 
        elif actual < total_needed:
            if actual < total_needed *0.25:
                quantity =  round(total_needed*1.5, 2)
                #put a bid for a large quantity
            elif actual < total_needed *0.5:
                quantity =  round(total_needed*1.25,2)
                #put a bid in for a good quantity
            else:
                quantity =  round(total_needed,2)
                #put a bid for a normal quantity.
        if modifier != 0.0:
            quantity = quantity * modifier
        
        return quantity
    
    def get_price(self, commodity, trade_house):
        believed = self.believed_prices[commodity][0]
        deviance = self.believed_prices[commodity][1]
        
        price = round(libtcod.random_get_float(0, believed-deviance, believed+deviance),2)
        
#        modifier = trade_house.supply_demand[commodity][0]
#        if modifier != 0.0:
#            price = price
        if price < 0:
            print "uh-oh price of %s in %s is less than 0" % (commodity, trade_house.parent.name)
            price = believed # for now.
            #TODO: temporary until I can work out a better way to get a price.
        return price

    
    def check_for_offer(self, bid, commodity, limit, actual, quantity, price):
        '''
        bid - is this a buy offer
        limit     - for a bid this is used to know how much at least they need to BUY
                  -for a sale this is used to know how much at most they can sell.
        actual - the quantity of resource the entity ACTUALLY has right now.
        price - the quantity the entity is willing to make a new bid/ask for.
        '''
        if bid:
            if len(self.trades["buys"][commodity]) == 0:
                return 0
            else: #tally up how much trying to buy.
                total = 0.0
                total_price = 0.0
                for offer in self.trades["buys"][commodity]:
                    total += offer.quantity
                    total_price += offer.price
                    
                avg_price = total_price / len(self.trades["buys"][commodity])
                
#                if total < limit:
#                    #PLACE MORE BIDS.
                return total
                    
        else:
            if len(self.trades["asks"][commodity]) == 0:
                return 0
            else: #tally up how much trying to buy.
                total = 0.0
                total_price = 0.0
                for offer in self.trades["asks"][commodity]:
                    total += offer.quantity
                    total_price += offer.price
                    
                avg_price = total_price / len(self.trades["asks"][commodity])
#                
#                if total < limit:
#                    #PLACE MORE asks.
#                    return total
#                if total < limit:
#                    #PLACE MORE asks.
                return total# - limit
    
class Basic_AI:
    def __init__(self):
        self.path = []
    
    def take_turn(self):
        pass
#        pawn = self.parent
#         path = self.path
#         if len(path) == 0:
#             new_x = libtcod.random_get_int(0, 0, len(self.tiles) - 1)
#             new_y = libtcod.random_get_int(0, 0, len(self.tiles[new_x]) - 1)
#             pathy_path = pawn.pather.find_path((pawn.x,pawn.y),(new_x,new_y)) 
#             if pathy_path is not None:
#                 self.path = list(pathy_path)
#                 print self.parent.name + "'s path is " + str(len(self.path)) + " long!"
#             
#         else:
#             grid = self.path[0]
#             dx = grid[0] - pawn.x
#             dy = grid[1] - pawn.y
#             check = pawn.move(dx,dy)
#             if check:
#                 R.world.add_foot_traffic(self.parent.x,self.parent.y)
#             
#             self.path.remove(grid)
#             
#             if check is False:
#                 self.path = []
            


class AI_CityTrader(Basic_AI):
    def __init__(self, trade_house):
        self.trader = Trader()
        self.trader.parent = self
        self.goal_city = None #goal for trading mish.
        self.resting = 0 #0 is no, any other number is days.
        self.trading = 0 #0 is no, any othe rnumber is days left.
        self.city_gold = 0 #how much the trader has to spend when on trade mish.
        self.t_h = trade_house
        self.path = None
    
    def take_turn(self):
        
        x = self.t_h.parent.x
        y = self.t_h.parent.y
        
        if self.t_h == R.cities[0].trade_house:
            print "aha"
        
        if self.goal_city != None and self.goal_city.x == self.parent.x and self.goal_city.y == self.parent.y:
            print "I am at the city!"
            self.path = []
            self.goal_city = None
            
        if self.goal_city == None and x == self.parent.x and y == self.parent.y:
            print "I am at my home city!"
            self.path = []
            self.goal_city = None
            self.t_h.caravans_out.remove(self.parent)
            self.t_h.caravans_in.append(self.parent)
        
        if self.trading > 0:
            pass
        
        elif self.resting <=0 or self.trading <= 0:
            if self.goal_city != None:
                if self.path != None and len(self.path) > 0:
                    grid = self.path[0]
                    dx = grid[0] - self.parent.x
                    dy = grid[1] - self.parent.y
                    check = self.parent.move(dx,dy)
                    if check:
                        #TODO: 
                        R.world.add_foot_traffic(self.parent.x,self.parent.y)
                        del self.path[0]
                    if check is False:
                        self.path = []
                else:
                    #find a path. IF possible.
                    print "finding new path to ", self.goal_city.name
                    self.path = self.parent.pather.find_path((self.parent.x,self.parent.y),(self.goal_city.x,self.goal_city.y))
                    if self.path == None:
                        self.goal_city = None
                        #shift itself back to the parent city.
                        self.goal_city = None
                        self.path = self.parent.pather.find_path((self.parent.x,self.parent.y), (x,y))
                    
                    #pass
            else:
                #ask city tradehouse about what goods to take to where.
                #self.t_h.get_trade_mission(self)
                if self.goal_city == None and self.parent.x == self.t_h.parent.x and self.parent.y == self.t_h.parent.y:
                    if self.t_h.caravans_out.count(self) > 0:
                        self.t_h.caravans_out.remove(self)
                    else:
                        pass
                        #self.t_h.caravans_in.append(self)  
                #if self.goal_city != None and self.parent.x == self.t_h.parent.x and self.parent.y == self.t_h.parent.y:
                #   if self.t_h.caravans_in.count(self) > 0:
                #       self.t_h.caravans_in.remove(self)
        else:
            if self.trading > 0:
                self.trading -= 1
            elif self.resting > 0:
                self.resting -= 1
                
                    
class AI_Hero(Basic_AI):
    def __init__(self, parent = None):
        self.parent = parent
        self.motive = "none"
        self.motivations = []
        self.dict_motive = {}
        self.goal = None
        self.path = []
        self.pather = Pather()
        
    def assess_self(self):
        '''
        this needs to be called whenever the character has to make a decision about something. SO hopefully not every turn.
        
        for example:
            the hero has just finished fighting a monster. 
            it now needs to assess its health levels and if they are low find some sort of healing.
            this function should "deal" out the motivaitons. they are tallied by assess_motives() 
            
            and then acted upon in TODO: action function
        '''
        cur_health = self.parent.fighter.health
        max_health = self.parent.fighter.max_hp
        if cur_health <= max_health:
            if cur_health >= max_health * 0.8:
                motive = Motive(imp=1, main="health", other="")
            
            elif cur_health >= max_health * 0.5:
                motive = Motive(imp=2, main="health", other="comfort")
            
            if cur_health >= max_health * 0.3:
                motive = Motive(imp=3, main="health", other="comfort")
            
            if cur_health < max_health * 0.3:
                motive = Motive(imp=5, main="health", other="comfort")
            
            self.dict_motive[motive.main].append(motive)
            
        
    def add_motive(self, importance, main="",other=""):
        motive = Motive(importance,main,other)
        self.motivations.append(motive)
                
    def assess_motives(self):
        for motive in self.motivations:
            if self.dict_motive.has_key(motive.main):
                self.dict_motive[motive.main] += motive.importance
            else: 
                self.dict_motive[motive.main] = motive.importance
            
            if motive.other != "":
                if self.dict_motive.has_key(motive.other):
                    self.dict_motive[motive.other] += motive.other_imp
                else: 
                    self.dict_motive[motive.other] = motive.other_imp
                    
#             if motive.main == "none":
#                 pass
#                 #pick a random goal.
#             elif motive.main == "health":
#                 pass
#             elif motive.main == "wealth":
#                 pass
#             elif motive.main == "comfort":
#                #go to civilisation of any kind. house/village/town/city depending on desperation.
#                 pass
#             elif motive.main == "adventure":
#                #go cave/dungeon/ruin delving to find monsters and treasure.
#                 pass 
#             elif motive.main == "buy":
#                 pass
#             elif motive.main == "sell":
#                 pass
        highest_no = 0
        highest = ""
        for key in self.dict_motive.keys():
            if self.dict_motive[key] > highest_no:
                highest = key
                highest_no = self.dict_motive[key]
                
        return highest, highest_no
                
    
    def take_turn(self):
        
#        if self.next_action == None: 
#            self.assess_self()
#            self.assess_motives()
            

        if len(self.path) == 0:
            goal = choice(R.cities)
            while goal == self.goal:
                goal = choice(R.cities)
            self.goal = goal
            new_x = goal.x 
            new_y = goal.y
            pathy_path = self.pather.find_path((self.parent.x,self.parent.y),(new_x,new_y)) 
            if pathy_path is not None:
                self.path = list(pathy_path)
                print self.parent.name + "'s path is " + str(len(self.path)) + " long!"
             
        else:
            grid = self.path[0]
            dx = grid[0] - self.parent.x
            dy = grid[1] - self.parent.y
            self.parent.move_p(dx,dy)
            R.world.add_foot_traffic(self.parent.x,self.parent.y)
             
            self.path.remove(grid)
        
        
    def move_to_goal(self,x,y):
        self.owner.move(x,y)    

class Motive(object):
    def __init__(self, imp = 0, main="", other=""):
        self.main = main
        self.other = other
        self.importance = imp #higher the value the more weight of importance.
        self.other_imp = float(imp)/2 #value for the secondary motive. Halved that of the first.
        
class Pather:
    OPEN = 0
    CLOSED = 1
    
    STRAIGHT = STRAIGHT#
    DIAG = DIAG
    
    def __init__(self):
        self.node_status = {}
        self.node_costs = {}
        self.open_list = [] ## the HIGHEST cost is at the LOWEST index number.
        
         
    def check_blocked(self,point):
        x = point[0]
        y = point[1]
        
        if self.tiles[x][y].blocked:
            return True
        
        return False
        

    def replace_node(self, possible_node):
        old_grid = possible_node.grid
        old_cost = self.node_costs[old_grid]
        if self.node_status.has_key(old_grid) and self.node_status[old_grid] == self.OPEN:
            index = self.get_node_binary(old_cost, old_grid)
            if index != -1:
                del self.open_list[index]
                self.add_node(possible_node)
        else:
            print "already been removed from lists. ADDING"
            self.add_node(possible_node)
            
            
        #del self.node_status[old_node]
        #self.open_list.remove()
    
    
    def find_path(self,start,end, tiles = []): 
        
        if len(tiles) == 0:
            self.tiles = R.tiles
        else: 
            self.tiles = tiles
         
        if start[0] < 0 or start[1] < 0 or end[0] < 0 or end[1] < 0:
            print "FALSE"
            return None
        
        if self.check_blocked(start) and self.check_blocked(end):
            print str(start[0]), "/",str(start[1]),"to" + str(end[0]), "/",str(end[1]) + " tile was not traversable."
            return None
        self.open_list = []
        self.node_costs.clear()
        self.node_status.clear()
        
        end_node = PathNode(end, 0)
        start_node = PathNode(start, 0, endNode=end_node)
        #print "weeee let's go."
        self.add_node(start_node)
        
        while len(self.open_list) > 0:
            current_node = self.open_list[len(self.open_list)-1] #putting this to 0 is cool.
            #check to see if the end has been reached.
            if current_node.is_equal_to_node(end_node) and current_node == self.open_list[0]:
                best_path = []
                while current_node != None:
                    best_path.insert(0, current_node.grid)
                    current_node = current_node.parent_node
                #return the path of grid points.
                print "open_list is " + str(len(self.open_list)) + " long"
                return best_path
            else:
                if current_node.is_equal_to_node(end_node) and current_node != self.open_list[0]:
                    current_node = self.open_list[len(self.open_list)-2]
                #do this
                if current_node.grid[0] < 0 or current_node.grid[1] < 0:
                    print "uh-oh somehow it's a minus!"
                    return None
                
                self.open_list.remove(current_node)
                self.node_status[current_node.grid] = self.CLOSED
                if self.node_costs[current_node.grid] != current_node.cost:
                    print "for some reason, the current grid costs don't match the dictionary.... fixing.."
                    self.node_costs[current_node.grid] = current_node.cost
                    
#                 if self.node_costs.has_key(current_node.grid):
#                     #node_costs is used to track the nodes. so this NEEDS to be removed.
#                     self.node_costs.pop(current_node.grid, 0)
#                 else:
#                     print "NODE WAS NOT IN NODE_COSTS"
#                     continue
                
                for neighbour in self.find_adjacent_nodes_2(current_node, end_node):
                    if self.node_status.has_key(neighbour.grid):
                        if self.node_status[neighbour.grid] == self.CLOSED:
                            continue
                        if self.node_status[neighbour.grid] == self.OPEN or neighbour.cost < self.node_costs[neighbour.grid]:
                            if neighbour.cost >= self.node_costs[neighbour.grid]:
                                continue
                            else:
                                self.replace_node(neighbour)
                    else:        
                        self.add_node(neighbour)
                self.node_status[current_node.grid] = self.CLOSED
                current_node = None
            
        
        print "failed", len(self.open_list), start[0], start[1], " --- > ", end[0],end[1]
        return None   
    
    def add_node(self, node):
        cost = node.cost
        index = self.add_to_open_list_(cost, node)
        self.open_list.insert(index, node)
        self.node_costs[node.grid] = cost
        self.node_status[node.grid] = node.open 
    
    def add_to_open_list(self, node):
        index = 0
        cost = node.cost
        
        while len(self.open_list) > index and cost < self.open_list[index].cost:
            index += 1
        
        self.open_list.insert(index, node)
        self.node_status[node.grid] = node.open
        self.node_costs[node.grid] = node.cost
        
    def get_node_binary(self, cost, grid, high=-1, low=0):
        #TODO: finish this.
        #NOT FINISHED
        length = len(self.open_list)
        index = -1
        
        if high == -1:
            high = length - 1
        
        mid = (high+low) /2
        
        if(length <= 0):
            return -1
        else:
            if length == 1:
                if self.open_list[0].cost == cost:  
                    return 0
                else:
                    print "bloop"
                    return -1
                
            elif length == 2:
                if self.open_list[0].cost == cost:  
                    return 0
                elif self.open_list[1].cost == cost:  
                    return 1
                else:
                    return 2
            else:
                if self.open_list[high].cost == cost:
                    if self.open_list[high].grid[0] == grid[0] and self.open_list[high].grid[1] == grid[1]:
                        #print "returning as it's the same."
                        return high
                    else:
                        #need to cycle through any that cost the same.
                        print "not returning as not the same grid"
                        return -1
                elif self.open_list[mid].cost == cost:
                    if self.open_list[mid].grid[0] == grid[0] and self.open_list[mid].grid[1] == grid[1]:
                        #print "returning as it's the same."
                        return mid
                    else:
                        print "not returning as not the same grid"
                        return -1
                elif self.open_list[low].cost == cost:
                    if self.open_list[low].grid[0] == grid[0] and self.open_list[low].grid[1] == grid[1]:
                        #print "returning as it's the same."
                        return low
                    else:
                        print "not repturning as not the same grid"
                        return -1
                else:
                    if cost < self.open_list[low].cost and cost > self.open_list[high].cost:
                        if self.open_list[mid].cost >= cost:
                            index = self.get_node_binary(cost, grid, mid, low)
                        elif self.open_list[mid].cost < cost:
                            index = self.get_node_binary(cost, grid, high, mid)
                    else:
                        #print "didn't find in open list"
                        return -1
                        

        return index       
        
    def add_to_open_list_(self, cost, node, high=-1, low=0):
        index = -1
        length = len(self.open_list)
        if high == -1:
            high = length - 1
        mid = (high+low) /2
        if(length <= 0):
            return 0
        else:
            if length == 1:
                if self.open_list[0].cost > cost:  
                    return 1
                elif self.open_list[0].cost <= cost:  
                    return 0
            elif length == 2:
                if self.open_list[0].cost <= cost:  
                    return 0
                elif self.open_list[1].cost <= cost:  
                    return 1
                else:
                    return 2
            else:
                if mid == length -1:
                    if self.open_list[mid].cost > cost:  
                        index = mid+1
                    elif self.open_list[mid].cost <= cost:  
                        index = mid
                elif mid == 0:
                    if self.open_list[0].cost > cost:  
                        index = 1
                    elif self.open_list[0].cost <= cost:  
                        index = 0
                else:
                    if self.open_list[mid].cost > cost and self.open_list[mid+1].cost < cost:  
                        return mid +1
                    elif self.open_list[0].cost < cost and self.open_list[mid-1].cost > cost:  
                        return mid
                    elif self.open_list[0].cost > cost: 
                        index = self.add_to_open_list_(cost, node, high, mid+1)
                    elif self.open_list[0].cost < cost: 
                        index = self.add_to_open_list_(cost, node, mid-1, low)
        return index
        
                
    
    def find_adjacent_nodes_2(self,current,end):
        nodes = []
        X = current.grid[0]
        Y = current.grid[1]
        distance = current.diag_heuristic(current.grid,end.grid)
        distance *= (1.0 + 1/1000)# agh 
        #distance = distance + (distance * 0.1) #current distance + 10% so that it excludes directly away from the target.
        length_x = len(self.tiles) - 1
        length_y = len(self.tiles[0]) - 1
        
        #Orthogonal directions
        point = (X-1, Y)#left
        new_distance = current.diag_heuristic(point,end.grid)
        if X > 0 and not self.check_blocked(point) and new_distance < distance: 
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end))
        point = (X+1, Y)#right
        new_distance = current.diag_heuristic(point,end.grid)
        if X < length_x and  not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end))
        point = (X, Y-1)#Up 
        new_distance = current.diag_heuristic(point,end.grid)
        if Y > 0 and not self.check_blocked(point) and new_distance < distance: 
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end))
        point = (X, Y+1)#Down
        new_distance = current.diag_heuristic(point,end.grid)
        if Y < length_y and not self.check_blocked(point) and new_distance < distance: 
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end)) 
        
        #Diagonal directions.
        point = (X-1, Y-1)  #upleft
        new_distance = current.diag_heuristic(point,end.grid)
        if X > 0 and Y > 0 and not self.check_blocked(point) and new_distance < distance: 
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))
        point = (X-1, Y+1)#down left
        new_distance = current.diag_heuristic(point,end.grid)
        if X > 0 and Y < length_y and not self.check_blocked(point) and new_distance < distance: 
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))
        point = (X+1, Y-1)#up-right
        new_distance = current.diag_heuristic(point,end.grid)
        if X < length_x and Y > 0 and not self.check_blocked(point) and new_distance < distance: 
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))
        point = (X+1, Y+1)#down-right
        new_distance = current.diag_heuristic(point,end.grid)
        if X < length_x and Y < length_y and not self.check_blocked(point) and new_distance < distance: 
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))
        
        
        return nodes

    def get_cost(self, point):
        #gets the cost of tile-movement.
        cost = self.tiles[point[0]][point[1]].cost
        return cost 

class PathNode:
    OPEN = 0
    CLOSED = 1

    
    def __init__(self, grid, cost, parentNode=None, endNode=None):
        self.grid = grid
        self.direct_cost = cost
        self.cost = 0
        self.open = self.OPEN
        
        self.parent_node = parentNode
        self.end_node = endNode
        
        if self.end_node != None:
            self.cost = self.direct_cost + self.diag_heuristic(self.grid, self.end_node.grid)
        
    def diag_heuristic(self,start, end):
#         dx = abs(start[0] - end[0])
#         dy = abs(start[1] - end[1])
#         return 10 * max(dx, dy)
    
        dx = abs(start[0] - end[0])
        dy = abs(start[1] - end[1])
        beep = STRAIGHT * (dx + dy) + (DIAG - 2 * STRAIGHT) * min(dx, dy) #+ (dx + dy)* GRASS 
        return beep
    
    def heuristic(self, node, end):
        return math.sqrt((end[0] - node[0])**2 + (end[1] - node[1])**2)
    
    def linear_cost(self):
        dx = self.end_node.grid[0] - self.grid[0] 
        dy = self.end_node.grid[1] - self.grid[1]  
        
        dx = abs(dx)
        dy = abs(dy)
        
        tempCost = 10 * min(dx, dy) + 10 * (max(dx, dy) - min(dx, dy))
        return tempCost  
    
    def LinearCost(self, point):
        dx = point[0] - self.grid[0] 
        dy = point[1] - self.grid[1]  
        
        dx = abs(dx)
        dy = abs(dy)
        
        tempCost = 10 * min(dx, dy) + 10 * (max(dx, dy) - min(dx, dy))
        return tempCost  
    
    def is_equal_to_node(self, node):
        if node.grid == self.grid:
            return True
        
        if node.grid[0] == self.grid[0] and node.grid[1] == self.grid[1]:
            return True
        
        return False



#hero_man = Object(x=0, y=0, char="@", name="blob", colour=libtcod.white, blocks=False, always_visible=False,
#                    ai=AI_Hero())
#hero_man.ai.add_motive(5, "wealth", "adventure")
#hero_man.ai.add_motive(5, "wealth", "adventure")
#hero_man.ai.add_motive(5, "wealth", "adventure")
#hero_man.ai.add_motive(5, "wealth", "adventure")
#hero_man.ai.add_motive(5, "health", "comfort")
#hero_man.ai.add_motive(5, "health", "comfort")
#hero_man.ai.add_motive(5, "buy", "adventure")
#hero_man.ai.add_motive(5, "sell", "wealth")
#hero_man.ai.add_motive(5, "wealth", "sell")
#hero_man.ai.add_motive(5, "comfort", "health")
#hero_man.ai.assess_motives()

