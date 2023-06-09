import modules as mods
from datetime import datetime
from pathlib import Path

def openLogFile(logpath,logfiletype):
    """
    Opent de logfile in schrijf modus, waar naartoe moet worden gelogd.

    :param str logpath: het pad waarin de logfile moet worden geschreven. Configureerbaar in config.json
    :param str logfiletype: het type logfile wat moet worden geopend. Mogelijke opties zijn: 'backup', 'cleanup' en 'copy'
    :return: de open logfile in write modus
    :rtype: object
    """
    mods.createFolder(logpath)
    date = datetime.today().strftime('%y%m%d')
    if logfiletype == "backup":
        logfilename = "backuplog-" + date + ".log"
    elif logfiletype == "cleanup":
        logfilename = "cleanuplog-" + date + ".log"
    elif logfiletype == "copy":
        logfilename = "copylog-" + date + ".log"

    try:
        logfile = open(logpath + logfilename,"w")
        return logfile
    except Exception:
        print("Er is iets naars gebeurd")
        exit()

def closeLogFile(logfile):
    """
    Sluit de logfile waar naartoe is gelogd.

    :param str logfile: het logfile object wat moet worden gesloten
    """
    logfile.close()

def cleanupLogs():
    print("Cleanup Logs")