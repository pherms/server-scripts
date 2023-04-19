import os, sys
from pathlib import Path
from datetime import datetime

def isDirectory(path):
    p = Path(path)
    isDirectory = p.is_dir()
    return isDirectory

def generateFileName(server,filetype,compression,logfile):
    date = datetime.today().strftime('%Y%m%d')
    if compression == 'bz2':
        # tar.bz2 file
        filename = server+date+"."+filetype+"."+compression
    else:
        # zip file
        filename = server+date+"."+filetype
    
    logfile.write("{} Backup wordt weggeschreven in bestand: {}".format(datetime.today(),filename))
    return filename

def createFolder(folder):
    try:
        Path(folder).mkdir(mode=0o755,parents=True)
    except FileExistsError:
        print("{} Folder {} bestaat al".format(datetime.today(),folder))
    else:
        print("{} Folder {} gemaakt".format(datetime.today(),folder))
    