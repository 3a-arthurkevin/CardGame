# -*- coding : utf-8 -*-

from Utils.Enum import enum
from Card import Card
from Stats import Stats
from Item import *
from random import *

ClassType = enum("ClassType",
                 "SWORDMASTER", "WARRIOR", "HALBARDIER", "ARCHER", "PEGASUS", "MAGE", "PRIEST")

WeaponType = enum("WeaponType",
                  "SWORD", "AXE", "LANCE", "BOW", "EMAGIC", "LMAGIC", "NONE")

"""
Définition des bonus malus directement pour simplifier le code
--> permet d'avoir moins de condition pour déterminer les bonus / malus
--> comme on a besoin de ces infos à chaque combat entre serviteurs autant les poser un fois pour toute
--> plus facile à maintenir en cas d'ajout et de retrait d'elements
--> mettre toutes les classes et armes pour ne pas a tester si une clé existe (en dehors du type NONE (jamais attribuer à une class ou arme))
"""

tabBonusBetweenWeapon = {WeaponType.SWORD   :  {"stronger" : WeaponType.AXE,     "weaker" : WeaponType.LANCE},
                         WeaponType.AXE     :  {"stronger" : WeaponType.LANCE,   "weaker" : WeaponType.SWORD},
                         WeaponType.LANCE   :  {"stronger" : WeaponType.SWORD,   "weaker" : WeaponType.AXE},
                         WeaponType.BOW     :  {"stronger" : WeaponType.NONE,    "weaker" : WeaponType.NONE},
                         WeaponType.EMAGIC  :  {"stronger" : WeaponType.NONE,    "weaker" : WeaponType.LMAGIC},
                         WeaponType.LMAGIC  :  {"stronger" : WeaponType.EMAGIC,  "weaker" : WeaponType.NONE}}

