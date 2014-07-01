# -*- coding : utf-8 -*-
# -*- coding: iso-8859-1 -*-

class Stats:
    '''
    Classe representant des statistiques
    
    Utilisation des stats lors des combats entre servant (sans prendre en compte l'ajout de stat des objets/armes)
        hp            : 10 --> 30  (pas de post traitement)
        strength      : 1  --> 10  (pas de post traitement)
        intelligence  : 1  --> 10  (pas de post traitement)
        precision     : 1  --> 10  (1pts == 10% <--> 10pts == 100%) % de touche
        speed         : 1  --> 10  (1pts == 5%  <--> 10pts == 50%)  % d'esquiver
        defense       : 1  --> 10  (pas de post traitement)
        resistance    : 1  --> 10  (pas de post traitement)
        critical      : 1  --> 10  (pas de post traitement)
    
    Le précision représente le % de toucher un servant,
        on y retire le % de vitesse de l'adversaire pour prendre en compte son esquive
        (à cela s'ajoute les stats de l'arme equipé si il y a et aussi du bonus/malus de l'arme adverse)
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
        