"""
Created on 23 Mar 2013

@author: Emily
"""

resource_chances = """{
    "ore": 
            {    
                "mountain":0,
                "tundra":5,
                "taiga":8,
                "temperate_forest":10, 
                "temperate_steppe":10, 
                "rain forest":5, 
                "tree savanna":12, 
                "grass savanna":15, 
                "dry steppe":20, 
                "semi-arid desert":20, 
                "arid desert":20, 
                "river":0
            },
    "food" : {
                "mountain":0, 
                "tundra":0, 
                "taiga":0, 
                "temperate forest":1, 
                "temperate steppe":5, 
                "rain forest":0, 
                "tree savanna":12, 
                "grass savanna":20, 
                "dry steppe":20, 
                "semi-arid desert":0, 
                "arid desert":0, 
                "river":5
            },
    "clay" : {
                "mountain":0, 
                "tundra":0, 
                "taiga":0, 
                "temperate forest":0, 
                "temperate steppe":0, 
                "rain forest":10, 
                "tree savanna":0, 
                "grass savanna":10, 
                "dry steppe":20, 
                "semi-arid desert":20, 
                "arid desert":20, 
                "river":5
            },
    "silt" : {
                "mountain":0, 
                "tundra":0, 
                "taiga":0, 
                "temperate forest":0, 
                "temperate steppe":0, 
                "rain forest":0, 
                "tree savanna":0, 
                "grass savanna":0, 
                "dry steppe":0, 
                "semi-arid desert":0, 
                "arid desert":0, 
                "river":500
            },
    "wood" : {
                "mountain":0, 
                "tundra":0, 
                "taiga":1000, 
                "temperate forest":1000, 
                "temperate steppe":1000, 
                "rain forest":1000, 
                "tree savanna":1000, 
                "grass savanna":5, 
                "dry steppe":0, 
                "semi-arid desert":0, 
                "arid desert":0, 
                "river":500
            }
    "flax" : {
                "mountain":0, 
                "tundra":0, 
                "taiga":0, 
                "temperate forest":0, 
                "temperate steppe":10, 
                "rain forest":0, 
                "tree savanna":0, 
                "grass savanna":20, 
                "dry steppe":20, 
                "semi-arid desert":5, 
                "arid desert":0, 
                "river":0
            }



}"""

raw_resources = """{
    "copper": {
        "name":"copper", 
        "category":"ores", 
        "resource_class":"strategic", 
        "gather_amount":4, 
        "break_chance":200,
        "app_chance":"ore"
        },
    "bronze": {
        "name":"bronze", 
        "category":"ores", 
        "resource_class":"strategic", 
        "gather_amount":4, 
        "break_chance":100,
        "app_chance":"ore"
        },
    "iron": {
        "name":"iron", 
        "category":"ores", 
        "resource_class":"strategic", 
        "gather_amount":4, 
        "break_chance":60,
        "app_chance":"ore"
        },
    "food": {
        "name":"food", 
        "category":"food", 
        "resource_class":"strategic", 
        "gather_amount":8, 
        "break_chance":1,
        "app_chance":"food"
        },
    "clay": {
        "name":"clay", 
        "category":"clays", 
        "resource_class":"strategic", 
        "gather_amount":4, 
        "break_chance":200,
        "app_chance":"clay"
        },
    "silt": {
        "name":"silt", 
        "category":"clays", 
        "resource_class":"strategic", 
        "gather_amount":4, 
        "break_chance":200,
        "app_chance":"silt"
        },
    "wood": {
        "name":"wood", 
        "category":"woods", 
        "resource_class":"strategic", 
        "gather_amount":4, 
        "break_chance":200,
        "app_chance":"wood"
        },
    "flax": {
        "name":"flax", 
        "category":"cloths", 
        "resource_class":"strategic", 
        "gather_amount":4, 
        "break_chance":200,
        "app_chance":"flax"
        }
    
}"""

finished_resources = """{
    "copper tools": {
        "category":"tools", 
        "resource_class":"strategic", 
        "material":"copper", 
        "in_amt":2,
        "out_amt":1
        }
    "bronze tools": {
        "category":"tools", 
        "resource_class":"strategic", 
        "material":"bronze", 
        "in_amt":2,
        "out_amt":1
        }
    "iron tools": {
        "category":"tools", 
        "resource_class":"strategic", 
        "material":"iron", 
        "in_amt":2,
        "out_amt":1
        }
    "iron sword": {
        "category":"tools", 
        "resource_class":"strategic", 
        "material":"iron", 
        "in_amt":2,
        "out_amt":1,
        "name":"iron sword"
        }
    "silt pottery": {
        "category":"pottery", 
        "resource_class":"strategic", 
        "material":"silt", 
        "in_amt":1,
        "out_amt":1
        }
    "clay pottery": {
        "category":"pottery", 
        "resource_class":"strategic", 
        "material":"clay", 
        "in_amt":1,
        "out_amt":1
        }
    "wood furniture": {
        "category":"furniture", 
        "resource_class":"strategic", 
        "material":"wood", 
        "in_amt":1
        "out_amt":1
        }
    "flax clothing": {
        "category":"clothing", 
        "resource_class":"strategic", 
        "material":"flax", 
        "in_amt":1,
        "out_amt":1
        }

}"""

