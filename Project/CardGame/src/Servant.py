# -*- coding : utf-8 -*-

from Utils import *
from Card import Card
from Stats import Stats

ClassType = enum("Class",
                 "SWORDMASTER", "WARRIOR", "HALBARDIER", "ARCHER", "PEGASUS", "MAGE", "PRIEST")

WeaponType = enum("Weapon",
                  "SWORD", "AXE", "LANCE", "BOW", "EMAGIC", "LMAGIC", "NONE")

"""
Définition des bonus malus directement pour simplifier le code
--> permet d'avoir moins de condition pour déterminer les bonus / malus
--> comme on a besoin de ces infos à chaque combat entre serviteurs autant les poser un fois pour toute
--> plus facile à maintenir en cas d'ajout et de retrait d'elements
--> mettre toutes les classes et armes pour ne pas à tester si une clé existe (en dehors du type NONE (jamais attribuer à une class ou arme))
"""

tabBonusBetweenWeapon = {WeaponType.SWORD   :  {"stronger" : WeaponType.AXE,     "weaker" : WeaponType.LANCE},
                         WeaponType.AXE     :  {"stronger" : WeaponType.LANCE,   "weaker" : WeaponType.SWORD},
                         WeaponType.LANCE   :  {"stronger" : WeaponType.SWORD,   "weaker" : WeaponType.AXE},
                         WeaponType.BOW     :  {"stronger" : WeaponType.NONE,    "weaker" : WeaponType.NONE},
                         WeaponType.EMAGIC  :  {"stronger" : WeaponType.NONE,    "weaker" : WeaponType.LMAGIC},
                         WeaponType.LMAGIC  :  {"stronger" : WeaponType.EMAGIC,  "weaker" : WeaponType.NONE}}

tabBonusBetweenClassAndWeapon = {ClassType.PEGASE       :  {"stronger" : WeaponType.NONE,  "weaker" : WeaponType.BOW},
                                 ClassType.SWORDMASTER  :  {"stronger" : WeaponType.NONE,  "weaker" : WeaponType.NONE},
                                 ClassType.WARRIOR      :  {"stronger" : WeaponType.NONE,  "weaker" : WeaponType.NONE},
                                 ClassType.HALBARDIER   :  {"stronger" : WeaponType.NONE,  "weaker" : WeaponType.NONE},
                                 ClassType.ARCHER       :  {"stronger" : WeaponType.NONE,  "weaker" : WeaponType.NONE},
                                 ClassType.MAGE         :  {"stronger" : WeaponType.NONE,  "weaker" : WeaponType.NONE},
                                 ClassType.PRIEST       :  {"stronger" : WeaponType.NONE,  "weaker" : WeaponType.NONE}}

class Servant(Card):
    """
    Derive de Card 
    Classe reprsesentant les serviteurs a invoquer qui pourront attaquer l'adversaire et ses serviteurs 
    """
    
    def __init__(self, params):
        Card.__init__(self, params.get("name"), params.get("description"), params.get("cost"))
        self.stats = Stats(params.get("hp"),
                           params.get("str"),
                           params.get("int"),
                           params.get("pre"),
                           params.get("spe"),
                           params.get("def"),
                           params.get("res"),
                           params.get("cri"))
        self.level = params.get("level")
        self.experience = params.get("xp")
        self.classType = params.get("classType")
        self.weaponType = params.get("weaponType")
        
    def getBattleData(self, servantSelf, servantEnemy):
        dicDataAttacker = {"hp" : 0, "dmg" : 0, "pre" : 0, "cri" : 0}
        dicDataDefender = {"hp" : 0, "dmg" : 0, "pre" : 0, "cri" : 0}
        dicData = {"dataAttacker" : dicDataAttacker, "dataDefender" : dicDataDefender}
        
        
        
        return dicData
        
    def getWeaponBonus(self, servantAttacker, servantEnemy):
        dicDataAttacker = {"str" : 0, "pre" : 0}
        dicDataDefender = {"str" : 0, "pre" : 0}
        dicData = {"bonusAttacker" : dicDataAttacker, "bonusDefender" : dicDataDefender}
        
        if(tabBonusBetweenWeapon.get(servantAttacker.weaponType).get("stronger") == servantEnemy.weaponType):
            dicDataAttacker["str"] += 1
            dicDataAttacker["pre"] += 1
            dicDataDefender["str"] += -1
            dicDataDefender["pre"] += -1
        elif(tabBonusBetweenWeapon.get(servantEnemy.weaponType).get("stronger") == servantAttacker.weaponType):
            dicDataAttacker["str"] += -1
            dicDataAttacker["pre"] += -1
            dicDataDefender["str"] += 1
            dicDataDefender["pre"] += 1
            
        if(tabBonusBetweenClassAndWeapon.get(servantAttacker.classType).get("weaker") == servantEnemy.weaponType):
            dicDataAttacker["str"] += 0
            dicDataAttacker["pre"] += 0
            dicDataDefender["str"] += 3
            dicDataDefender["pre"] += 0
        elif(tabBonusBetweenClassAndWeapon.get(servantEnemy.classType).get("weaker") == servantAttacker.weaponType):
            dicDataAttacker["str"] += 0
            dicDataAttacker["pre"] += 0
            dicDataDefender["str"] += 3
            dicDataDefender["pre"] += 0
            
        return 0
        
    def battleBetweenServant(self, servantSelf, servantEnemy):
        self.attack(servantSelf, servantEnemy)
        
    def attack(self, servantSelf, servantEnemy):
        self.applyDamage(servantEnemy)
        self.applyDamage(servantSelf)
        
    def applyDamage(self, servant):
        print('applyDamage')
    """
    def applyWeekness(self, servant):
        if(self.classType == "SWORDMASTER" and servant.classType == "WARRIOR"):
    """     
    
    def earnedExperience(self, servantSelf, servantEnemy):
        earnedXp = 50
        earnedXp = earnedXp * (servantEnemy.level/servantSelf.level)
        if(servantEnemy.stats.hp > 0):
            earnedXp = int(earnedXp/2)
        return earnedXp
        
    """
    Fonction appelé lors d'un level up --> à remplacer par l'utilisation d'un item à utilisation direct
    car point de stat gagné spécifique selon la class
    """
    def levelUp(self):
        self.stats.hp += 1
        self.stats.strength += 1
        self.stats.intelligence += 1
        self.stats.precision += 1
        self.stats.speed += 1
        self.stats.defense += 1
        self.stats.resistance += 1
        self.stats.critical += 1
        
        self.experience = 0
        self.level = 2