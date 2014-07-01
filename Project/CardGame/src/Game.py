# -*- coding : utf-8 -*-

from Player import Player
from Utils import Config

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
        self.cards = self.config["Cards"]
        self.players = [Player(params.get("playerName1")), Player(params.get("playerName2"))]
    
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
        
        
        if choose != "N":
            print("Choix invalide")
            
        print("Création d'un nouveau deck")
        
        player.createDeck()
        
        choose = input("Voulez-vous sauvegarder votre deck ? (Y/N)")
        
        if choose == "Y":
            self.saveDeck(player)
            return
        
        elif choose != "N":
            print("Choix invalide")
            
        print("Le deck ne sera pas sauvegardé")
        return
    
    def getDeck(self):
        
        self.deck = self.config["Deck"]
        
        if len(self.deck) <= 0:
            return None
        
        deckName = input("Quel deck voulez-vous charger ?")
        
        jsonDeck = [ deck for deck in self.deck if deck["Name"] == deckName ]
        deck = []
        if len(deck) >= 1:
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
        decks.append({"Name":deckName, "CardList" : cardList})
        
        #self.config["Decks"] = decks
        
        print(self.config["Decks"])
        
        return True
    
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
    
    def turn(self, mainPlayer, playerAttackable):
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
        
        endTurn = False
        
        while not endTurn:
            print("""Quel action voulez vous faire :
                  1) Poser une carte
                  2) Attaquer l'adversaire
                  3) Mettre fin au tour
                  """)
            choose = int(input("Choix : "))
            
            if choose == 1:
                self.putCard(mainPlayer)
            elif choose == 2:
                self.attackServant(mainPlayer, playerAttackable)
            elif choose == 3:
                endTurn = True
            else:
                print("Choix invalide")
            
    def putCard(self, player):
        print("putCard")
        return
    
    def attackServant(self, mainPlayer, attackablePlayer):
        print("Attack servant")
        return
    
if __name__ == "__main__":
    game = Game({"playerName1":"arthur", "playerName2":"kevin"})
    
    game.loop()
    
    
