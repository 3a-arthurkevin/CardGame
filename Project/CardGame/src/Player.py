# -*- coding : utf-8 -*-

import queue
import random
import copy

class Player:
    
    totalCardIntoDeck = 20
    
    def __init__(self, namePlayer):
        self.name = namePlayer
        self.lifePoint = 10
        self.maxCardInHand = 5
        self.hand = [] #* self.maxCardInHand 
        self.cardsList = []
        self.deck = queue.Queue()
        
        self.maxCardInBoardForServant = 3
        self.maxCardInBoardForItem = 3
        self.servantsOnBoard = [None] * self.maxCardInBoardForServant
        self.itemOnBoard = [None] * self.maxCardInBoardForItem
        
        self.mana = 0
        
    def displayHand(self):
        if(len(self.hand) <= 0):
            print("Aucune Carte en main")
        else:
            for card in self.hand:
                print("-----")
                print(card)
                print("-----")
    
    def useMana(self, manaValue):
        self.mana -= manaValue
    
    def addManaForPlayerTurn(self):
        """
        Action appelée à chaque debut de tour d'un joueur
        Renouvellement du mana pour utiliser les cartes
        """
        self.mana = 4 
    
    def putWeaponOnBoard(self, weapon, slotToPut):
        self.itemOnBoard[slotToPut] = weapon
        self.hand.remove(weapon)
    
    def createDeck(self, cardsList):
        """
        Fonction qui demande à l'utilisateur de constituer son deck
        Remplit le tableau cardList des cartes choisi par l'utilisateur
        """
        
        if len(cardsList) <= 0:
            print("CardList empty")
            return False
        
        print("Création du deck du joueur : ", self.name)
        print("Choississez entre les 3 cartes proposées jusqu'à arriver à un total de ", Player.totalCardIntoDeck , " cartes dans votre deck\n")
        
        while len(self.cardsList) < self.totalCardIntoDeck:
            cards = []
            print(Player.totalCardIntoDeck - len(self.cardsList), " cartes restante à choisir \n")
            
            for i in range(3):
                cards.append(cardsList[random.randint(0, len(cardsList)-1)])
                print(i+1, ")", cards[i])
                print("-----")
            
            validChoose = False
            choose = 0
            
            while not validChoose:
                try:
                    choose = int(input("Quelle carte avez vous choisit ? \n"))
                except ValueError:
                    choose = 0
                    
                if choose >= 1 and choose <= 3:
                    validChoose = True
                else:
                    print("Choix invalide")
            
            self.cardsList.append(copy.deepcopy(cards[choose-1]))
        
        return True
    
    def takeCardFromDeck(self):
        """
        Pioche une carte dans le deck 
        si il y en reste
        si le joueur n'a pas atteint la limite de carte en main maximum
        """
        
        if self.deck.qsize() <= 0:
            return False
        
        if(not self.findFreeSlotInHand()):
            del self.hand[len(self.hand)-1]
        
        self.hand.append(self.deck.get())     
            
        return True
    
    def drawCardForBegining(self):
        """
        Fonction appelé en debut de partie
        Fait piocher 3 cartes au joueur en début de partie
        """
        for i in range(3):
            self.takeCardFromDeck()
        
    
    def countServantOnBoard(self):
        i = 0
        for elem in self.servantsOnBoard:
            if(elem != None):
                i += 1
        return i
    
    def countItemOnBoard(self):
        i = 0
        for elem in self.itemOnBoard:
            if(elem != None):
                i += 1
        return i
    
    def getServantOnBoard(self):
        lstServantOnBoard = []
        for elem in self.servantsOnBoard:
            if(elem != None):
                lstServantOnBoard.append(elem)
        return lstServantOnBoard
            
    def getItemOnBoard(self):
        lstItemOnBoard = []
        for elem in self.itemOnBoard:
            if(elem != None):
                lstItemOnBoard.append(elem)
        return lstItemOnBoard
        
    def putServantInBoard(self, cardServant):
        """
        Fonction qui pose un serviteur sur le terrain si il y a un emplacement libre
        """ 
        i = self.findFreeSlotForServant()
        if(i >= 0):
            self.servantsOnBoard[i] = cardServant
            self.hand.remove(cardServant)
            return True
        return False
    
    def canPutItemInBoard(self):
        """
        Fonction qui regarde si il y a un emplacement libre sur le terrain pour utilier un item/weapon
        """ 
        i = self.findFreeSlotForItem()
        if(i >= 0):
            return True
        return False
    
    def putItemInBoard(self, cardItem):
        """
        Fonction qui utilise/equipe un item/weapon si il y a un emplacement libre sur le terrain
        """ 
        i = self.findFreeSlotForItem()
        if(i >= 0):
            self.itemOnBoard[i] = cardItem
            self.hand.remove(cardItem)
            return True
        return False
    
    def findFreeSlotInHand(self):
        """
        Fonction qui retourne Vrai si il y a de la place pour prendre un nouvelle carte dans sa main
        """
        if(len(self.hand) >= self.maxCardInHand):
            return False
        return True
    
    def findFreeSlotForServant(self):
        """
        Fonctions qui retourne l'index d'un emplacement libre (None) sur le plateau pour les servants
        """
        for i in range(len(self.servantsOnBoard)):
            if(self.servantsOnBoard[i] == None):
                return i
        return -1
    
    def findFreeSlotForItem(self):
        """
        Fonctions qui retoure l'index d'un emplacement libre (None) sur le plateau
        pour les card autre que Servant (Item et Weapon --> on pose les Weapons et les Items dans le même tableau)
        """
        for i in range(len(self.itemOnBoard)):
            if(self.itemOnBoard[i] == None):
                return i
        return -1
    

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
        index = self.findServantInBoard(servant)
        if(index >= 0):
            print("Point de vie restant à ", self.name, " : ", self.lifePoint , " - ", servant.level, " = ", self.lifePoint - servant.level)
            self.lifePoint -= servant.level
            self.servantsOnBoard[index] = None
            print("Serviteur parti au cimtière")
        else:
            print("Erreur, serviteur non présent sur le terrain")
    
    def findServantInBoard(self, servant):
        found = False
        sizeBoardServant = len(self.servantsOnBoard)
        i=0
        while(not found and i<sizeBoardServant):
            if(self.servantsOnBoard[i] == servant):
                return i
            i += 1
        return -1
    
    def removeItemFromBoard(self, item):
        """
        Fonction retirant un card autre que Servant passée en paramètre
        Utilisé lorsque l'item n'est plus equipé/ lorsqu'il est utilisé
        """
        index = self.findItemInBoard(item)
        if(index >= 0):
            self.itemOnBoard[index] = None
        else:
            print("Erreur, item non présent sur le terrain")
        
    def findItemInBoard(self, item):
        found = False
        sizeBoardItem = len(self.itemOnBoard)
        i=0
        while(not found and i<sizeBoardItem):
            if(self.itemOnBoard[i] == item):
                return i
            i += 1
        return -1
       
    def setCanFightForServantsOnBoard(self):
        """
        Fonction appelée à chaque debut de tour pour set la possibilité au serviteur sur le terrain d'attaquer
        """
        for servant in self.servantsOnBoard:
            if(servant != None):
                servant.canFight = True

    def getServantsCanFight(self):
        "Fonction qui retourne une liste de tous les serviteurs pouvant attaquer l'adveraire ou ses serviteurs"
        lstServantCanFight = []
        for elem in self.servantsOnBoard:
            if(elem != None):
                if(elem.canFight):
                    lstServantCanFight.append(elem)
        return lstServantCanFight
        
    def hasLoose(self, enemyName):
        """
        Fonction qui vérifie si le joueur a perdu la partie
            -->Si il n'a plus de point de vit
            -->Si il n'a plus de card à piocher
        Retourne Vrai si perdu, Faux sinon
        """
        if self.lifePoint <= 0:
            print(self.name, "n'a plus de point de vie ! \nVictoire de", enemyName)
            return True
        if self.deck.qsize() <= 0:
            print(self.name, "n'a plus de carte dans son deck ! \nVictoire de", enemyName)
            return True
        
        return False
