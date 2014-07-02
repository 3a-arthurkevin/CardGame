# -*- coding : utf-8 -*-

import json
import os
import codecs

projectDir = os.path.abspath(os.path.dirname(__file__) + "\\..\\..")

def loadConfig(fileName=(projectDir + "\\Data\\data.json")):
    data = {}
    try:
        #file = open(fileName)
        file = codecs.open(fileName, "r", "utf-8")     
        data = json.loads(file.read())
        file.close()   
    except IOError:
        print("file : ", fileName, " not found")

    return data

def saveConfig(data, indent=True, fileName=(projectDir + "\\Data\\data.json")):
    try:
        file = open(fileName, "w")
        file.write(json.dumps(data, indent=indent))
        file.close()
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
        
        
        
        