# -*- coding : utf-8 -*-

from Card import Card
from Stats import Stats

class Servant(Card):
    """
    Derive de Card 
    Classe reprsesentant les serviteurs a invoquer qui pourront attaquer l'adversaire et ses serviteurs 
    """
    
    def __init__(self, parameters = {}):
        Card.__init__(self, parameters.get("name"), parameters.get("description"), parameters.get("cost"))
        self.stats = Stats(parameters.get("hp"),
                           parameters.get("str"),
                           parameters.get("int"),
                           parameters.get("pre"),
                           parameters.get("spe"),
                           parameters.get("def"),
                           parameters.get("res"),
                           parameters.get("cri"))
        self.level = 1
        #level max pour unité de base = 2 --> si classe up, level 3 et level max = 4
        self.experience = 0

        
    def fight(self, servant):
        print("attack")

    def gainExperience(self, servant):
        print("Exp up")
        if(self.level == 1 and self.experience == 100):
            self.levelUp()
        
        
    def levelUp(self):
        self.stats.hp += 1
        self.stats.strength += 1
        self.stats.intelligence += 1
        self.stats.precision += 1
        self.stats.speed += 1
        self.stats.defense += 1
        self.stats.resistance += 1
        self.stats.critical += 1
        
        self.experience = 101