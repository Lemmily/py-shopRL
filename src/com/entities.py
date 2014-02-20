'''
Created on 16 Mar 2013

@author: Emily
'''
import libtcodpy as libtcod
import R
import math
import economy
import sentient
import Utils


class Object:
    
    def __init__(self, x=0, y=0, char="@", name="blob", colour=libtcod.white, blocks=False, always_visible=False,
                    item=None, type = "object"):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.type = type
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
        
    def draw_faded(self, cam_x=0, cam_y=0): 
        
        if (self.x >= cam_x and self.x < cam_x + R.MAP_VIEW_WIDTH and 
                self.y >= cam_y and self.y < cam_y + R.MAP_VIEW_HEIGHT):
            pos_x = self.x - cam_x
            pos_y = self.y - cam_y
            
            colour = libtcod.Color(self.colour.r,self.colour.g,self.colour.b)
            libtcod.color_scale_HSV(colour, 0.7, 0.7) #hopefully 80% saturation.
            libtcod.console_set_default_foreground(R.con_char, colour)
            libtcod.console_put_char(R.con_char, pos_x, pos_y, self.char, libtcod.BKGND_NONE)#ADDALPHA(0.0))

    def draw(self, cam_x=0, cam_y=0): 
        
        if (self.x >= cam_x and self.x < cam_x + R.MAP_VIEW_WIDTH and
                self.y >= cam_y and self.y < cam_y + R.MAP_VIEW_HEIGHT):
            
                pos_x = self.x - cam_x
                pos_y = self.y - cam_y
                
                libtcod.console_set_default_foreground(R.con_char, self.colour)
                libtcod.console_put_char(R.con_char, pos_x, pos_y, self.char, libtcod.BKGND_NONE)

class Mover(Object):
    def __init__(self, x=0, y=0, char="@", name="blob", colour=libtcod.white, blocks=False, always_visible=False,
                        stats=None, you=None, pather=None, ai=None):
        Object.__init__(self, x, y, char, name, colour, blocks, always_visible)
        self.direction = "S"
        
        self.activity_log = {"history": [], "kills": [], "travels": [], "transactions":[]}
        
        self.stats = stats
        if stats:
            self.stats.parent = self
        
        self.inventory = sentient.Inventory() #not entirely sure where htis needs to go.
        
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

class Player(Mover):
    def __init__(self, d_l = 0):
        Mover.__init__(self)
        
        self.dungeon_level = d_l #what is this? depth?
        R.inventory = self.inventory = sentient.Inventory() #= {"armour":[], "melee":[], "potions":[],"scrolls":[]}
        self.skills = sentient.Skills()
        
        
    def grab_item(self, object_):
        self.inventory.append(object_)


class Item:
    def __init__(self, use_function = None):
        self.use_function = use_function
        self.parent = None

    def use(self):
        if self.use_function is None:
            R.ui.message(self.parent.name + " cannot be used!")
        else:
            if self.use_function() == "used":
                R.inventory.remove(self.parent)
                
class Hero:
    def __init__(self):
        self.dungeon_level = 0 #floor level currently on.
        self.inventory = [] #stuff being carried
        self.equipment = [] #attempts to have one armour one weapon one clothing. (to start with)
    #unsure as to what needs to go here.
    
class Fighter:
    def __init__(self, max_hp=100, max_mp=0):
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp   
    
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

attributes = ["str","con","dex","int","cha","wis", "luc"]

skill_list_1 = [ #// 0_name:string, 1_attribute, 2_needTraining:Boolean, 3_desc:String,[4_dependsOn],[5_dependants]
                 ["Appraise", "int", False, "Used to analyse an item for monetary value, and contributing factors",["none"],["none"]],
                 ["Armour", "str", False, "How well you can wear armour. Negates some of the penalties of heavier armour",["none"],["none"]],
                 ["Dodge", "dex", False, "Improves your chance of dodging attacks and traps",["none"],["none"]],
                 ["Fighting", "dex", False, "Improves your chance of hitting and your damage in melee",["none"],["none"]],
                 ]
# Skill manager
class Stats:
    def __init__(self, max_hp = 100, max_mp = 10):
        self.skills = {}
        for line in skill_list_1:
            self.skills[line[0].lower()] = Skill( line[0], line[1])
            
        self.attr = {}
        for stat in attributes:
            self.attr[stat] = Attribute(stat, 10)
            
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp   
        
        self.ac = -1 # not calculated yet.
        
        
    def skill_level_check(self,skill):
        
        sk_lvl = self.skills[skill].level
        
        return sk_lvl #TODO: nake lookup table to look up what level the skill is at. for now just retrun this/
    
    def has(self, skill):
        if self.skills.has_key(skill):
            return True
        return False
    
    def get_level(self,skill):
        return self.skills[skill].level
    
    def skill_check(self, name):
        if self.has(name):
            skill = self.skills[name]
            return roll_d20() + skill.level + self.attr[skill.group].modifier
    
    def gain_exp(self,amount, skill):
        #TODO: this is temporpary - I want to have exp spread over multiple skills. similar to crawl.
        self.skills[skill].gain(amount)
        
    def update_AC(self):
        skill = self.skill_level_check("armour")
        self.ac = self.parent.inventory.get_AC() * (22 + skill)/ 22
        
    def get_AC(self):
        return self.ac
    
    def get_GDR(self, damage):
        #gdr works *only* against melee.
        #only *guaranteed* an amount of damage reduction equal to 1/2 AC
        #be sure to make sure AC is up to date when any armour/skill has changed with update_AC()
        
        gdr_per = 14 * math.sqrt(self.get_AC() - 2)
        
        return min(damage * gdr_per /100, self.ac)
        
        
        
        

class Skill:
    def __init__(self,name,group="None"):
        self.name = name
        self.group = group
        self.exp = 0
        self.level = 1
        self.aptitude = 1 #speed at which they gain skill levels.... probably somewhere better to hold this.
       
    def gain(self,amount):
        self.exp += amount
        if self.exp > 100:
            self.level += 1
            self.exp -= 100
            R.ui.message("You have leveled up " + self.name + " to level " + str(self.level))
        
class Attribute():
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    
    @property
    def modifier(self):
        if self.value <= 1: return -5
        elif self.value < 4: return -4
        elif self.value < 6: return -3
        elif self.value < 8: return -2
        elif self.value < 10: return -1
        elif self.value < 12: return 0
        elif self.value < 14: return 1
        elif self.value < 16: return 2
        elif self.value < 18: return 3
        elif self.value <= 20: return 5
        elif self.value > 20: return 6


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
    
def roll_d20():
    return libtcod.random_get_int(0, 1, 20)
