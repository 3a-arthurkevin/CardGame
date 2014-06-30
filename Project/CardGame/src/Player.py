# -*- coding : utf-8 -*-

import queue

class Player:
    
    def __init__(self):
        self.lifePoint = 10
        self.maxCardInHand = 10
        self.hand = []
        self.deck = queue()
        
        self.maxCardInBoardForServant = 5
        self.maxCardInBoardForItem = 5
        self.servantsOnBoard = []
        self.itemOnBoard = []
        
        
    def load(self, idPlayer):
        
        
        return True
    """
    Pioche une carte dans le deck 
    si il y en reste
    si le joueur n'a pas atteint la limite de carte en main maximum
    """    
    def takeCardIntoDeck(self):
        if len(self.deck) <= 0:
            return False
        
        if len(self.hand) >= self.maxCardInHand:
            del self.hand[self.maxCardInHand]
            
        self.hand.append(self.deck.get())
        
    """
    Fonction qui pose une carte sur le terrain si il y a un remplacement libre
    pour les cartes serviteurs ou les cartes objets
    """    
    def putServantInBoard(self, cardServantInHand):
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
    
    """
    Fonctions qui retoure l'index d'un emplacement libre sur le plateau
    soit pour les servants, soit pour les objets

    """
    def findFreeSlotForServant(self):
        if(len(self.servantsOnBoard) >= self.maxCardInBoard):
            return -1
        return len(self.servantsOnBoard)
    
    def findFreeSlotForItem(self):
        if(len(self.itemOnBoard) >= self.maxCardInBoardForItem):
            return -1
        return len(self.itemOnBoard)
    
    """
    Fonction qui retire de la main une carte posée
    """
    def removeCardFromHand(self, card):
        self.hand.remove(card)