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
    logfile = mods.openLogFile(logfilepath,"backup",debug)
    hostname = mods.getHostname(logfile)
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

    mods.addFilesToArchive(archive,filetype,logfile,listToBackup,debug)

    mods.closeArchiveWrite(archive,filetype)
    archiveFileSize = mods.getArchiveFileSize(archive)

    logfile.write("{} Backup geslaagd\n".format(datetime.today()))
    mods.closeLogFile(logfile)

    message_text = """\
    De backup van {hostname} is succesvol uitgevoerd.\n
    Het backup bestand is {filesizeHumanReadable} groot.\n
    Zie ook bijgande logfile\n""".format(hostname=hostname,filesizeHumanReadable=archiveFileSize)
    subject = "Backup server {} succesvol".format(hostname)

    mods.sendMail(subject,message_text,logfile)
    
if __name__ == '__main__':
    main()