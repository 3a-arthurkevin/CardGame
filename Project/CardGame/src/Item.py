# -*- coding : utf-8 -*-

from Utils.Enum import enum
from Stats import Stats
from Card import *

ItemType = enum(
    "ItemType",
    "POTION", "WEAPON", "BOOSTER"
    )

class Item(Card):
    
    def __init__(self, params):
        Card.__init__(self, params)
        self.stats = Stats(params)
        
    def __str__(self):
        return Card.__str__(self) + self.stats.__str__()