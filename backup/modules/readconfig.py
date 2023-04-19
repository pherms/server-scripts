import json
from datetime import datetime

def readSourcesFile(logfile):
    logfile.write("{} Inlezen van lijst met te backuppen files en folders\n".format(datetime.today()))
    sourceFile = open('sources', 'r')
    lines = sourceFile.readlines()
    return lines

def readConfig():
    f = open("config.json","rb")
    jsonObject = json.load(f)
    f.close
    return jsonObject