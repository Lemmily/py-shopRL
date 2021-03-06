'''
Created on 10 Mar 2013

@author: Emily
'''

import random

from src import libtcodpy as libtcod


def random_choice(chances_dict):
    #choose one option from a dictionary of chances, returning the key.

    chances = chances_dict.values() # all the values
    strings = chances_dict.keys() #all the keys

    return strings[rand_choice_index(chances)]

def rand_choice_index(chances): #choose one option from the list of chances, returning its index
    #the dice will land on some number between 1 and the sum of all the chances.
    dice = libtcod.random_get_int(0, 1, sum(chances))

    #go through all chances, keeping the sum so far
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w
        #sees if the dice landed in the part that corresponds to this choice
        if dice <= running_sum:
            return choice
        choice += 1
        
                
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
                        
def roll_100():
    return int(random.random() * 100)



def flip():
    if chance_roll(50):
        return True
    else:
        return False



def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))


def in_rectangle(ix, iy, w, h):
    return 0 <= ix < w and 0 <= iy < h


def maxi(a, b):
    if a > b: return a
    else: return b

def mini(a, b):
    if a < b: return a
    else: return b
