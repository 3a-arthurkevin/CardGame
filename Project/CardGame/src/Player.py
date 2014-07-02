# -*- coding : utf-8 -*-

import queue
import random

class Player:
    
    totalCardIntoDeck = 30
    
    def __init__(self, namePlayer):
        self.name = namePlayer
        self.lifePoint = 10
        self.maxCardInHand = 10
        self.hand = []
        self.cardsList = []
        self.deck = queue.Queue()
        
        self.maxCardInBoardForServant = 5
        self.maxCardInBoardForItem = 5
        self.servantsOnBoard = []
        self.itemOnBoard = []
        
        
    def createDeck(self, cardsList):
        """Fonction qui demande à l'utilisateur de constituer son deck
        Rempli le tableau cardList des cartes choisit par l'utilisateur
        """
        
        if len(cardsList) <= 0:
            print("CardList empty")
            return False
        
        print("Création du deck du joueur : ", self.name)
        print("Choississez entre les 3 cartes proposées jusqu'à arriver à un total de ", Player.totalCardIntoDeck , " cartes dans votre deck")
        
        while len(self.cardsList) < 30:
            cards = []
            print(Player.totalCardIntoDeck - len(self.cardsList), " cartes restante à choisir")
            
            for i in range(3):
                cards.append(cardsList[random.randint(0, len(cardsList)-1)])
                print(i+1, ")", cards[i])
            
            validChoose = False
            choose = 0
            
            while not validChoose:
                try:
                    choose = int(input("Quelle carte avez vous choisit ? "))
                except ValueError:
                    choose = 0
                    
                if choose >= 1 and choose <= 3:
                    validChoose = True
                else:
                    print("Choix invalide")
            
            self.cardsList.append(cards[choose-1])
        
        return True
    
    def takeCardIntoDeck(self):
        """
        Pioche une carte dans le deck 
        si il y en reste
        si le joueur n'a pas atteint la limite de carte en main maximum
        """
        
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
    
    
    """
    Fonction qui retire de la main une carte pos�e
    """
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
