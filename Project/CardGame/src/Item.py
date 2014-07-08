# -*- coding : utf-8 -*-

from Utils.Enum import enum
from Card import *

"""
PLus besoin du Type item dans ce cas la ? comme on a que des objets qui modifient les stats
"""

ItemType = enum(
    "ItemType",
    "BOOSTER", "WEAPON"
    )

class Item(Card):
    
    def __init__(self, params):
        """
        Information utilise à un item
        """
        Card.__init__(self, params)
        
    def useItem(self, servant):
        """
        Fonction qui ajoute les effets de l'objet sur un servant passé en paramètre
        """
        servant.stats.hp += self.stats.hp
        servant.stats.strength += self.stats.strength
        servant.stats.intelligence += self.stats.intelligence
        servant.stats.precision += self.stats.precision
        servant.stats.speed += self.stats.speed
        servant.stats.defense += self.stats.defense
        servant.stats.resistance += self.stats.resistance
        servant.stats.critical += self.stats.critical

        
    def __str__(self):
        return Card.__str__(self) + self.stats.__str__()
