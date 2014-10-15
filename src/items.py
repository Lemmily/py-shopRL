'''
Created on 27 Aug 2013

@author: Emily
'''
import libtcodpy as libtcod
import entities.Object as Object

"""NOT USED AT THE MOMENT"""

class Item(Object):
    def __init__(self, x=0,y=0,char="#",name="None",type="object",colour=libtcod.white, blocks=False, always_visible=False, 
                    item =None):
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
            

class Item_Comp:
    def __init__(self,char="$",colour=libtcod.white,type="object"):
        """These are all things that are held in the Object class atm"""
        self.x = 0
        self.y = 0
        self.char = char
        self.colour = colour
        self.type = type
        