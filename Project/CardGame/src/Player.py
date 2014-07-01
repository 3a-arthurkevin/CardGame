# -*- coding : utf-8 -*-
# -*- coding: iso-8859-1 -*-

import queue

class Player:
    
    def __init__(self, namePlayer):
        self.name = namePlayer
        self.lifePoint = 10
        self.maxCardInHand = 10
        self.hand = []
        self.deck = queue.Queue()
        
        self.maxCardInBoardForServant = 5
        self.maxCardInBoardForItem = 5
        self.servantsOnBoard = []
        self.itemOnBoard = []
        
        
    def load(self, idPlayer):
        
        
        return True
    
    def takeCardIntoDeck(self):
        """
        Pioche une carte dans le deck 
        si il y en reste
        si le joueur n'a pas atteint la limite de carte en main maximum
        """    
        #if len(self.deck) <= 0:
        if self.deck.qsize() <= 0:
            return False
        
        if len(self.hand) >= self.maxCardInHand:
            del self.hand[self.maxCardInHand]
            
        self.hand.append(self.deck.get())
        
    def putServantInBoard(self, cardServantInHand):
        """
        Fonction qui pose une carte sur le terrain si il y a un remplacement libre
        pour les cartes serviteurs ou les cartes objets
        """ 
        i = self.findFreeSlotForServant()
        if(i >= 0):
            self.servantsOnBoard[i] = cardServantInHand
            return True
        return False
    
    def putItemInBoard(self, cardItemInHand):
        i = self.findFreeSlotForItem()
        if(i >= 0):
            self.itemOnBoard[i] = cardItemInHand
            return True
        return False
    
    
    def findFreeSlotForServant(self):
        """
        Fonctions qui retoure l'index d'un emplacement libre sur le plateau
        soit pour les servants, soit pour les objets
        """
        if(len(self.servantsOnBoard) >= self.maxCardInBoard):
            return -1
        return len(self.servantsOnBoard)
    
    def findFreeSlotForItem(self):
        if(len(self.itemOnBoard) >= self.maxCardInBoardForItem):
            return -1
        return len(self.itemOnBoard)
    
    def removeCardFromHand(self, card):
        """
        Fonction qui retire de la main une carte posée
        """
        self.hand.remove(card)
        
    def hasLoose(self):
        if self.lifePoint <= 0:
            return True
        
        if self.deck.qsize() <= 0:
            return True
        
        return False
