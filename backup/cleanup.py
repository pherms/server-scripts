# import datetime
from datetime import *
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
            print('[cleanup.py] Inhoud van files array bij vm: {}'.format(files))

            files_cleaned,files_renamed = mods.determineRemoveOrBackup(files,hostType,logfile,backuppath)
            # for file in files.keys():
            #     fileName = file
            #     backupFileDate = datetime.strftime(files.get(fileName),'%Y-%m-%d')

            #     jaar,week,dag = date.fromisoformat(backupFileDate).isocalendar()[:3]
            #     currentJaar,currentWeek,currentDag = date.fromisoformat(datetime.strftime(datetime.now(),'%Y-%m-%d')).isocalendar()[:3]

            #     logfile.write("{} Beoordelen van bestand: {}\n".format(datetime.today(),file))

            #     # backup dag 7 hernoemen naar week
            #     if dag == 7:
            #         mods.renameBackupFile(backuppath,fileName,logfile,"week")
            #         files_renamed.append(fileName)

            #     # oude dag backups verwijderen
            #     if dag < 7  and week == currentWeek -1 and not ("week" in fileName or "month" in fileName) and not dag == currentDag:
            #         # remove file
            #         mods.removeBackupFile(backuppath,fileName,logfile)
            #         files_cleaned.append(fileName)

            #     # oudste weekbackup hernoemen naar month
            #     if week == currentWeek - 4:
            #         # rename file
            #         mods.renameBackupFile(backuppath,fileName,logfile,"month")
            #         files_renamed.append(fileName)

            #     # oude weekbackup verwijderen
            #     if (week in range(currentWeek - 4,currentWeek - 1)) and not "month" in fileName:
            #         mods.removeBackupFile(backuppath,fileName,logfile)
            #         files_cleaned.append(fileName)
        elif hostType == 'host':
            # 1. voor elke folder in backuppath get files -> array
            # 2. for elk bestand in array -> determineRemoveOrRename()
            print('[cleanup.py]HostType detecteerd: {}'.format(hostType))
            filesArray = {}
            for folder in os.listdir(backuppath):
                print('[cleanup.py]BackupPath from config: {}'.format(backuppath))
                print('[cleanup.py]Folder of file naam: {}'.format(folder))
                if mods.isDirectory(backuppath + folder):
                    print('[cleanup.py]Folder name is: {}'.format(folder))
                    for file in os.listdir(backuppath + folder):
                        fullFile = os.path.abspath(backuppath + folder + '/' + file)
                        print('[cleanup.py]Full filename: {}'.format(fullFile))
                        filesArray[fullFile] = "nothing"
                        print('FilesArray: {}'.format(filesArray))

            files_cleaned,files_renamed = mods.determineRemoveOrBackup(filesArray,hostType,logfile,backuppath)
            
            print('[cleanup.py]Files cleaned: {}'.format(files_cleaned))
            print('[cleanup.py]Files renamed: {}'.format(files_renamed))



        logfile.write("{} Files verwijderd: {}\n".format(datetime.today(),len(files_cleaned)))
        logfile.write("{} Files hernoemd: {}\n".format(datetime.today(),len(files_renamed)))

        message_text = """\
        De cleanup van oude files van {hostname} is succesvol voltooid.\n\n
        Het totaal aantal verwijderde bestanden is: {totalFilesCleaned}\n
        Het totaal aantal hernoemde bestanden is: {totalFilesRenamed}\n\n
        Zie ook bijgande logfile\n""".format(hostname=hostname,totalFilesCleaned=len(files_cleaned),totalFilesRenamed=len(files_renamed))
        subject = "Cleanup van files naar op server {} succesvol".format(hostname)
        
        mods.closeLogFile(logfile)
        mods.sendMail(subject,message_text,logfile)

    except Exception:
        message="Cleanup van server {} is gefaald\n".format(hostname)
        mods.sendMailFailedCleanup(hostname,message)

if __name__ == '__main__':
    main()
