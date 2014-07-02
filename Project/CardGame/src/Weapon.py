# -*- coding : utf-8 -*-

from Utils.Enum import enum
from Stats import Stats
from Card import *

WeaponType = enum("WeaponType",
                  "SWORD", "AXE", "LANCE", "BOW", "EMAGIC", "LMAGIC", "NONE")

class Weapon(Card):
    
    def __init__(self, params):
        Card.__init__(self, params)
        self.stats = Stats(params)
        self.durability = params.get("durability")
        self.weaponType = params.get("weaponType")
        
    def useItem(self, servant):
        self.equipeItem(servant)
        
    def equipeItem(self, servant):
        """
        Fonction qui set l'arme equipé par le servant passé en paramètre
        Verification des armes que le servant peut equiper avant
        """
        if(servant.weaponType == self.weaponType):
            servant.equipeWeapon(self)
        else:
            print(servant.name, " can't equipe ", self.name)
            
    def useWeapon(self):
        self.durability -= 1