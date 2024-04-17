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
    debug = bool(config["debug"])

    logfile = mods.openLogFile(logfilepath,"cleanup",debug)
    hostname = mods.getHostname(logfile)
    
    files_cleaned = []
    files_renamed = []

    try:
        if hostType == 'vm':
            files = mods.getCreationTime(backuppath,debug)

            files_cleaned,files_renamed = mods.determineRemoveOrBackup(files,hostType,logfile,backuppath,debug)
        elif hostType == 'host':
            # filesArray = {}
            backupRootPath = str(Path(backuppath).parent)
            
            for folder in os.listdir(backupRootPath):
                # currentFolder = backupRootPath + '/' + folder
                print("[DEBUG] folder {} in backuppath {}".format(folder,backupRootPath))
                currentFolder = os.path.join(str(backupRootPath),str(folder))
                if mods.isDirectory(currentFolder):
                    # for file in os.listdir(folder):
                    
                        # fullFile = os.path.abspath(currentFolder + '/' + file)
                        # filesArray[fullFile] = "nothing"
                    files = mods.getCreationTime(currentFolder,debug)
                    print("[DEBUG] files: {} in folder {}".format(files,currentFolder))
                    files_cleaned,files_renamed = mods.determineRemoveOrBackup(files,hostType,logfile,currentFolder,debug)
                        

            if debug:
                print("[DEBUG] HostType: {}".format(hostType))
                print("[DEBUG] filesArray: {}".format(filesArray))
                print("[DEBUG] backupRootPath: {}".format(backupRootPath))
                print("[DEBUG] fullFile: {}".format(fullFile))

            # files_cleaned,files_renamed = mods.determineRemoveOrBackup(filesArray,hostType,logfile,backupRootPath,debug)
            
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
        mods.cleanupLogs(logfilepath,debug)

    except Exception as error:
        message="""\
            Cleanup van server {hostname} is gefaald\n
            {error}""".format(hostname=hostname,error=error)
        mods.sendMailFailedCleanup(hostname,message)

if __name__ == '__main__':
    main()
