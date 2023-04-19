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
    
    
    server = config["server"]
    compression = config["compression"]
    backuppath = config["backuppath"]
    filesize = config["filesize"]
    filetype = config["filetype"]
    logfilepath = config["logfilepath"]
    
    logfile = mods.openLogFile(logfilepath)
    logfile.write("{} Inlezen configuratie bestand\n".format(datetime.today()))
    mods.createFolder(backuppath)
    filename = backuppath + mods.generateFileName(server,filetype,compression,logfile)
    
    lines = mods.readSourcesFile(logfile)
    archive = mods.openArchiveWrite(filename,filetype,compression)

    for line in lines:
        if mods.determineInclusion(line):
            line = mods.prepareFileToZip(line)
            mods.addFilesToArchive(archive,Path(line),filetype,logfile)

    mods.closeArchiveWrite(archive,filetype)
    logfile.write("{} Backup geslaagd\n".format(datetime.today()))
    mods.closeLogFile(logfile)
    
if __name__ == '__main__':
    main()