gatherers_by_token = """{
                         'food':{'name':'Food Farmer', 'consumed':[], 'essential':['tools'], 'preferred':['clothing', 'furniture', 'pottery'] },
                         'flax':{'name':'Flax Farmer', 'consumed':[], 'essential':['tools'], 'preferred':['furniture', 'pottery'] },
                         'copper':{'name':'Copper Miner', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] },
                         'bronze':{'name':'Bronze Miner', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] },
                         'iron':{'name':'Iron Miner', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] },
                         'clay':{'name':'Clay Gatherer', 'consumed':[], 'essential':[], 'preferred':['clothing'] },
                         'silt':{'name':'Silt Gatherer', 'consumed':[], 'essential':[], 'preferred':['clothing'] },
                         'wood':{'name':'Woodcutter', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] }
                         }"""
# Good producers
producers_by_token = """{                     
                         'copper tools':{'name':'Copper Blacksmith', 'finished_good':'copper tools', 'consumed':['woods'], 'essential':[], 'preferred':['clothing'] },
                         'bronze tools':{'name':'Bronze Blacksmith', 'finished_good':'bronze tools', 'consumed':['woods'], 'essential':[], 'preferred':['clothing'] },
                         'iron tools':{'name':'Iron Blacksmith', 'finished_good':'iron tools', 'consumed':['woods'], 'essential':[], 'preferred':['clothing'] },
                         'silt pottery':{'name':'Silt Potter', 'finished_good':'silt pottery', 'consumed':[], 'essential':[], 'preferred':['clothing'] },
                         'clay pottery':{'name':'Clay Potter', 'finished_good':'clay pottery', 'consumed':[], 'essential':[], 'preferred':['clothing'] },
                         'wood furniture':{'name':'Wood Carptenter', 'finished_good':'wood furniture', 'consumed':[], 'essential':['tools'], 'preferred':['clothing'] },
                         'flax clothing':{'name':'Flax Clothier', 'finished_good':'flax clothing', 'consumed':[], 'essential':['tools'], 'preferred':[] }
                         }"""



# How many gatherers of a resource a city starts with.
city_gatherers_templates = """
                {
                    "1": {"ores": 1, "foods":10,    "cloths":7, "clays":4, "woods":3},
                    "2": {"ores": 9, "foods":5,     "cloths":2, "clays":3, "woods":4},
                    "3": {"ores": 5, "foods":8,     "cloths":5, "clays":6, "woods":5},
                    "4": {"ores": 3, "foods":3,     "cloths":9, "clays":4, "woods":3},
                    "5": {"ores": 7, "foods":7,     "cloths":7, "clays":7, "woods":7},
                    "6": {"ores": 0, "foods":12,    "cloths":6, "clays":9, "woods":6},
                    "7": {"ores": 7, "foods":7,     "cloths":7, "clays":7, "woods":7},
                    "8": {"ores": 9, "foods":2,     "cloths":2, "clays":7, "woods":10}
                     
                }"""

# How many producers of goods a city starts with.
city_producers_templates = """
                {
                    "1": {"copper tools": 1, "bronze tools":4, "iron tools":8, "silt pottery":1, "clay pottery":8, "wood furniture":4, "flax clothing":3},
                    "2": {"copper tools": 2, "bronze tools":5, "iron tools":7, "silt pottery":2, "clay pottery":7, "wood furniture":3, "flax clothing":2},
                    "3": {"copper tools": 3, "bronze tools":6, "iron tools":6, "silt pottery":3, "clay pottery":6, "wood furniture":2, "flax clothing":9},
                    "4": {"copper tools": 4, "bronze tools":7, "iron tools":5, "silt pottery":4, "clay pottery":5, "wood furniture":1, "flax clothing":1},
                    "5": {"copper tools": 5, "bronze tools":7, "iron tools":4, "silt pottery":5, "clay pottery":4, "wood furniture":1, "flax clothing":1},
                    "6": {"copper tools": 6, "bronze tools":8, "iron tools":3, "silt pottery":6, "clay pottery":3, "wood furniture":9, "flax clothing":2},
                    "7": {"copper tools": 7, "bronze tools":9, "iron tools":2, "silt pottery":7, "clay pottery":2, "wood furniture":3, "flax clothing":3},
                    "8": {"copper tools": 8, "bronze tools":9, "iron tools":1, "silt pottery":8, "clay pottery":1, "wood furniture":4, "flax clothing":1},
                     
                }"""
