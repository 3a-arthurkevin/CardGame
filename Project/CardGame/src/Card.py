# -*- coding : utf-8 -*-

class Card:
    """
    Classe mère pour Serviteur et Item
    """
    
    def __init__(self, params):
        self.idCard = params.get("idCard")
        self.name = params.get("name")
        self.description = params.get("description")
        self.cost = params.get("cost")
        
    def destroyCard(self):
        print("destroy")
        
    def __str__(self):
        return "Name : " + self.name + ", Desc : " + self.description + ", Coût : " + str(self.cost)
