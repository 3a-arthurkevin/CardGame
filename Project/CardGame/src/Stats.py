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
        self.strong = params.get("strong", 0)
        self.intel = params.get("intel", 0)
        self.prec = params.get("prec", 0)
        self.speed = params.get("speed", 0)
        self.defence = params.get("def", 0)
        self.res = params.get("res", 0)
        self.crit = params.get("crit", 0)
        