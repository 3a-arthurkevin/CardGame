'''
Created on 29 juin 2014

@author: Kevin
'''

def enum(enumName, *listValueNames):
    listValueNumbers = range(len(listValueNames))
    dictAttrib = dict( zip(listValueNames, listValueNumbers) )
    dictReverse = dict( zip(listValueNumbers, listValueNames) )
    dictAttrib["dictReverse"] = dictReverse
    return type(enumName, (), dictAttrib)

# Remplacer par l'enum pour Item
Direction = enum(
    "Direction", #Nom de l'enum
    "UP", "DOWN", "LEFT", "RIGHT" # Valeur de l'enum
    )

class Item:
    
    def __init__(self):
        self.hp = 1