# -*- coding : utf-8 -*-

from Utils import *

WeaponType = enum("Weapon",
                  "SWORD", "AXE", "LANCE", "BOW", "EMAGIC", "LMAGIC")

if __name__ == '__main__':
    print(WeaponType.SWORD)
    #print(Weapon.SWORD)
