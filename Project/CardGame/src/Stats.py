# -*- coding : utf-8 -*-

class Stats:
    '''
    Classe representant des statistiques
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
        