# -*- coding : utf-8 -*-

from Utils.Enum import enum

WeaponType = enum("Weapon",
                  "SWORD", "AXE", "LANCE", "BOW", "EMAGIC", "LMAGIC")

print("tranché")


if __name__ == '__main__':
    print(WeaponType.SWORD)
    #print(Weapon.SWORD)
