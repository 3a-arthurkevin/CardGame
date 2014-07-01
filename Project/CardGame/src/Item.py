# -*- coding : utf-8 -*-
# -*- coding: iso-8859-1 -*-

from Utils import *
from Stats import Stats

ItemType = enum(
    "ItemType",
    "POTION", "WEAPON", "BOOSTER"
    )

class Item:
    
    def __init__(self):
        self.stats = Stats()