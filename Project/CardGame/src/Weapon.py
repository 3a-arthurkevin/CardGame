# -*- coding : utf-8 -*-

from Utils.Enum import enum
from Card import *

"""
Enumération des type d'arme disponible dans le jeu
"""
WeaponType = enum("WeaponType",
                  "SWORD", "AXE", "LANCE", "BOW", "EMAGIC", "LMAGIC", "NONE")


"""
Nom des arme associé à leurs type
"""
dicWeaponToString = {WeaponType.SWORD   : "Epée",
                     WeaponType.AXE     : "Hache",
                     WeaponType.LANCE   : "Lance",
                     WeaponType.BOW     : "Arc",
                     WeaponType.EMAGIC  : "Magie élémantaire",
                     WeaponType.LMAGIC  : "Magie blanche"}

class Weapon(Card):
    
    def __init__(self, params):
        """
        Information qualifiant une armes
        """
        Card.__init__(self, params)
        self.durability = params.get("Durability")
        self.weaponType = params.get("WeaponType")
        
    def useWeapon(self):
        """
        Réduit la durabilité d'une arme
        """
        self.durability -= 1
        
    def __str__(self):
        """
        fonction d'affichage des infos d'une arme
        """
        return Card.__str__(self) + self.stats.__str__() + "\nDurabilité : " + str(self.durability)