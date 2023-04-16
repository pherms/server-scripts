import json

def readSourcesFile():
    sourceFile = open('sources', 'r')
    lines = sourceFile.readlines()
    return lines

def readConfig():
    f = open("config.json","rb")
    jsonObject = json.load(f)
    f.close
    return jsonObject