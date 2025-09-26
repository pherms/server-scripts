import modules as mods
from datetime import datetime
from pathlib import Path
import requests

def openLogFile(logpath,logfiletype,action,debug):
    """
    Opent de logfile in schrijf modus, waar naartoe moet worden gelogd.

    :param str logpath: het pad waarin de logfile moet worden geschreven. Configureerbaar in config.json
    :param str logfiletype: het type logfile wat moet worden geopend. Mogelijke opties zijn: 'backup', 'cleanup' en 'copy'
    :return: de open logfile in write modus
    :rtype: object
    """
    mods.createFolder(logpath)
    date = datetime.today().strftime('%Y%m%d')
    if logfiletype == "backup":
        logfilename = "backuplog-" + date + ".log"
    elif logfiletype == "cleanup":
        logfilename = "cleanuplog-" + date + ".log"
    elif logfiletype == "copy":
        logfilename = "copylog-" + date + ".log"
    elif logfiletype == "update":
        logfilename = "updatelog.log"

    try:
        if action == "write":
            logfile = open(logpath + logfilename,"w")
        elif action == "read":
            logfile = open(logpath + logfilename,"r")

        if debug:
            print("[DEBUG] Logfile {} is aangemaakt".format(logfilename))

        return logfile
    except Exception:
        print("Er is iets naars gebeurd tijdens het openen van de logfile")
        exit()

def closeLogFile(logfile):
    """
    Sluit de logfile waar naartoe is gelogd.

    :param str logfile: het logfile object wat moet worden gesloten
    """
    logfile.close()

def sendLogFile(serverName,logfile,debug,apiServer,apiToken):
    """
    Verzend de logfile via een API call.

    :param str serverName: de server waar naartoe is gebackupt
    :param str logfile: het logfile object wat moet worden verzonden
    :param bool debug: of debug mode aan staat
    :param str apiServer: de API server waar naartoe moet worden verzonden
    """
    logContent = logfile.read()
    endpoint = "http://{}/api/v1/logging".format(apiServer)

    headers = {}
    if apiToken:
        headers["X-API-Token"] = apiToken
        headers["Content-Type"] = "application/json"
    
    payload = {
        "Servername": serverName,
        "Logentry": logContent,
        "Logdate": datetime.now().isoformat()
    }
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=20)
    except Exception as e:
        print("Er is een error opgetreden tijdens het verbinden met de API server: {}".format(e))
        return

    if debug:
        print("[DEBUG] API response: {}".format(response.status_code))

    if response.status_code != 200:
        print("Fout bij het verzenden van logdata: {} {}".format(response.status_code, response.text))
        return

