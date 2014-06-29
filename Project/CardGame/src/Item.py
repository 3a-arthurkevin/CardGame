def enum(enumName, *listValueNames):
    listValueNumbers = range(len(listValueNames))
    dictAttrib = dict( zip(listValueNames, listValueNumbers) )
    dictReverse = dict( zip(listValueNumbers, listValueNames) )
    dictAttrib["dictReverse"] = dictReverse
    return type(enumName, (), dictAttrib)


ItemType = enum(
    "ItemType",
    "POT", "WEAPON", "BOOSTER"
    )

class Item:
    
    def __init__(self):
        self.stats = 0