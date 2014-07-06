# -*- coding : utf-8 -*-

class Card:
    """
    Classe mère pour Serviteur et Item
    """
    
    def __init__(self, params):
        self.idCard = params.get("idCard")
        self.name = params.get("Name")
        self.description = params.get("Desc")
        self.cost = params.get("Cost")
        
    def destroyCard(self):
        print(self.name, " goes to the card graveyard")
        
    def __str__(self):
        return "Name : " + self.name + ", Desc : " + self.description + ", Coût : " + str(self.cost) + "\n"
