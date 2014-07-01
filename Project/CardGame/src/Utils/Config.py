# -*- coding : utf-8 -*-

import json
import os

projectDir = os.path.abspath(os.path.dirname(__file__) + "\\..\\..")

def loadConfig(fileName=(projectDir + "\\Data\\data.json")):
    data = {}
    try:
        file = open(fileName)     
        data = json.loads(file.read())   
    except IOError:
        print("file : ", fileName, " not found")

    return data

def saveConfig(data, indent=True, fileName=(projectDir + "\\Data\\data.json")):
    try:
        file = open(fileName, "w")
        file.write(json.dumps(data, indent=indent))
    except IOError:
        print("File not Found")
    except TypeError:
        print("le type de data est pas cool")
    
    return

if __name__ == '__main__':
    
    d = loadConfig()
    
    if len(d) == 0:
        print("dico vide")
    
    else:
        saveConfig(d)
        
        
        
        