# -*- coding : utf-8 -*-

import copy
import random

from Card import Card
from Item import Item
from Player import Player
from Servant import Servant
from Utils import Config
from Utils.CleanScreen import cleanScreen
from Weapon import Weapon
from goto import goto, label  # Trololololol


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
        self.useGoto = False
        self.config = Config.loadConfig()
        self.cards = []
        self.setupCard()

        self.players = [Player(params.get("playerName1")), Player(params.get("playerName2"))]
        
        self.setupPlayer(self.players[0])
        self.setupPlayer(self.players[1])
        self.setupDeck()
    
    def setupCard(self):
        """
        Création de la liste des cartes disponible dans le jeu
        """
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
        """
        Création du deck du joueur.
        Deux possibilité possible
        Création d'un deck en choississant chaque carte qui le composera.
        Récupération d'un deck stocké dans le fichier de configuration
        """
        
        cleanScreen()
        print("Création du joueur : ", player.name)
        
        try:
            choose = int(input("""Que voulez vous faire ?
            1) Charger un deck existant
            2) Choisir chaque carte de son deck
            3) Laisser notre super algorithme de la mort qui tue construire un deck imbattable pour vous
            """))
        except:
            choose = -1
        
        if choose == 1:
            deck = self.getDeck()
            
            if deck != None:
                player.cardsList = deck
                return
            
            else:
                print("Error lors de la récupération d'un deck existant")
                
        elif choose == 3:
            deck = self.getRandomDeck()
            
            if deck != None:
                player.cardsList = deck
                if self.useGoto:
                    goto .tyrionIsDead
                else:
                    self.chooseSaveDeck(player)
            
            else:
                print("Error lors de la génération aléatoire du deck")
        
        if choose != 2:
            print("Erreur dans la saisie du choix")
        
        print("Création d'un nouveau deck")
        player.createDeck(self.cards)
        
        
        if self.useGoto:
            label .tyrionIsDead
            try:
                choose = input("Voulez-vous sauvegarder votre deck ? (Y/N)")
            except:
                choose = -100
        
            if choose == "Y":
                self.saveDeck(player)
                return
        
            elif choose != "N":
                print("Choix invalide")
            
                print("Le deck ne sera pas sauvegardé")
                
        else:
            self.chooseSaveDeck(player)
               
        return
    
    def getRandomDeck(self):
        """
        Créer un deck aléatoire pour le joueur
        """
        deck = []
        
        for i in range(Player.totalCardIntoDeck):
            deck.append(copy.deepcopy(self.cards[random.randint(0, len(self.cards) - 1)]))
        
        return deck
    
    def getDeck(self):
        """
        Récupère le deck dans le fichier de configuration en fonction du nom du deck
        Si le deck récupéré comporte des erreurs la fonction retourne None
        """
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
                if len(card) > 0:
                    deck.append(copy.deepcopy(card[0]))
                
        if len(deck) == Player.totalCardIntoDeck:
            return deck
        
        else:
            print("Erreur dans le deck")
            
        return None
    
    def chooseSaveDeck(self, player):
        try:
            choose = input("Voulez-vous sauvegarder votre deck ? (Y/N)")
        except:
            choose = -100
        
        if choose == "Y":
            self.saveDeck(player)
            return
        
        elif choose != "N":
            print("Choix invalide")
            
        print("Le deck ne sera pas sauvegardé")
        return
    
    def saveDeck(self, player):
        """
        Sauvegarde du deck dans le fichier de configuration
        Le deck sauvegardé est associé à un nom
        Si le nom est déjà présent dans le fichier de configuration le deck est écrasé 
        """
        
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
        cleanScreen()
        self.turn(self.players[0], self.players[1])
        if self.players[0].hasLoose(self.players[1].name) or self.players[1].hasLoose(self.players[0].name):
            return False
        
        cleanScreen()
        self.turn(self.players[1], self.players[0])
        if self.players[0].hasLoose(self.players[1].name) or self.players[1].hasLoose(self.players[0].name):
            return False
        
        return True
    
    def turn(self, mainPlayer, attackablePlayer):
        '''Fait jouer le joueur mainPlayer face à playerAttackable
        Plusieurs action sont réalisé a la suite:
        Player pioche une carte
        puis attente du choix de l'action
        La player peut poser une carte sur le board, attaquer l'autre player avec ces serviteurs
        '''
        
        print("_____________________________\n")
        print(mainPlayer.name, " à vous de jouer")
        
        if(not mainPlayer.takeCardFromDeck()):
            print(mainPlayer.name, " n'a plus de carte dans son deck !")
            return
        
        
        mainPlayer.addManaForPlayerTurn()
        
        mainPlayer.setCanFightForServantsOnBoard()
        
        card = mainPlayer.hand[len(mainPlayer.hand) - 1]
        #card.destroyCard()

        print("vous avez tiré la carte :\n", card)
        
        putCardMode = True
        attackMode = False
        endTurn = False
        
        #Debut boucle
        while not endTurn:
            putCardMode = True
            attackMode = False
            endTurn = False
            
            #Mode poser ses cartes
            while(putCardMode):
                print("\n---- MODE POSAGE DE CARTE ----\n")
                print("Mana restant : ", mainPlayer.mana, "\n"), 
                print("""Quel action voulez vous faire : 
                -1) Voir le terrain
                0) Voir la main
                1) Poser une carte sur le terrain
                2) Passer en mode attaquer
                3) Mettre fin au tour""")
                
                try:
                    choice = int(input("Choix : "))
                except:
                    choice = -100
                
                cleanScreen()
                
                if(choice == -1):
                    self.seeBoard(mainPlayer, attackablePlayer)
                elif choice == 0:
                    mainPlayer.displayHand()
                elif choice == 1:
                    self.putCard(mainPlayer)
                elif choice == 2:
                    attackMode = True
                    putCardMode = False
                elif choice == 3:
                    endTurn = True
                    putCardMode = False
                else:
                    print("Choix invalide")
            
            #Mode attacquer
            while(attackMode):
                print("\n---- MODE ATTAQUE ----\n")
                print("Vos points de vie : ", mainPlayer.lifePoint)
                print("Point de vie de", attackablePlayer.name, " : ", attackablePlayer.lifePoint, "\n")
                print("""Quel action voulez vous faire :
                0) Voir le terrain
                1) Attaquer un serviteur
                2) Attaquer l'adversaire
                3) Mettre fin au tour""")
                try:
                    choice = int(input("Choix : "))
                except:
                    choice = -100
                
                cleanScreen()
                
                if(choice == 0):
                    self.seeBoard(mainPlayer, attackablePlayer)
                elif choice == 1:
                    if(self.attackServant(mainPlayer, attackablePlayer)):
                        return True
                elif choice == 2:
                    if(self.attackPlayer(mainPlayer, attackablePlayer)):
                        return True
                elif choice == 3:
                    endTurn = True
                    attackMode = False
                else:
                    print("Choix invalide")
            
    def putCard(self, player):
        """
        Pose une carte sur le terrain pour le player reçu en paramètre
        La fonction affiche la liste des carte dans la main
        Demande la carte a poser sur le board et vérifie si l'utilisateur peut posé la carte choisi
        """
        
        if(player.mana <= 0):
            print("Vous n'avez pas assez de mana pour poser des cartes")
            return
        
        nbCardInHand = len(player.hand)
        
        if(nbCardInHand <= 0):
            print("Vous n'avez plus de carte en main !")
            return
        
        print("Quelle carte voulez vous poser ?")
        print("-1) Annuler l'action")
        for i in range(nbCardInHand):
            if(player.hand[i] != None):
                print(i+1,")", " poser ", player.hand[i].name)
        
        try:
            choice = int(input("Choix : "))
        except:
            choice = -100
        
        if(choice == -1):
            return
        elif(choice >= 1 and choice <= nbCardInHand):
            
            if(player.hand[choice-1].cost <= player.mana):
                
                if(type(player.hand[choice-1]) is Servant):
                    self.putServant(player, choice-1)
                
                elif(type(player.hand[choice-1]) is Item):
                    self.putItem(player, choice-1)
                
                elif(type(player.hand[choice-1]) is Weapon):
                    self.putWeapon(player, choice-1)
            else:
                print("Vous n'avez pas assez de mana pour utiliser cette carte")
        
        else:
            print("Choix invalide")
        return
    
    def putServant(self, player, index):
        """
        Fonction prenant le player qui pose la carte et l'index de la carte à poser dans la main du joueur
        S'occupe de la procédure pour poser un serviteur sur le plateau
        """
        servant = player.hand[index]
        if(player.putServantInBoard(servant)):
            player.useMana(servant.cost)
            print("Serviteur posé sur le terrain")
        else:
            print("Impossible de poser plus de Serviteur sur le terrain")
            
    def putItem(self, player, index):
        """
        Fonction prenant le player qui pose la carte et l'index de la carte à poser dans la main du joueur
        S'occupe de la procédure pour poser un item sur le plateau
        """
        item = player.hand[index]
        lstServantOnBoard = player.getServantOnBoard()
        nbServantOnBoard = len(lstServantOnBoard)
        
        if(nbServantOnBoard <= 0):
            print("Impossible d'utiliser un item, aucun serviteur sur le terrain")
            return
            
        if(player.canPutItemInBoard()):
            
            print("Utiliser l'item sur : ")
            print("-1) Annuler l'action")
            
            for i in range(nbServantOnBoard):
                print(i+1,")", lstServantOnBoard[i].name)
            
            try:
                servantChoice = int(input("Choix : "))
            except:
                servantChoice = -100
                
            if(servantChoice == -1):
                return

            elif(servantChoice >= 1 and servantChoice <= nbServantOnBoard):
                player.putItemInBoard(item)
                item.useItem(lstServantOnBoard[servantChoice-1])
                player.useMana(item.cost)
                print("Item utilisé")
                player.removeItemFromBoard(item)
            else:
                print("Choix invalide")
        
        else:
            print("Pas de place sur le terrain pour utiliser un item")
            
    def putWeapon(self, player, index):
        """
        Fonction prenant le player qui pose la carte et l'index de la carte à poser dans la main du joueur
        S'occupe de la procédure pour équiper une amre sur un serviteur/poser carte arme sur le plateau
        """
        slotIndex = player.findFreeSlotForItem()
        
        if(slotIndex >= 0):
            lstServantOnBoard = player.getServantOnBoard()
            nbServantOnBoard = len(lstServantOnBoard)
            
            if(nbServantOnBoard > 0):
                print("Sur quel serviteur voulez vous équiper l'arme :")
                print("-1) Annuler l'action")
                for i in range(nbServantOnBoard):
                    print(i+1,")", " équiper sur ", lstServantOnBoard[i].name)
                    
                try:
                    servantChoice = int(input("Choix : "))
                except:
                    servantChoice = -100
                    
                if(servantChoice == -1):
                    return

                elif(servantChoice >= 1 and servantChoice <= nbServantOnBoard):
                    
                    weapon = player.hand[index]
                    servant = lstServantOnBoard[servantChoice-1]

                    if(servant.weaponEquipped != None):
                        print("Ce servant a deja une arme d'équipée")
                    elif(servant.weaponType == weapon.weaponType):
                        servant.equipWeapon(weapon)
                        player.putWeaponOnBoard(weapon, slotIndex)
                        player.useMana(weapon.cost)
                        print("Arme équipée")
                    else:
                        print("Ce servant ne peux pas équiper ce type arme")
                
                else:
                    print("Choix invalide")
                    
            else:
                print("Impossible d'équiper une arme si aucun servant se trouve sur le terrain")
        else:
            print("Plus assez de place sur le terrain pour équiper une arme")
        
    def attackServant(self, mainPlayer, attackablePlayer):
        """
        récupérer la liste des servant canAttack du mainPlayer
        et traiter avec
        """
        lstServantAttackable = attackablePlayer.getServantOnBoard()
        nbServantAttackable = len(lstServantAttackable)
        
        if(nbServantAttackable <= 0):
            print("Le joueur adverse n'a aucun serviteur sur le terrain")
            return
        else:
            lstServantUsable = mainPlayer.getServantsCanFight()
            nbServantMain = len(lstServantUsable)
            
            if(nbServantMain > 0):
                print("Choisir un servant pour attaquer")
                print("-1) Annuler l'action")
                for i in range(nbServantMain):
                    print(i+1, ") utiliser ", lstServantUsable[i].name)
                    
                try:
                    choiceServantAttacker = int(input("Choix : "))
                except:
                    choiceServantAttacker = -100
                
                if(choiceServantAttacker == -1):
                    return
                
                elif(choiceServantAttacker >= 1 and choiceServantAttacker <= nbServantMain):

                    print("Choisir un serviteur ennemi à attaquer : ")
                    print("-1) Annuler action")
                    for i in range(nbServantAttackable):
                        print(i+1, ") Attaquer ", lstServantAttackable[i].name)
                        
                    try:
                        choiceServantToAttack = int(input("Choix : "))
                    except:
                        choiceServantToAttack = -100
                    
                    if(choiceServantToAttack == -1):
                        return
                    elif(choiceServantToAttack >= 1 and choiceServantToAttack <= nbServantAttackable):
                        servantAttacker = lstServantUsable[choiceServantAttacker-1]
                        servantAttacked = lstServantAttackable[choiceServantToAttack-1]
                        
                        servantAttacker.battleBetweenServant(servantAttacked)
                            
                        self.weaponAndDeathManagerForServantAfterBattle(mainPlayer, attackablePlayer, servantAttacker)
                        self.weaponAndDeathManagerForServantAfterBattle(attackablePlayer, mainPlayer, servantAttacked)

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
    
    def weaponAndDeathManagerForServantAfterBattle(self, playerAttacker, playerAttacked, servant):
        """
        Fonction appelé à la fin d'un combat entre serviteurs prenant en paramètres 
            le joueur qui attaque, le joueur qui subit l'attaquet et le serviteur du premier joueur en paramètre
        appellant 2 fonctions qui appliquent l'usure de l'arme et sa destruction si elle n'a plus de durabilité
        et la mort si un serviteur n'a plus de point de vie à l'issue du combat 
        """
        self.weaponServantManagerAfterBattle(playerAttacker, servant)
        self.deathServantManagerForServantAfterBattle(playerAttacker, playerAttacked, servant)
    
    def weaponServantManagerAfterBattle(self, player, servant):
        """
        Fonction qui prend en paramètre un joueur et un de ses serviteur
        pour vérifier si le serviteur avait une arme équipé, et appliquer l'usure et/ou la cassure et l'enlever du terrain
        si une arme est bien équipée
        """
        if(not servant.checkWeapon()):
            player.removeItemFromBoard(servant.weaponEquipped)
            servant.unequippedWeapon()
            
    def deathServantManagerForServantAfterBattle(self, playerAttacker, playerAttacked, servant):
        """
        Fonction prenant en paramètre le joueur qui attaque, le joueur qui subit l'attaquer et le servant du 1er player en paramètre
        Elle vérifie les point de vie du serviteur sont à 0 ou moins à l'issue d'un combat
        Si oui, on retire le serviteur et on vérifie si le joueur a perdu la partie (à cause de la perte de point de vie à chaque servant qui meurt)
        """
        if(servant.stats.hp <= 0):
            playerAttacker.removeItemFromBoard(servant.weaponEquipped)
            playerAttacker.removeServantFromBoard(servant)
            if(playerAttacker.hasLoose(playerAttacked.name)):
                return True
        return
            
    def attackPlayer(self, mainPlayer, attackablePlayer):
        """
        Fonction qui fait attaquer attackablePlayer par mainPlayer
        La fonction fait les vérification de possibilité d'attquer (serviteur sur le board, ...)
        """
        if(attackablePlayer.countServantOnBoard() > 0):
            print("Impossible d'attaquer directement ", attackablePlayer.name, " car il est protegé par ses serviteurs !")
            return
        
        lstServantUsable = mainPlayer.getServantsCanFight()
        nbServantMain = len(lstServantUsable)
            
        if(nbServantMain > 0):
            print("Choisir un servant pour attaquer")
            print("-1) Annuler l'action")
            for i in range(nbServantMain):
                print(i+1, ") utiliser ", lstServantUsable[i].name)
            
            try:
                servantAttacker = int(input("Choix : "))
            except:
                servantAttacker = -100
            
            if(servantAttacker == -1):
                return
                
            elif(servantAttacker >= 1 and servantAttacker <= nbServantMain):
                lstServantUsable[servantAttacker-1].attackPlayer(attackablePlayer)
                self.weaponServantManagerAfterBattle(mainPlayer, lstServantUsable[servantAttacker-1])
                if(attackablePlayer.hasLoose(mainPlayer.name)):
                    return True
                return
                
            else:
                print("Choix invalide")
               
        else:
            print("Aucun servant sur le plateau peut attaquer")
            return

        return
    
    def seeBoard(self, mainPlayer, otherPlayer):
        """
        Fonction qui affiche les cartes se trouvant sur le terrain (le sien et celui de l'adversaire)
        """
        print("_____________________________")
        print("Terrain de ", mainPlayer.name)
        print("Serviteurs : ")
        for elem in mainPlayer.servantsOnBoard:
            if(elem != None):
                print("-----")
                print(elem)
                print("-----")
        print("Items : ")
        for elem in mainPlayer.itemOnBoard:
            if(elem != None):
                print("-----")
                print(elem)
                print("-----")
        print("_____________________________")
        print("Terrain de ", otherPlayer.name)
        print("Serviteurs : ")
        for elem in otherPlayer.servantsOnBoard:
            if(elem != None):
                print("-----")
                print(elem)
                print("-----")
        print("Items : ")
        for elem in otherPlayer.itemOnBoard:
            if(elem != None):
                print("-----")
                print(elem)
                print("-----")
        print("_____________________________")
        
        
    
if __name__ == "__main__":
    game = Game({"playerName1":"Arthur", "playerName2":"Kevin"})
    
    game.players[0].drawCardForBegining()
    game.players[1].drawCardForBegining()
    
    while(game.loop()):
        continue
    
    
    
