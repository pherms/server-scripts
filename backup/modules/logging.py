import modules as mods
from datetime import datetime
from pathlib import Path

def openLogFile(logpath,logfiletype,debug):
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
        # if Path(logpath + logfilename).exists():
        #     logfile = open(logpath + logfilename,"a")
        # else:
        logfile = open(logpath + logfilename,"w")

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
