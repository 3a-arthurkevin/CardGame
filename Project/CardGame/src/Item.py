# -*- coding : utf-8 -*-

from Utils import *
from Stats import Stats

ItemType = enum(
    "ItemType",
    "POTION", "WEAPON", "BOOSTER"
    )

class Item:
    
    def __init__(self):
        self.stats = Stats()