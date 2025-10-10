# import sys
# sys.path.append('./modules')
# from modules import readtext as readtext
import modules as mods
from pathlib import Path
from datetime import datetime

# from .modules/readsource import *
# dir(readsource)

def main():
    config = mods.readConfig()
    
    compression = config["compression"]
    backuppath = config["backuppath"]
    filetype = config["filetype"]
    logfilepath = config["logfilepath"]
    sources = config["sourcesLocation"]
    debug = bool(config["debug"])
    apiserver = config["apiServer"]
    logfile = mods.openLogFile(logfilepath,"backup","write",debug)
    hostname = mods.getHostname(logfile)
    apitoken = config["apiToken"]
    exclusionList = []
    inclusionList = []
    listToBackup = []
    
    logfile.write("{} Inlezen configuratie bestand\n".format(datetime.today()))
    mods.createFolder(backuppath)
    filename = backuppath + mods.generateFileName(hostname,filetype,compression,logfile,debug)
    
    lines = mods.readSourcesFile(logfile,sources,debug)
    archive = mods.openArchiveWrite(filename,filetype,logfile,debug)

    for line in lines:
        mods.determineFolderlists(line,exclusionList,inclusionList,debug)

    mods.prepareSourceListToBackup(logfile,listToBackup,exclusionList,inclusionList,debug)
    
    if debug:
        print("[DEBUG] Exclusion list: {}".format(exclusionList))

    result = mods.addFilesToArchive(archive,filetype,logfile,listToBackup,debug)

    mods.closeArchiveWrite(archive,filetype)
    archiveFileSize = mods.getArchiveFileSize(archive)

    logfile.write("{} Backup geslaagd\n".format(datetime.today()))
    logfile.write("{} De backup is {}\n".format(datetime.today(),archiveFileSize))
    mods.closeLogFile(logfile)

    if result == "success":
        logfileread = "Backup succesvol uitgevoerd"
    elif result == "failure":
        logfileread = mods.openLogFile(logfilepath,"backup","read",debug)
        mods.closeLogFile(logfileread)
    
    mods.sendLogFile(hostname,logfileread,debug,apiserver,apitoken,result,archiveFileSize)
if __name__ == '__main__':
    main()