# -*- coding : utf-8 -*-

from Utils.Enum import enum
from Card import Card
from Stats import Stats
from Item import *
from random import *

ClassType = enum("Class",
                 "SWORDMASTER", "WARRIOR", "HALBARDIER", "ARCHER", "PEGASUS", "MAGE", "PRIEST")

WeaponType = enum("Weapon",
                  "SWORD", "AXE", "LANCE", "BOW", "EMAGIC", "LMAGIC", "NONE")

"""
Définition des bonus malus directement pour simplifier le code
--> permet d'avoir moins de condition pour d�terminer les bonus / malus
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

tabBonusBetweenClassAndWeapon = {ClassType.PEGASUS       :  {"stronger" : WeaponType.NONE,  "weaker" : WeaponType.BOW},
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
        self.weaponEquipped = None
        

    def getBattleData(self, servantEnemy):
        """
        Fonction qui retourne un dictionnaire de donn�es 
        concernant un combat entre 2 serviteurs
        """
        
        dicDataAttacker = {"hp"  : self.stats.hp, 
                           "dmg" : self.stats.strength, 
                           "pre" : self.stats.precision,
                           "spe" : self.stats.speed,
                           "cri" : self.stats.critical}        
        dicDataDefender = {"hp"  : servantEnemy.stats.ph,
                           "dmg" : servantEnemy.stats.strength,
                           "pre" : servantEnemy.stats.precision,
                           "spe" : servantEnemy.stats.speed,
                           "cri" : servantEnemy.stats.critical}
        
        dicData = {"dataAttacker" : dicDataAttacker, "dataDefender" : dicDataDefender}
        
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
        
        return dicData
        
        
    def getBattleBonus(self, servantEnemy):
        """
        Fonction qui retourne un dictionnaire de donn�es (sera utilse pour dislpay les infos sur l'ecran)
        concerant les bonus et malus selon les armes et classe lors d'un combat entre 2 serviteurs 
            (voir les 2 gros dictionnaires en haut du ficier pour mieux comprendre) 
            (Le serviteur attaquant est self / le serviteur d�fendant est servantEnemy)
        """
    
        dicDataAttacker = {"dmg" : 0, "pre" : 0}
        dicDataDefender = {"dmg" : 0, "pre" : 0}
        dicData = {"bonusAttacker" : dicDataAttacker, "bonusDefender" : dicDataDefender}
        #Checking des bonus malus pour les armes
        if(tabBonusBetweenWeapon.get(self.weaponType).get("stronger") == servantEnemy.weaponType):
            dicDataAttacker["dmg"] += 1
            dicDataAttacker["pre"] += 1
            dicDataDefender["dmg"] += -1
            dicDataDefender["pre"] += -1
        elif(tabBonusBetweenWeapon.get(servantEnemy.weaponType).get("stronger") == self.weaponType):
            dicDataAttacker["dmg"] += -1
            dicDataAttacker["pre"] += -1
            dicDataDefender["dmg"] += 1
            dicDataDefender["pre"] += 1
        #Checking des bonus malus de la classe par rapport � l'arme    
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
        Fonction r�cup�rant toutes les infos des servants
        Et traite tout le combat
        """
        dicData = self.getBattleData(servantEnemy)
        dicDataAttacker = dicData.get("dataAttacker")
        dicDataDefenser = dicData.get("dataDefenser")
        """
        Tour de l'attaquant
            On fait du randint pour avoir savoir si le servant touchera la cible et/ou si il fera un coup critique
            Si le randInt Critique est compris entre 1 et le critique de stat --> dommage*3 et lancement de l'attaque
            Sinon, si lr randInt de Touche est comprise entre 1 et la pr�cision  --> lancement de l'attaque
            Sinon attaque manqu�
        Tour du d�fenseur
            Verification si le d�fenseur est en vie
                Si oui --> Meme sch�ma que l'attaquant
        Donner l'exp�rience du combat
        D�truire si serviteur mort (avoir 0 hp)
        """
        precisionAttacker = (dicDataAttacker.get("pre")*10) - (dicDataDefenser.get("spe")*5)
        criticalAttacker = randint(1, 100)
        hitAttacker = randint(1, 100)
        damageAttacker = dicDataAttacker.get("dmg")
        
        if(criticalAttacker >= 1 and criticalAttacker <= self.stats.critical):
            damageAttacker *= 3
            self.applyDamage(servantEnemy, damageAttacker)
        elif(hitAttacker >= 1 and hitAttacker <= precisionAttacker):
            self.applyDamage(servantEnemy, damageAttacker)
        else:
            print("miss")
            
        if(servantEnemy.stats.hp > 0):
            #Tour du defenseur
            precisionDefenser = (dicDataDefenser.get("pre")*10) - (dicDataAttacker.get("spe")*5)
            criticalDefenser = randint(1, 100)
            hitDefenser = randint(1, 100)
            damageDefenser = dicDataDefenser.get("dmg")
            
            if(criticalDefenser >= 1 and criticalDefenser <= servantEnemy.stats.critical):
                damageDefenser *= 3
                servantEnemy.applyDamage(self, damageDefenser)
            elif(hitDefenser >= 1 and hitDefenser <= precisionDefenser):
                servantEnemy.applyDamage(self, damageDefenser)
            else:
                print("miss")

        self.earnedExperience(servantEnemy)
        servantEnemy.earnedExperience(self)

        if(self.stats.hp <= 0):
            self.killed()
        if(servantEnemy.stats.hp <= 0):
            servantEnemy.killed()
        
         
    def applyDamage(self, servantAttacked, damageToApply):
        """
        Fonction qui applique les degat lors d'un combat entre serviteur
        Si les hp sont inf�rieur � 0, ils seront remis � 0
        """
        servantAttacked.stats.hp -= damageToApply
        if(servantAttacked.stats.hp < 0):
            servantAttacked.stats.hp = 0
    
    
    def killed(self):
        print("killed")
    
    
    def earnedExperience(self, servantEnemy):
        """
        Fonction de calcul retournant l'experience gagner lors d'un combar
            De base on consid�re que l'ennemi est tu� et qu'on gagne 50pts d'xp (sur 100pts pour level up)
            On multiplie ces 50pts par le niveau de l'ennemi divis� par le sien
            Et ensuite, si l'ennemi n'est pas mort, on divise par 2 le total avec un cast int pour ne pas avoir de d�cimale
        """
        earnedXp = 50
        earnedXp = earnedXp * (servantEnemy.level/self.level)
        if(servantEnemy.stats.hp > 0):
            earnedXp = int(earnedXp/2)
        return earnedXp
        
    
    def levelUp(self):
        """
        Fonction appel� lors d'un level up --> � remplacer par l'utilisation d'un item � utilisation direct
        car point de stat gagn� sp�cifique selon la class
        """
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
        
if __name__ == '__main__':
    print("�ta��")