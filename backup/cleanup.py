# import datetime
from datetime import *
from pathlib import Path
import os
import modules as mods

def main():
    config = mods.readConfig()

    backuppath = config["backuppath"]
    logfilepath = config["logfilepath"]
    hostType = config["hostType"]

    logfile = mods.openLogFile(logfilepath,"cleanup")
    hostname = mods.getHostname(logfile)
    
    files_cleaned = []
    files_renamed = []

    try:
        if hostType == 'vm':
            files = mods.getCreationTime(backuppath)

            files_cleaned,files_renamed = mods.determineRemoveOrBackup(files,hostType,logfile,backuppath)
        elif hostType == 'host':
            filesArray = {}
            backupRootPath = str(Path(backuppath).parent)
            
            for folder in os.listdir(backupRootPath):
                currentFolder = backupRootPath + '/' + folder
                if mods.isDirectory(currentFolder):
                    for file in os.listdir(currentFolder):
                        fullFile = os.path.abspath(currentFolder + '/' + file)
                        filesArray[fullFile] = "nothing"

            files_cleaned,files_renamed = mods.determineRemoveOrBackup(filesArray,hostType,logfile,backupRootPath)
            
        logfile.write("{} Files verwijderd: {}\n".format(datetime.today(),len(files_cleaned)))
        logfile.write("{} Files hernoemd: {}\n".format(datetime.today(),len(files_renamed)))

        message_text = """\
        De cleanup van oude files van {hostname} is succesvol voltooid.\n\n
        Het totaal aantal verwijderde bestanden is: {totalFilesCleaned}\n
        Het totaal aantal hernoemde bestanden is: {totalFilesRenamed}\n\n
        Zie ook bijgande logfile\n""".format(hostname=hostname,totalFilesCleaned=len(files_cleaned),totalFilesRenamed=len(files_renamed))
        subject = "Cleanup van files op server {} succesvol".format(hostname)
        
        mods.closeLogFile(logfile)
        mods.sendMail(subject,message_text,logfile)

        # Cleanup logfiles in logpPath
        mods.cleanupLogs(logfilepath)

    except Exception as error:
        message="""\
            Cleanup van server {hostname} is gefaald\n
            {error}""".format(hostname=hostname,error=error)
        mods.sendMailFailedCleanup(hostname,message)

if __name__ == '__main__':
    main()
