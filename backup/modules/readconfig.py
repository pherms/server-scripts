import json
import socket
from datetime import datetime

def readSourcesFile(logfile,sources):
    """
    Leest de sources file in. De locatie van de sources file is configureerbaar in config.json

    :param obj logfile: het logfile bestand waar naartoe moet worden gelogd
    :param str sources: de locatie van de sources file. Deze parameter is configureerbaar in config.json
    :return: een array met lines
    :rtype: array
    """
    try:
        logfile.write("{} Inlezen van lijst met te backuppen files en folders\n".format(datetime.today()))
        sourceFile = open(sources, 'r')
        lines = sourceFile.readlines()
        return lines
    except Exception:
        logfile.write("{} Er is een fout opgetreden bij het inlezen van sources file. Backup wordt afgebroken.\n".format(datetime.today()))
        exit()

def readConfig():
    """
    Leest de config.json file in.

    :return: een json object
    :rtype: object
    """
    try:
        f = open("/etc/server-scripts/backup-config.json","rb")
        jsonObject = json.load(f)
        f.close
        return jsonObject
    except Exception:
        print("{} Er is een fout opgetreden bij het inlezen van de config file. Backup wordt afgebroken.\n".format(datetime.today()))
        exit()

def getHostname(logfile):
    """
    Leest de hostname waarde uit de config.json. Wanneer deze waarde niet in de config file staat geconfigureerd, dan wordt de systeem waarde opgehaald. Deze waarde is configureerbaar in config.json

    :param obj logfile: de logfile waarnaartoe gelogd moet worden
    :return: de hostname waarde als string
    :rtype: str
    """
    try:
        config = readConfig()
        if 'server' not in config:
            logfile.write("{} Servernaam niet gevonden in config bestand. Gebruik hostnaam\n".format(datetime.today()))
            hostname = socket.gethostname()
        else:
            hostname = config["server"]
        
        return hostname
    except Exception:
        logfile.write("{} Fout opgetreden tijdens het ophalen van de hostname\n".format(datetime.today()))
