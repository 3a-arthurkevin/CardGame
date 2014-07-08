# -*- coding : utf-8 -*-

from Game import Game

"""
import pygame
from pygame.locals import *
pygame.init()
"""

if __name__ == '__main__':
    """
    Lance une partie SuperCardFighter
    """
    playerOneName = "Arthur"
    playerTwoName = "Kevin"
    
    game = Game({"playerName1" : playerOneName, "playerName2" : playerTwoName})
    
    game.players[0].drawCardForBegining()
    game.players[1].drawCardForBegining()
    
    while(game.loop()):
        continue