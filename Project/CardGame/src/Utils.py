# -*- coding : utf-8 -*-
# -*- coding: iso-8859-1 -*-

def enum(enumName, *listValueNames):
    listValueNumbers = range(len(listValueNames))
    dictAttrib = dict( zip(listValueNames, listValueNumbers) )
    dictReverse = dict( zip(listValueNumbers, listValueNames) )
    dictAttrib["dictReverse"] = dictReverse
    return type(enumName, (), dictAttrib)