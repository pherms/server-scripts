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

    logfile = mods.openLogFile(logfilepath,"cleanup","write",debug)
    hostname = mods.getHostname(logfile)

    try:
        g_files_cleaned = []
        g_files_renamed = []

        if hostType == 'vm':
            files = mods.getCreationTime(backuppath,debug)

            g_files_cleaned,g_files_renamed = mods.determineRemoveOrBackup(files,hostType,logfile,backuppath,debug)
        elif hostType == 'host':
            backupRootPath = str(Path(backuppath).parent)
            for folder in os.listdir(backupRootPath):
                currentFolder = os.path.join(str(backupRootPath),str(folder))
                if mods.isDirectory(currentFolder):
                    files = mods.getCreationTime(currentFolder,debug)
                    files_cleaned_currentFolder,files_renamed_currentFolder = mods.determineRemoveOrBackup(files,hostType,logfile,currentFolder,debug)
                g_files_cleaned.append(files_cleaned_currentFolder)
                g_files_renamed.append(files_renamed_currentFolder)
                        
            if debug:
                print("[DEBUG] HostType: {}".format(hostType))
                print("[DEBUG] backupRootPath: {}".format(backupRootPath))

        logfile.write("{} Files verwijderd: {}\n".format(datetime.today(),len(g_files_cleaned)))
        logfile.write("{} Files hernoemd: {}\n".format(datetime.today(),len(g_files_renamed)))

        message_text = """\
        De cleanup van oude files van {hostname} is succesvol voltooid.\n\n
        Het totaal aantal verwijderde bestanden is: {totalFilesCleaned}\n
        Het totaal aantal hernoemde bestanden is: {totalFilesRenamed}\n\n
        Zie ook bijgande logfile\n""".format(hostname=hostname,totalFilesCleaned=len(g_files_cleaned),totalFilesRenamed=len(g_files_renamed))
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
