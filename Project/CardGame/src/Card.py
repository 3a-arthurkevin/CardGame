# -*- coding : utf-8 -*-

class Card:
    """
    Classe mere pour Serviteur et Item
    """
    
    def __init__(self, params):
        self.name = params.get("name")
        self.description = params.get("description")
        self.cost = params.get("cost")
        
    def destroyCard(self):
        print("destroy")    
