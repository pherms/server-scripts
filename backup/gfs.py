import modules as mods
from pathlib import Path
from datetime import datetime
from datetime import date
import socket
import os

def main():
    config = mods.readConfig()
    
    compression = config["compression"]
    backuppath = 'C:\\Users\\pherm\\backup\\'
    filesize = config["filesize"]
    filetype = config["filetype"]
    logfilepath = config["logfilepath"]
    logfile = mods.openLogFile(logfilepath)

    for file in os.walk(backuppath):
        print(backuppath)
        print(file)
        fullFile = backuppath + file
        dateModified = mods.getDateTime(fullFile)
        week,dag = date.fromisoformat(dateModified).isocalendar()[:2]
        print("Week: {}",week)
        print("dag: {}",dag)

if __name__ == '__main__':
    main()
