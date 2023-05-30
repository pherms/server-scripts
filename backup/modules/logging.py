import modules as mods
from datetime import datetime
from pathlib import Path

def openLogFile(logpath,logfiletype):
    mods.createFolder(logpath)
    date = datetime.today().strftime('%y%m%d')
    if logfiletype == "backup":
        logfilename = "backuplog-" + date + ".log"
    elif logfiletype == "cleanup":
        logfilename = "cleanuplog-" + date + ".log"

    try:
        logfile = open(logpath + logfilename,"w")
        return logfile
    except Exception:
        print("Er is iets naars gebeurd")
        exit()

def closeLogFile(logfile):
    logfile.close()

def cleanupLogs():
    print("Cleanup Logs")