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
        
        self.players = [Player(params.get("playerName1")), Player(params.get("playerName2"))]
        
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
            strChoose = """Quel action voulez vous faire :
            1) Poser une carte
            2) Attaquer l'adversaire
            3) Mettre fin au tour
            """
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
    
    