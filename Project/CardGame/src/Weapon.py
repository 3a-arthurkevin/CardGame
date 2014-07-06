# -*- coding : utf-8 -*-

from Utils.Enum import enum
from Stats import Stats
from Card import *

WeaponType = enum("WeaponType",
                  "SWORD", "AXE", "LANCE", "BOW", "EMAGIC", "LMAGIC", "NONE")

dicWeaponToString = {WeaponType.SWORD   : "Epée",
                     WeaponType.AXE     : "Hache",
                     WeaponType.LANCE   : "Lance",
                     WeaponType.BOW     : "Arc",
                     WeaponType.EMAGIC  : "Magie élémantaire",
                     WeaponType.LMAGIC  : "Magie blanche"}

class Weapon(Card):
    
    def __init__(self, params):
        Card.__init__(self, params)
        self.stats = Stats(params)
        self.durability = params.get("Durability")
        self.weaponType = params.get("WeaponType")
        
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
        
    def __str__(self):
        return Card.__str__(self) + self.stats.__str__()