tabBonusBetweenClassAndWeapon = {ClassType.PEGASUS      :  {"stronger" : WeaponType.NONE,  "weaker" : WeaponType.BOW},
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
        Card.__init__(self, params)
        self.stats = Stats(params)
        self.level = params.get("level")
        self.experience = params.get("xp")
        self.classType = params.get("classType")
        self.weaponType = params.get("weaponType")
        self.weaponEquipped = None
        

    def getBattleData(self, servantEnemy):
        """
        Fonction qui retourne un dictionnaire de données 
        concernant un combat entre 2 serviteurs
        """
        damageAttacker = self.stats.strength
        damageDefender = servantEnemy.stats.strength 
        
        if(self.classType == ClassType.MAGE):
            damageAttacker = self.stats.intelligence
        if(servantEnemy.classType == ClassType.MAGE):
            damageDefender = servantEnemy.stats.intelligence
            
        dicDataAttacker = {"hp"  : self.stats.hp, 
                           "dmg" : damageAttacker, 
                           "pre" : self.stats.precision,
                           "spe" : self.stats.speed,
                           "cri" : self.stats.critical}        
        dicDataDefender = {"hp"  : servantEnemy.stats.hp,
                           "dmg" : damageDefender,
                           "pre" : servantEnemy.stats.precision,
                           "spe" : servantEnemy.stats.speed,
                           "cri" : servantEnemy.stats.critical}
        
        dicDataBonus = self.getBattleBonus(servantEnemy)
        
        dicDataAttacker["dmg"] += dicDataBonus.get("bonusAttacker").get("dmg")
        dicDataAttacker["pre"] += dicDataBonus.get("bonusAttacker").get("pre")
        dicDataDefender["dmg"] += dicDataBonus.get("bonusDefender").get("dmg")
        dicDataDefender["pre"] += dicDataBonus.get("bonusDefender").get("pre")
        
        if(self.weaponEquipped != None and self.weaponEquipped == ItemType.WEAPON):
            dicDataAttacker["dmg"] += self.weaponEquipped.stats.strength
            dicDataAttacker["pre"] += self.weaponEquipped.stats.precision
            dicDataAttacker["spe"] += self.weaponEquipped.stats.speed
            dicDataAttacker["cri"] += self.weaponEquipped.stats.critical
        if(servantEnemy.weaponEquipped != None and servantEnemy.weaponEquipped == ItemType.WEAPON):
            dicDataDefender["dmg"] += servantEnemy.weaponEquipped.stats.strength
            dicDataDefender["pre"] += servantEnemy.weaponEquipped.stats.precision
            dicDataDefender["spe"] += servantEnemy.weaponEquipped.stats.speed
            dicDataDefender["cri"] += servantEnemy.weaponEquipped.stats.critical
        
        dicData = {"dataAttacker" : dicDataAttacker, "dataDefender" : dicDataDefender}
        
        return dicData
        
        
    def getBattleBonus(self, servantEnemy):
        """
        Fonction qui retourne un dictionnaire de données (sera utilse pour dislpay les infos sur l'ecran)
        concerant les bonus et malus selon les armes et classe lors d'un combat entre 2 serviteurs 
            (voir les 2 gros dictionnaires en haut du ficier pour mieux comprendre) 
            (Le serviteur attaquant est self / le serviteur défendant est servantEnemy)
        """
    
        dicDataAttacker = {"dmg" : 0, "pre" : 0}
        dicDataDefender = {"dmg" : 0, "pre" : 0}
        dicData = {"bonusAttacker" : dicDataAttacker, "bonusDefender" : dicDataDefender}
        #Checking des bonus malus pour les armes
        if(tabBonusBetweenWeapon.get(self.weaponType).get("stronger") == servantEnemy.weaponType):
            dicDataAttacker["dmg"] += 1
            dicDataAttacker["pre"] += 2
            dicDataDefender["dmg"] += -1
            dicDataDefender["pre"] += -2
        elif(tabBonusBetweenWeapon.get(servantEnemy.weaponType).get("stronger") == self.weaponType):
            dicDataAttacker["dmg"] += -1
            dicDataAttacker["pre"] += -2
            dicDataDefender["dmg"] += 1
            dicDataDefender["pre"] += 2
        #Checking des bonus malus de la classe par rapport à l'arme    
        if(tabBonusBetweenClassAndWeapon.get(self.classType).get("weaker") == servantEnemy.weaponType):
            dicDataAttacker["dmg"] += 0
            dicDataAttacker["pre"] += 0
            dicDataDefender["dmg"] += 3
            dicDataDefender["pre"] += 0
        elif(tabBonusBetweenClassAndWeapon.get(servantEnemy.classType).get("weaker") == self.weaponType):
            dicDataAttacker["dmg"] += 3
            dicDataAttacker["pre"] += 0
            dicDataDefender["dmg"] += 0
            dicDataDefender["pre"] += 0
            
        return dicData
        
        
    def battleBetweenServant(self, servantEnemy):
        """
        Fonction récupérant toutes les infos des servants
        Et traite tout le combat
        """
        dicData = self.getBattleData(servantEnemy)
        dicDataAttacker = dicData.get("dataAttacker")
        dicDataDefender = dicData.get("dataDefender")

        """
        Tour de l'attaquant
            On fait du randint pour avoir savoir si le servant touchera la cible et/ou si il fera un coup critique
            Si le randInt Critique est compris entre 1 et le critique de stat --> dommage*3 et lancement de l'attaque
            Sinon, si le randInt de Touche est comprise entre 1 et la précision  --> lancement de l'attaque
            Sinon attaque manqué
        Tour du défenseur
            Verification si le défenseur est en vie
                Si oui --> Meme schéma que l'attaquant
        Donner l'expérience du combat
        Détruire si serviteur mort (avoir 0 hp)
        """
        
        damageAttacker = dicDataAttacker.get("dmg")
        damageDefender = dicDataDefender.get("dmg")
        
        if(self.classType == ClassType.MAGE):
            damageAttacker -= servantEnemy.stats.resistance
        else:
            damageAttacker -=  servantEnemy.stats.defense
            
        if(servantEnemy.classType == ClassType.MAGE):
            damageDefender -= self.stats.resistance
        else:
            damageDefender -= self.stats.defense
            
        
        precisionAttacker =  dicDataAttacker.get("pre")*10 - dicDataDefender.get("spe")*4
        precisionDefender = dicDataDefender.get("pre")*10 - dicDataAttacker.get("spe")*4
        
        if(damageAttacker < 0):
            damageAttacker = 0
        if(precisionAttacker < 0):
            precisionAttacker = 0
        if(damageDefender < 0):
            damageDefender = 0
        if(precisionDefender < 0):
            precisionDefender = 0
        
        print("_________________________")
        print("Battle between", self.name, " and ", servantEnemy.name)
        print("-----")
        print("Stats of this battle")
        print(self.name, " - atk ", damageAttacker, " | hit ", precisionAttacker, "% | crit ", self.stats.critical, "%")
        print(servantEnemy.name, " - atk ", damageDefender, " | hit ", precisionDefender, "% | crit ", servantEnemy.stats.critical, "%")
        print("-----")
        print(self.name," - hp - ", self.stats.hp)
        print(servantEnemy.name, " - hp - ", servantEnemy.stats.hp)
        print("-----")
            
        criticalAttacker = randint(1, 100)
        hitAttacker = randint(1, 100)
        
        if(criticalAttacker >= 1 and criticalAttacker <= self.stats.critical):
            damageAttacker *= 3
            self.applyDamage(servantEnemy, damageAttacker)
            print(self.name, " - Critical Hit!!!")
        elif(hitAttacker >= 1 and hitAttacker <= precisionAttacker):
            self.applyDamage(servantEnemy, damageAttacker)
            print(self.name, " - Hit")
        else:
            print(self.name, " - Miss")
            
        #print(self.name, " : ", self.stats.hp, " | ", damageAttacker, " | ", hitAttacker, " | ", precisionAttacker, " | ", criticalAttacker, " | ", self.stats.critical)
            
        if(servantEnemy.stats.hp > 0):
            #Tour du defenseur
            criticalDefender = randint(1, 100)
            hitDefender = randint(1, 100)
            
            if(criticalDefender >= 1 and criticalDefender <= servantEnemy.stats.critical):
                damageDefender *= 3
                servantEnemy.applyDamage(self, damageDefender)
                print(servantEnemy.name, " - Critical Hit!!!")
            elif(hitDefender >= 1 and hitDefender <= precisionDefender):
                servantEnemy.applyDamage(self, damageDefender)
                print(servantEnemy.name, " - Hit")
            else:
                print(servantEnemy.name, " - Miss")

            #print(servantEnemy.name ," : ", servantEnemy.stats.hp, " | ", damageDefender, " | ", hitDefender, " | ", precisionDefender, " | " , criticalDefender, " | ", servantEnemy.stats.critical)

        self.earnedExperience(servantEnemy)
        servantEnemy.earnedExperience(self)

        print("-----")
        print(self.name," - hp - ", self.stats.hp)
        print(servantEnemy.name, " - hp - ", servantEnemy.stats.hp)
        print("-----")
        
        self.endBattleManaging(servantEnemy)
        print("-----")
        
        print("Battle Ended")
        print("_________________________")
         
    def applyDamage(self, servantAttacked, damageToApply):
        """
        Fonction qui applique les degat lors d'un combat entre serviteur
        Si les hp sont inférieur à 0, ils seront remis à 0
        """
        servantAttacked.stats.hp -= damageToApply
        if(servantAttacked.stats.hp < 0):
            servantAttacked.stats.hp = 0
    
    def endBattleManaging(self, servantEnemy):
        """
        Fonction qui s'occupe de la fin du combat (vérification si servant est mort et/ou attribution de l'xp + level up)
        """
        if(self.stats.hp <= 0):
            self.killed()
        elif(self.level == 1):
            earnedXp = self.earnedExperience(servantEnemy)
            self.experience += self.earnedExperience(servantEnemy)
            print(self.name, "exp earned :", earnedXp, " | total exp : ", self.experience)
            self.checkLevelUp()
            
        if(servantEnemy.stats.hp <= 0):
            servantEnemy.killed()
        elif(servantEnemy.level == 1):
            earnedXp = servantEnemy.earnedExperience(self)
            servantEnemy.experience += servantEnemy.earnedExperience(self)
            print(servantEnemy.name, "exp earned :", earnedXp, " | total exp : ", servantEnemy.experience)
            servantEnemy.checkLevelUp()
            
    
    def killed(self):
        print(self.name, " - killed")
    
    
    def earnedExperience(self, servantEnemy):
        """
        Fonction de calcul retournant l'experience gagner lors d'un combar
            De base on considère que l'ennemi est tué et qu'on gagne 50pts d'xp (sur 100pts pour level up)
            On multiplie ces 50pts par le niveau de l'ennemi divisé par le sien
            Et ensuite, si l'ennemi n'est pas mort, on divise par 2 le total avec un cast int pour ne pas avoir de décimale
        """
        earnedXp = 0
        if(self.level == 1):
            earnedXp = 50
            earnedXp = earnedXp * (servantEnemy.level/self.level)
            if(servantEnemy.stats.hp > 0):
                earnedXp = int(earnedXp/2)
        return earnedXp
        
    def displayServantInfo(self):
        print("name : ", self.name, "\n",
              "description : ", self.description, "\n",
              "cost : ", self.cost, "\n", 
              "hp", self.stats.hp, " | ",
              "atk", self.stats.strength, " | ",
              "int", self.stats.intelligence, " | ",
              "pre", self.stats.precision, " | ",
              "spe", self.stats.speed, " | ",
              "def", self.stats.defense, " | ",
              "res", self.stats.resistance, " | ",
              "cri", self.stats.critical)
    
    def checkLevelUp(self):
        """
        Fonction qui vérifie si le servant a assez d'xp pour level up
        Si oui, appel de la fonction faisant monter les stats
        """
        if(self.experience >= 100):
            print("Level up !!!")        
            self.levelUp()
            self.displayServantInfo()
    
    def levelUp(self):
        """
        Fonction appelé lors d'un level up --> à remplacer par l'utilisation d'un item à utilisation direct
        car point de stat gagné spécifique selon la class
        --> crée fonction useItem
        
        if(self.classType == ClassType.SWORDMASTER):
            self.useItemLevelUp(ClassType.SWORDMASTER)
        elif(self.classType == CLassType.WARRIOR):
            self.useItemLevelUp(ClassType.WARRIOR)
        elif(self.classType == ClassType.HALBARDIER):
            self.useItemLevelUp(ClassType.HALBARDIER)
        elif(self.classType == ClassType.ARCHER):
            self.useItemLevelUp(ClassType.ARCHER)
        elif(self.classType == ClassType.PEGASUS):
            self.useItemLevelUp(ClassType.PEGASUS)
        elif(self.classType == ClassType.MAGE):
            self.useItemLevelUp(ClassType.MAGE)
        elif(self.classType == ClassType.PRIEST):
            self.useItemLevelUp(ClassType.PRIEST)
        else:
            print("Error")
        """
        self.stats.hp += 1
        self.stats.strength += 1
        self.stats.intelligence += 1
        self.stats.precision += 1
        self.stats.speed += 1
        self.stats.defense += 1
        self.stats.resistance += 1
        self.stats.critical += 1
        
        self.experience = 100
        self.level = 2
        
if __name__ == '__main__':
    dicDataServant1 = {"name" : "s1", 
                  "description" : "ds1", 
                  "cost" : 1,
                  "hp" : 10, 
                  "str" : 6, 
                  "int" : 1, 
                  "pre" : 7, 
                  "spe" : 7,  
                  "def" : 3, 
                  "res" : 3, 
                  "cri" : 5, 
                  "level" : 1, 
                  "xp" : 0, 
                  "classType" : 0, 
                  "weaponType": 0}
    s1 = Servant(dicDataServant1)
    
    dicDataServant2 = {"name" : "s2", 
                  "description" : "ds2", 
                  "cost" : 3, 
                  "hp" : 16, 
                  "str" : 9, 
                  "int" : 2, 
                  "pre" : 7, 
                  "spe" : 5,  
                  "def" : 5, 
                  "res" : 2, 
                  "cri" : 3, 
                  "level" : 2, 
                  "xp" : 100, 
                  "classType" : 1, 
                  "weaponType": 1}
    s2 = Servant(dicDataServant2)
    
    #s1.displayServantInfo()
    
    s1.battleBetweenServant(s2)
    s2.battleBetweenServant(s1)
    s1.battleBetweenServant(s2)
    s2.battleBetweenServant(s1)
    