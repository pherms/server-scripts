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
    filesize = config["filesize"]
    filetype = config["filetype"]
    logfilepath = config["logfilepath"]
    sources = config["sourcesLocation"]
    logfile = mods.openLogFile(logfilepath,"backup")
    hostname = mods.getHostname(logfile)
    
    logfile.write("{} Inlezen configuratie bestand\n".format(datetime.today()))
    mods.createFolder(backuppath)
    filename = backuppath + mods.generateFileName(hostname,filetype,compression,logfile)
    
    lines = mods.readSourcesFile(logfile,sources)
    archive = mods.openArchiveWrite(filename,filetype,compression,logfile)

    for line in lines:
        if mods.determineInclusion(line):
            line = mods.prepareFileToZip(line)
            mods.addFilesToArchive(archive,Path(line),filetype,logfile)

    archiveFileSize = mods.closeArchiveWrite(archive,filetype)

    logfile.write("{} Backup geslaagd\n".format(datetime.today()))
    mods.closeLogFile(logfile)

    message_text = """\
    De backup van {hostname} is succesvol uitgevoerd.\n
    Het backup bestand is {filesizeHumanReadable} groot.\n
    Zie ook bijgande logfile\n""".format(hostname=hostname,filesizeHumanReadable=mods.archiveSize(archiveFileSize))
    subject = "Backup server {}".format(hostname)

    mods.sendMail(subject,message_text,logfile)
    
if __name__ == '__main__':
    main()