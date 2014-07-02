# -*- coding : utf-8 -*-

class Stats:
    '''
    Classe representant des statistiques
    
    Utilisation des stats lors des combats entre servant (sans prendre en compte l'ajout de stat des objets/armes)
        hp            : 10 --> 30  (pas de post traitement)
        strength      : 1  --> 10  (pas de post traitement)
        intelligence  : 1  --> 10  (pas de post traitement)
        precision     : 1  --> 10  (1pts == 10% <--> 10pts == 100%) % de touche
        speed         : 1  --> 10  (1pts == 4%  <--> 10pts == 40%)  % d'esquiver
        defense       : 1  --> 10  (pas de post traitement)
        resistance    : 1  --> 10  (pas de post traitement)
        critical      : 1  --> 10  (pas de post traitement)
    
    Le précision représente le % de toucher un servant,
        on y retire le % de vitesse de l'adversaire pour prendre en compte son esquive
        (à cela s'ajoute les stats de l'arme equip� si il y a et aussi du bonus/malus de l'arme adverse)
    Avec un traitemenr spécial selon la stat (à tweeker si pas top)
    '''

    def __init__(self, params = {}):
        '''
        Constructor
        '''
        self.hp = params.get("hp", 0)
        self.strength = params.get("str", 0)
        self.intelligence = params.get("int", 0)
        self.precision = params.get("pre", 0)
        self.speed = params.get("spe", 0)
        self.defense = params.get("def", 0)
        self.resistance = params.get("res", 0)
        self.critical = params.get("cri", 0)
        
    def __str__(self):
        return  "hp : "  + str(self.hp)             + " | " + \
                "atk : " + str(self.strength)       + " | " + \
                "int : " + str(self.intelligence)   + " | " + \
                "pre : " + str(self.precision)      + " | " + \
                "spe : " + str(self.speed)          + " | " + \
                "def : " + str(self.defense)        + " | " + \
                "res : " + str(self.resistance)     + " | " + \
                "cri : " + str(self.critical)
        
if __name__ == '__main__':
    print("éà@ù%$£*è")
        