# -*- coding : utf-8 -*-

from Player import Player

class Game:
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
        self.board = [[]] * 2 # Plateau a deux cote, chaque cote correspond a un joueur
        self.players = [Player(), Player()]
        
    def destroyCard(self):
        print("destroy")