import json
import socket
from datetime import datetime

def readSourcesFile(logfile):
    try:
        logfile.write("{} Inlezen van lijst met te backuppen files en folders\n".format(datetime.today()))
        sourceFile = open('sources', 'r')
        lines = sourceFile.readlines()
        return lines
    except Exception:
        logfile.write("{} Er is een fout opgetreden bij het inlezen van sources file. Backup wordt afgebroken.\n".format(datetime.today()))
        exit()

def readConfig():
    try:
        f = open("config.json","rb")
        jsonObject = json.load(f)
        f.close
        return jsonObject
    except Exception:
        print("{} Er is een fout opgetreden bij het inlezen van de config file. Backup wordt afgebroken.\n".format(datetime.today()))
        exit()

def getHostname(logfile):
    try:
        config = readConfig()
        if 'server' not in config:
            logfile.write("{} Servernaam niet gevonden in config bestand. Gebruik hostnaam\n".format(datetime.today()))
            server = socket.gethostname()
        else:
            server = config["server"]
        
        return server
    except Exception:
        logfile.write("{} Fout opgetreden tijdens het ophalen van de hostname\n".format(datetime.today()))
