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
    
monsters = """{
    "1":{
                   "Goblin":{  "name":"goblin",
                               "char":"g",
                               "colour":[10,100,10]
                            },
                               
                   "Wolf":{    "name":"wolf",
                               "char":"w",
                               "colour":[50,50,50]
                            },
                               
                   "Giant Rat":{
                               "name":"giant rat",
                               "char":"r",
                               "colour":[80,10,80]
                            }
              },
              
    "2":{
                    "Orc":[],
                    "Kobold": []
                }
    }"""


objects = """{
    "door":{ "blocks":"True",
             "char": "D",
             "colour": [00,00,00]
            },
            
    "box":{ "blocks": "True",
            "char": "B",
            "colour": [00,00,00]
          }
    }"""