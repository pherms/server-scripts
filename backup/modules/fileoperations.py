import os, sys
import platform
import time
from pathlib import Path
from datetime import datetime

def isDirectory(path):
    p = Path(path)
    isDirectory = p.is_dir()
    return isDirectory

def generateFileName(hostname,filetype,compression,logfile):
    date = datetime.today().strftime('%Y%m%d')
    if compression == 'bz2':
        # tar.bz2 file
        filename = hostname+"-"+date+"."+filetype+"."+compression
    else:
        # zip file
        filename = hostname+"-"+date+"."+filetype
    
    logfile.write("{} Backup wordt weggeschreven in bestand: {}\n".format(datetime.today(),filename))
    return filename

def createFolder(folder):
    try:
        Path(folder).mkdir(mode=0o755,parents=True)
    except FileExistsError:
        print("{} Folder {} bestaat al".format(datetime.today(),folder))
    else:
        print("{} Folder {} gemaakt".format(datetime.today(),folder))

def getCreationTime(directory):
    # create an empty dictionary to store the file names and creation times
    file_times = {}
    # loop through all the files in the directory
    for file in os.listdir(directory):
        # get the full path of the file
        file_path = os.path.join(directory, file)
        # get the creation time of the file in seconds since epoch
        creation_time = os.path.getctime(file_path)        
        # convert the creation time to a human-readable format
        creation_time = time.ctime(creation_time)
        creation_datetime = datetime.strptime(creation_time,'%a %b %d %H:%M:%S %Y')
        # store the file name and creation time in the dictionary
        file_times[file] = creation_datetime.date()
    # return the dictionary
    return file_times
