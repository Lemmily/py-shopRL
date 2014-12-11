'''
Created on 6 Sep 2013

@author: Emily
'''
import math
import R
import entities
from random import choice
from src.pathfinding import Pather, PathFinder


GRASS = 15
MOUNTAIN = 40
PATH = 5


MOTIVATIONS = ["none", "health", "wealth", "buy", "sell", "adventure", "comfort"] 


skill_list_1 = [ #// 0_name:string, 1_attribute, 2_needTraining:Boolean, 3_desc:String,[4_dependsOn],[5_dependants]
                 ["Appraise", "int", False, "Used to analyse an item for monetary value, and contributing factors",["none"],["none"]],
                 ["Armour", "str", False, "How well you can wear armour. Negates some of the penalties of heavier armour",["none"],["none"]],
                 ["Dodge", "dex", False, "Improves your chance of dodging attacks and traps",["none"],["none"]],
                 ["Fighting", "dex", False, "Improves your chance of hitting and your damage in melee",["none"],["none"]],
                ]
class Skills:
    def __init__(self):
        pass
        self.dict = {}
        for line in skill_list_1:
            self.dict[line[0]] = Skill( line[0], line[1])
        
        
    def skill_level_check(self,skill):
        
        sk_exp = self.dict[skill].exp
        
        return sk_exp #TODO: make lookup table to look up what level the skill is at. for now just retrun this/

class Skill:
    def __init__(self,name,group="None"):
        self.name = name
        self.group = group
        self.exp = 0
        
        
    
class Basic_AI:
    def __init__(self):
        self.action = "idle"
    
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
            
class Inventory:
    def __init__(self):
        self.contents = [] #might make this a dict. then pre sorted into categories.
        self.equipment = {"head":None,"torso":None,"legs":None,"hands":None,"right":None,"left":None, 
                          "ring left":None, "ring right":None, "amulet":None, "neck":None}
        
    def store_item(self,item):
        self.contents.append(item)
        
    def retrieve_item(self,item):
        if self.check_for_item(item):
            self.contents.remove(item)
            
    def check_for_item(self,item):
        if item in self.contents:
            return True
        else:
            return False
        
    def check_for_type(self,type):
        for item in self.contents:
            if item.type == type:
                return True
        return False
    
    def retrieve_all_type(self, type):
        all_items_type = []
        
        for item in self.contents:
            if item.type == type:
                all_items_type.append(item)
                
        return all_items_type

    def get_disfigured(self,wounds):
        for wound in wounds:
            self.equipment.pop(wound,None)
            
            
class Hero(Basic_AI):
    def __init__(self):
        self.path = []
        self.personality = pick_personality()
        
        
    def take_turn(self):
        pass




    
class AI_CityTrader(Basic_AI):
    """
    The job that the ai is performing.
    """
    def __init__(self, trade_house):
        Basic_AI.__init__(self)
        self.trader = entities.Trader()
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
        Basic_AI.__init__(self)
        self.parent = parent
        self.motive = "none"
        self.motivations = []
        self.dict_motive = {}
        self.goal = None
        self.path = []
        self.pather2 = Pather()
        self.pather = PathFinder()

        
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
            # pathy_path = self.pather.new_find_path((self.parent.x,self.parent.y),(new_x,new_y), R.tiles)
            pathy_path = self.pather.find_path(R.world, (self.parent.x,self.parent.y),(new_x,new_y))
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
        self.timer = 24 #hours the motive hangs around. ?
        
    def tick(self):
        self.timer -= 1
        
def pick_personality():
    pass


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

