__author__ = 'lemmily'


"""
Created on 4 Mar 2013

@author: Emily
"""
import libtcodpy as libtcod
from src import R
from src.game import Game

if __name__ == "__main__":
    libtcod.console_set_custom_font("ont_big.png", libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(R.SCREEN_WIDTH, R.SCREEN_HEIGHT, "Trader-RL", False)
    libtcod.sys_set_fps(R.LIMIT_FPS)
    con = libtcod.console_new(R.SCREEN_WIDTH, R.SCREEN_HEIGHT)
    game = Game(con)
    game.run()
