# -*- coding : utf-8 -*-

from Game import Game

import pygame
from pygame.locals import *


pygame.init()

if __name__ == '__main__':
    playerOneName = "Player1"
    playerTwoName = "Player2"
    #game = Game({"playerName1" : playerOneName, "playerName2" : playerTwoName})
    #game.loop()
    
    
    """
    Loop ouverture du jeu
        -->affichage des menus
            -->faire un deck
            -->loop création deck
                -->save
                -->load
                -->retour
            -->Faire un combat
                -->1 joueur
                -->2 joueur
                -->Loop jeu
                    -->joueur entre son nom
                    -->joueur choisi sont deck
                    -->lancement nouvelle interface
                        -->combat
                        -->Fin partie
                        -->retour au menu (boucle debut)
    """