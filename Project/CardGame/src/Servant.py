# -*- coding : utf-8 -*-

from Utils import *
from Card import Card
from Stats import Stats

ClassType = enum(
    "Class",
    "SWORDMASTER", "WARRIOR", "HALBARDIER", "ARCHER", "PEGASUS", "MAGE", "PRIEST"
    )

class Servant(Card):
    """
    Derive de Card 
    Classe reprsesentant les serviteurs a invoquer qui pourront attaquer l'adversaire et ses serviteurs 
    """
    
    def __init__(self, params):
        Card.__init__(self, params.get("name"), params.get("description"), params.get("cost"))
        self.stats = Stats(params.get("hp"),
                           params.get("str"),
                           params.get("int"),
                           params.get("pre"),
                           params.get("spe"),
                           params.get("def"),
                           params.get("res"),
                           params.get("cri"))
        self.level = params.get("level")
        self.experience = 0
        self.classType = params.get("classType")

        
    def battleBetweenServant(self, servant):
        self.attack(servant)
        
    def attack(self, servant):
        self.applyDamage(servant)
        self.applyDamage(self)
        
    def applyDamage(self, servant):
        print('applyDamage')

    def applyWeekness(self, servant):
        if(self.classType == "SWORDMASTER" and servant.classType == "WARRIOR"):
            
    
    def gainExperience(self, servant):
        print("Exp up")
        if(self.level == 1 and self.experience >= 100):
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
        
        self.experience = 100
        self.level = 2