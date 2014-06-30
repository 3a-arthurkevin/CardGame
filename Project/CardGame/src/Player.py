# -*- coding : utf-8 -*-

import queue

class Player:
    
    def __init__(self):
        self.lifePoint = 10
        self.maxCardInHand = 10
        self.hand = []
        self.deck = queue()
        
        self.servantsOnBoard = []
        self.itemOnBoard = []
        
        
    def load(self, idPlayer):
        
        
        return True
        
    def takeCardIntoDeck(self):
        if len(self.deck) <= 0:
            return False
        
        if len(self.hand) >= self.maxCardInHand:
            del self.hand[self.maxCardInHand]
            
        self.hand.append(self.deck.get())