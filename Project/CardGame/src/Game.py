# -*- coding : utf-8 -*-

from Utils import Config
from Player import Player
from Servant import Servant
from Item import Item
from Weapon import Weapon
import random

class Game:
    '''
    La classe Game représente une partie de jeu
    Elle s'occupe de l'instanciation des player et de lancer les actions relative au jeu (Tour, création de deck)
    '''


    def __init__(self, params):
        '''
        Initialisation d'une partie
        Création des player
        '''
        self.config = Config.loadConfig()
        self.cards = []
        self.setupCard()

        self.players = [Player(params.get("playerName1")), Player(params.get("playerName2"))]
        
        self.setupPlayer(self.players[0])
        self.setupPlayer(self.players[1])
        self.setupDeck()
    
    def setupCard(self):
        cards = self.config.get("Cards")
        
        for jsonCard in cards:
            if jsonCard["TypeCard"] == "Servant":
                self.cards.append(Servant(jsonCard))
                
            elif jsonCard["TypeCard"] == "Item":
                self.cards.append(Item(jsonCard))
            
            elif jsonCard["TypeCard"] == "Weapon":
                self.cards.append(Weapon(jsonCard))    
        
        return
    
    def setupPlayer(self, player):
        print("Création du joueur : ", player.name)
        
        choose = input("Voulez-vous utiliser un deck existant ? (Y/N)")
        
        if choose == "Y":
            deck = self.getDeck()
            
            if deck != None:
                player.cardsList = deck
                return
            
            else:
                print("Error lors de la récupération d'un deck existant")
        
        
        if choose != "N" and choose != "Y":
            print("Choix invalide")
            
        print("Création d'un nouveau deck")
        
        player.createDeck(self.cards)
        
        choose = input("Voulez-vous sauvegarder votre deck ? (Y/N)")
        
        if choose == "Y":
            self.saveDeck(player)
            return
        
        elif choose != "N":
            print("Choix invalide")
            
        print("Le deck ne sera pas sauvegardé")
        return
    
    def getDeck(self):
        
        self.deck = self.config.get("Decks", None)
        
        if len(self.deck) <= 0:
            return None
        
        deckName = input("Quel deck voulez-vous charger ?")
        
        jsonDeck = [ deck for deck in self.deck if deck["Name"] == deckName ]
        deck = []
        
        if len(jsonDeck) >= 1:
            jsonDeck = jsonDeck[0]
            for idCard in jsonDeck["CardList"]:
                card = [c for c in self.cards if c.idCard == idCard]
                deck.append(card)
                
        if len(deck) == Player.totalCardIntoDeck:
            return deck
        
        else:
            print("Nombre de carte insufisante dans le deck")
            
        return None
    
    def saveDeck(self, player):
        
        if len(player.cardsList) < Player.totalCardIntoDeck:
            print("Le nombre de carte dans le deck du joueur n'est pas suffisant")
            return False
        
        cardList = [ card.idCard for card in player.cardsList ]
        deckName = input("Choisissez le nom de votre deck : ")
        decks = self.config["Decks"]
        
        deck = [ deck for deck in decks if deck["Name"] == deckName ]
        
        if len(deck) <= 0:
            decks.append({"Name":deckName, "CardList" : cardList})
        else:
            deck[0]["CardList"] = cardList
        
        Config.saveConfig(self.config)
        
        return True
    
    def setupDeck(self):
        for player in self.players:
            while len(player.cardsList) > 0:
                cardRandom = random.randint(0, len(player.cardsList) - 1)
                player.deck.put(player.cardsList[cardRandom])
                del player.cardsList[cardRandom]
    
    def loop(self):
        '''Chaque appel de cette fonction fait avancer la partie d'un tour pour chaque joueur
        retourne un booleen si le tour a mis fin a la partie
        '''            
        
        self.turn(self.players[0], self.players[1])
        if self.players[0].hasLoose() or self.players[1].hasLoose():
            return False
        
        self.turn(self.players[1], self.players[0])
        if self.players[0].hasLoose() or self.players[1].hasLoose():
            return False
        
        return True
    
    def turn(self, mainPlayer, attackablePlayer):
        '''Fait jouer le joueur mainPlayer face à playerAttackable
        Plusieurs action sont réalisé a la suite:
        Player pioche une carte
        puis attente du choix de l'action
        La player peut poser une carte sur le board, attaquer l'autre player avec ces serviteurs
        '''
        
        print(mainPlayer.name, " à vous de jouer")
        
        if not mainPlayer.takeCardIntoDeck():
            print(mainPlayer.name , " n'a plus de carte dans son deck !")
            return
        
        print("vous avez tiré la carte :", mainPlayer.hand[len(mainPlayer.hand) - 1])
        
        putCardMode = True
        attackMode = False
        endTurn = False
        
        mainPlayer.addManaForPlayerTurn()
        
        while not endTurn:
            putCardMode = True
            attackMode = False
            endTurn = False
            
            while(putCardMode):
                print("""Quel action voulez vous faire :
                      0) Voir la main
                      1) Poser une carte
                      2) Passer à l'attaquer
                      3) Mettre fin au tour
                      """)
                choice = int(input("Choix : "))
                
                if choice == 0:
                    mainPlayer.displayHand()
                elif choice == 1:
                    self.putCard(mainPlayer)
                elif choice == 2:
                    attackMode = True
                    putCardMode = False
                elif choice == 3:
                    endTurn = True
                else:
                    print("Choix invalide")
            
            while(attackMode):
                print("""Quel action voulez vous faire :
                      1) Attaquer un serviteur
                      2) Attaquer l'adversaire
                      3) Mettre fin au tour
                      """)
                choice = int(input("Choix : "))
                
                if choice == 1:
                    self.attackServant(mainPlayer, attackablePlayer)
                elif choice == 2:
                    self.attackPlayer(mainPlayer, attackablePlayer)
                elif choice == 3:
                    endTurn = True
                else:
                    print("Choix invalide")
            
    def putCard(self, player):
        if(player.mana <= 0):
            print("Vous n'avez pas assez de mana pour poser des cartes")
            return
        nbCardInHand = len(player.hand)
        
        print("Quelle carte voulez vous poser ?")
        print("-1) Annuler l'action")
        for i in range(nbCardInHand):
            print(i+1,")", " poser ", player.hand[i].name)
        
        choice = int(input("Choix : "))
        
        if(choice == -1):
            return
        elif(choice >= 1 and choice <= nbCardInHand):
            
            if(type(player.hand[choice-1]) is Servant):
                if(player.putServantInBoard(player.hand[choice-1])):
                    print("Serviteur posé sur le terrain")
                else:
                    print("Impossible de poser plus de Serviteur sur le terrain")
            
            elif(type(player.hand[choice-1]) is Item):
                item = player.hand[choice-1]
                if(player.putItemInBoard(player.hand[choice-1])):
                    print("Item utilisé")
                    player.removeItemFromBoard(item)
                else:
                    print("Plus assez de place pour utiliser un item")
            
            elif(type(player.hand[choice-1]) is Weapon):
                slotIndex = player.findFreeSlotForItem()
                
                if(slotIndex >= 0):
                    
                    if(len(player.servantsOnBoard) > 0):
                        nbServantOnBoard = len(player.servantsOnBoard) 
                        print("-1) Annuler l'action")
                        for i in range(nbServantOnBoard):
                            print(i+1,")", " utiliser ", player.servantsOnBoard[i].name)
                        servantChoice = int(input("Choix"))
                        
                        if(servantChoice == -1):
                            return
        
                        elif(servantChoice >= 1 and servantChoice <= nbServantOnBoard):
                            if(player.servantsOnBoard[servantChoice-1].weaponType == player.hand[choice-1].weaponType):
                                weapon = player.hand[choice-1]
                                player.findFreeSlotForItem(weapon)
                                player.servantsOnBoard[servantChoice-1].equipWeapon(weapon)
                                print("Arme équipée")
                            elif(player.servantsOnBoard[servantChoice-1].weaponEquipped != None):
                                print("Ce servant a deja une arme d'équipée")
                            else:
                                ("Ce servant ne peux pas équiper ce type arme")
                        
                        else:
                            print("Choix invalide")
                            
                    else:
                        print("Impossible d'équiper une arme si aucun servant se trouve sur le terrain")
                else:
                    print("Plus assez de place sur le terrain pour équiper une arme")
        
        else:
            print("Choix invalide")
        return
        
    """
    récupérer la liste des servant canAttack du mainPlayer
    et traiter avec
    """
    def attackServant(self, mainPlayer, attackablePlayer):
        
        nbServantAttackable = len(attackablePlayer.servantsOnBoard)
        
        if(nbServantAttackable <= 0):
            print("Le joueur adverse n'a aucun serviteur sur le terrain")
            return
        else:
            lstServantUsable = mainPlayer.getServantsCanFight()
            nbServantMain = len(lstServantUsable)
            
            print("Choisir un servant pour attaquer")
            if(nbServantMain > 0):
                print("-1) Annuler l'action")
                for i in range(nbServantMain):
                    print(i+1, ") utiliser ", mainPlayer.servantsOnBoard[i].name)
                servantAttacker = int(input("Choix : "))
                
                if(servantAttacker == -1):
                    return
                
                elif(servantAttacker >= 1 and servantAttacker <= nbServantMain):
                    print("Choisir un servant avec qui attaquer : ")
                    print("-1) Annuler Action")
                    for i in range(nbServantMain):
                        print(i+1, ") ", lstServantUsable[i].name)
                    choiceServantAttacker = int(input("Choix : "))
                    
                    if(choiceServantAttacker == -1):
                        return
                    
                    elif(choiceServantAttacker >= 1 and choiceServantAttacker <= nbServantMain):
                        lstServantAttackable = attackablePlayer.servantsOnBoard
                        nbServantMain = len(lstServantAttackable)
                        
                        print("Choisir un serviteur ennemi à attaquer : ")
                        print("-1) Annuler action")
                        for i in range(nbServantAttackable):
                            print(i+1, ") Attaquer ", lstServantAttackable[i].name)
                        choiceServantToAttack = int(input("Choix : "))
                        
                        if(choiceServantToAttack == -1):
                            return
                        elif(choiceServantToAttack >= 1 and choiceServantToAttack <= nbServantAttackable):
                            servantAttacker = lstServantUsable[choiceServantAttacker-1]
                            servantAttacked = lstServantAttackable[choiceServantToAttack-1]
                            
                            servantAttacker.battleBetweenServant(servantAttacked)
                            
                            if(servantAttacker.weaponEquipped):
                                if(not servantAttacker.checkWeapon()):
                                    mainPlayer.removeItemFromBoard(servantAttacker.weaponEquipped)
                                    servantAttacker.weaponEquipped = None
                            if(servantAttacker.stats.hp <= 0):
                                mainPlayer.removeServantFromBoard(servantAttacker)
                             
                            if(servantAttacked.weaponEquipped):
                                if(not servantAttacked.checkWeapon()):
                                    attackablePlayer.removeItemFromBoard(servantAttacked.weaponEquipped)
                                    servantAttacked.weaponEquipped = None
                            if(servantAttacked.stats.hp <= 0):
                                attackablePlayer.removeServantFromBoard(servantAttacked)

                        else:
                            print("Choix invalide")
                            return
                    
                    else:
                        print("Choix invalide")
                        return
                
                else:
                    print("Choix invalide")
                    return
            else:
                print("Aucun servant sur le plateau peut attaquer")
                return

        return
    
    def attackPlayer(self, mainPlayer, attackablePlayer):
        
        return
    
if __name__ == "__main__":
    game = Game({"playerName1":"arthur", "playerName2":"kevin"})
    
    game.loop()
    
    
