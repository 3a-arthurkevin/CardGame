# -*- coding : utf-8 -*-

import queue
import random

class Player:
    
    totalCardIntoDeck = 30
    
    def __init__(self, namePlayer):
        self.name = namePlayer
        self.lifePoint = 10
        self.maxCardInHand = 10
        self.hand = [None] * self.maxCardInHand 
        self.cardsList = []
        self.deck = queue.Queue()
        
        self.maxCardInBoardForServant = 5
        self.maxCardInBoardForItem = 5
        self.servantsOnBoard = [None] * self.totalCardIntoDeck
        self.itemOnBoard = [None] * self.totalCardIntoDeck
        
        self.mana = 0
        
    def displayHand(self):
        for card in self.hand:
            print(card)
    
    def addManaForPlayerTurn(self):
        self.mana = 4 
        
    def createDeck(self, cardsList):
        """
        Fonction qui demande à l'utilisateur de constituer son deck
        Remplit le tableau cardList des cartes choisi par l'utilisateur
        """
        
        if len(cardsList) <= 0:
            print("CardList empty")
            return False
        
        print("Création du deck du joueur : ", self.name)
        print("Choississez entre les 3 cartes proposées jusqu'à arriver à un total de ", Player.totalCardIntoDeck , " cartes dans votre deck")
        
        while len(self.cardsList) < self.totalCardIntoDeck:
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
    
    def takeCardFromDeck(self):
        """
        Pioche une carte dans le deck 
        si il y en reste
        si le joueur n'a pas atteint la limite de carte en main maximum
        """
        
        if self.deck.qsize() <= 0:
            print("no card")
            return False
        
        if len(self.hand) >= self.maxCardInHand:
            del self.hand[(self.maxCardInHand) - 1]
            
        self.hand.append(self.deck.get())
        return True
        
    def putServantInBoard(self, cardServantInHand):
        """
        Fonction qui pose une carte sur le terrain si il y a un emplacement libre
        pour les cartes serviteurs ou les cartes objets
        """ 
        i = self.findFreeSlotForServant()
        print(i)
        if(i >= 0):
            self.servantsOnBoard[i] = cardServantInHand
            self.hand.remove(cardServantInHand)
            return True
        return False
    
    def putItemInBoard(self, cardItemInHand):
        i = self.findFreeSlotForItem()
        print(i)
        if(i >= 0):
            self.itemOnBoard[i] = cardItemInHand
            self.hand.remove(cardItemInHand)
            return True
        return False
    
    
    def findFreeSlotForServant(self):
        """
        Fonctions qui retoure l'index d'un emplacement libre sur le plateau
        soit pour les servants
        """
        i = -1
        for j in range(len(self.servantsOnBoard)):
            if(self.servantsOnBoard[j] == None):
                return j
        return i
    
    def findFreeSlotForItem(self):
        """
        Fonctions qui retoure l'index d'un emplacement libre sur le plateau
        pour les card autre que Servant (Item et Weapon --> on pose les Weapons et les Items dans le même tableau)
        """
        i = -1
        for j in range(len(self.itemOnBoard)):
            if(self.itemOnBoard[j] == None):
                return j
        return i
    

    def removeCardFromHand(self, card):
        """
        Fonction qui retire de la main une carte posée qui est le paramètre de cette fonction
        """
        self.hand.remove(card)
        
    def removeServantFromBoard(self, servant):
        """
        Fonction retirant un Servant passé en paramètre
        Utilisé lorsque le servant est mort (hp <= 0)
        """
        self.servantsOnBoard.remove(servant)
        
    def removeItemFromBoard(self, item):
        """
        Fonction retirant un card autre que Servant passée en paramètre
        Utilisé lorsque l'item n'est plus equipé/ lorsqu'il est utilisé
        """
        self.itemOnBoard.remove(item)
       
    def setCanFightForServantsOnBoard(self):
        for servant in self.servantsOnBoard:
            servant.canAttack = True

    def getServantsCanFight(self):
        "Fonction qui retourne uen liste de tout les serviteurs pouvant attaquer l'adveraire ou ses seerviteurs"
        lstServantCanFight = [servant for servant in self.servantsOnBoard if servant.canFight]
        return lstServantCanFight
        
    def hasLoose(self):
        """
        Fonction qui vérifie si le joueur a perdu la partie
            -->Si il n'a plus de point de vit
            -->Si il n'a plus de card à piocher
        Retourne Vrai si perdu, Faux sinon
        """
        if self.lifePoint <= 0:
            return True
        
        if self.deck.qsize() <= 0:
            return True
        
        return False
