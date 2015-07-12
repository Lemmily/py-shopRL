'''
Created on 29 Mar 2013

@author: Emily
'''

rooms = """{
    "crypt":{
                "monster types": ["undead","bandits"],
                "treasure": "sometimes",
                "colours": [(22,22,22), (44,44,44), (66,66,66), (88,88,88), (44,55,44)], #dark/murky reds, browns, dark greens
                "openness":25
            },
    "vault":{
                "monster types": ["orcs","goblins","bandits"],
                "treasure": "yes",
                "colours": [(22,22,22), (44,44,44), (66,66,66), (88,88,88), (44,55,44)],
                "openness": 2
                
            },
    "hall":{
                "monster types": ["general"],
                "treasure": "sometimes",
                "colours": [(22,22,22), (44,44,44), (66,66,66), (88,88,88), (44,55,44)],
                "openness": 50
            },
    }"""
##theStats = [0_STR, 1_DEX, 2_PER, 3_CON, 4_INT, 5_WIS, 6_CHA, 7_LUCK];
monsters = """{
            "1":{
                    "goblin":   ["goblin","g",[10,100,10],["head","torso","left","right"],[6,6,7,4,8,4,2,7]],
                    "wolf":     ["wolf","w",[50,50,50],[], [7,9,8,3,9,4,3]],
                    "giant rat":   ["giant rat","r",[80,10,80],[]]
                },
            "2":{
                    "orc":      ["orc","o",[70,140,70],["head","torso","legs","left","right"], [10,6,7,8,7,6,2,7]],
                    "kobold":   ["kobold","k",[218,160,30],["head","torso","left","right"]]
                }
            } """
# monsters = """{
#     "1":{
#            "goblin":{  "name":"goblin",
#                        "char":"g",
#                        "colour":[10,100,10],
#                        "equipment":["head","torso","right","left"]
#                     },
#                        
#            "wolf":{    "name":"wolf",
#                        "char":"w",
#                        "colour":[50,50,50]
#                     },
#                        
#            "giant rat":{
#                        "name":"giant rat",
#                        "char":"r",
#                        "colour":[80,10,80]
#                     }
#               },
#               
#     "2":{
#             "orc":  {
#                 "name":"Orc",
#                 "char":"o",
#                 "colour":[10,100,10],
#                 "equipment":["head","torso","legs","right","left"],
#                 },
#             "kobold": {
#                 "name":"Kobold",
#                 "char":"k",
#                 "colour":[10,100,10],
#                 "equipment":["head","torso","right","left"]
#                 }
#     }"""











master_items_list = [
    ##[0_Value,1_Level,2_Power,3_type,4_ActualName,5_SubType,[6_Effect], 7_DC, 8_AC, 9_EV, [10_damage (times dice rolled), (dice sides), (bonus)], 11_UsefUnction]

    [6, 1, 0, "clothing", "Tatty Shirt", "Cloth Scraps", [1], 1, 1, 0, None],
    [6, 1, 0, "clothing", "Linen Sack", "Cloth Scraps", [1], 4, 1, 0, None],
    [8.9, 1, 1, "clothing", "Tatty Robe", "Cloth Robe", [1], 7, 1, 0, None],
    [13, 1, 2, "clothing", "Woven Robe", "Cloth Robe", [1], 13, 2, 0, None],
    [24, 2, 2, "clothing", "Silk Robe", "Cloth Robe", [1], 18, 3, 0, None],

    [8, 1, 0, "armour", "Farmers Garb", "Leather Scraps", [1], 3, 2, -1, None],
    [17, 1, 1, "armour", "Hide Armour", "Leather Armour", [1], 6, 2, 0, None],
    [30, 1, 2, "armour", "Leather Vest", "Leather Armour", [1], 12, 2, -1, None],
    [60, 2, 1, "armour", "Chainmail", "Metal Armour", [1], 14, 7, -4, None],
    [100, 2, 2, "armour", "Metal Breastplate", "Metal Armour", [1], 17, 10, -5, None],

    [4, 1, 0, "weapon", "Tree Branch", "Club", [1], 4, 0, 0, [1, 4, 0]],
    [6, 1, 1, "weapon", "Rusty Dagger", "Dagger", [1], 6, 0, 0, [1, 6, 0]],
    [13, 1, 2, "weapon", "Dagger", "Dagger", [1], 10, 0, 0, [2, 6, 0]],
    [25, 2, 1, "weapon", "Short Sword", "Sword", [1], 12, 0, 0, [2, 8, 4]],
    [30, 2, 2, "weapon", "Long Sword", "Sword", [1], 14, 0, 0, [3, 8, 2]],
    [45, 3, 1, "weapon", "Rapier", "Sword", [1], 16, 0, 0, [3, 10, 6]],
    [65, 3, 2, "weapon", "GreatSword", "Sword", [1], 18, 0, 0, [2, 12, 8]],

    [25, 1, 0, "potion", "Healing Potion", "Potion", [1], 18, 0, 0, None, "heal"],
    [25, 1, 0, "potion", "Hurtful Potion", "Potion", [1], 19, 0, 0, None, "hurt"],
    [25, 1, 0, "potion", "Poison", "Potion", [1], 18, 0, 0, None, "poison"],
    [25, 1, 0, "potion", "Hurtful Potion", "Potion", [1], 19, 0, 0, None, "hurt"],
]
