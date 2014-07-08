# -*- coding : utf-8 -*-

class Card:
    """
    Classe mère pour Serviteur et Item
    """
    
    def __init__(self, params):
        """
        Informations définissant une carte
        """
        self.idCard = params.get("idCard")
        self.name = params.get("Name")
        self.description = params.get("Desc")
        self.cost = params.get("Cost")
        
    def destroyCard(self):
        """
        Indication que la carte est envoyé au cimtière
        -->(lors d'un destroy, la carte n'est plus présente dans la main ou dans le plateau == innacessible)
        """
        print(self.name, " goes to the card graveyard")
        
    def __str__(self):
        return "Name : " + self.name + ", Desc : " + self.description + ", Coût : " + str(self.cost) + "\n"
