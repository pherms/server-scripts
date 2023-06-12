# import datetime
from datetime import *
import os
import modules as mods

def main():
    config = mods.readConfig()
    
    backuppath = config["backuppath"]
    logfilepath = config["logfilepath"]

    logfile = mods.openLogFile(logfilepath,"cleanup")
    files = mods.getCreationTime(backuppath)
    hostname = mods.getHostname(logfile)
    
    files_cleaned = []
    files_renamed = []

    # try:
    for file in files.keys():
        fileName = file
        backupFileDate = datetime.strftime(files.get(fileName),'%Y-%m-%d')

        jaar,week,dag = date.fromisoformat(backupFileDate).isocalendar()[:3]
        currentJaar,currentWeek,currentDag = date.fromisoformat(datetime.strftime(datetime.now(),'%Y-%m-%d')).isocalendar()[:3]

        # backup dag 7 hernoemen naar week
        if dag == 7:
            logfile.write("{} Hernoemen van bestand {} naar weekbackup\n".format(datetime.today(),fileName))
            if fileName.split('.')[1] == "tar":
                fileNameArray = fileName.split('.')
                fileNameNew = backuppath + fileNameArray[0] + '-week.' + fileNameArray[1] + '.' + fileNameArray[2]
                os.rename(backuppath + fileName,backuppath + fileNameNew)
            else:
                os.rename(backuppath + fileName,backuppath + fileName.split('.')[0] + '-week.' + fileName.split('.')[1])
            files_renamed.append(fileName)

        # oude dag backups verwijderen
        if dag < 7  and week == currentWeek -1 and not ("week" in fileName or "month" in fileName) and not dag == currentDag:
            # remove file
            print(f"verwijderen dagbackup file: {fileName}")
            logfile.write("{} Verwijderen van bestand {}\n".format(datetime.today(),fileName))
            # os.remove(backuppath + fileName)
            logfile.write("{} Bestand {} zou verwijderd zijn\n".format(datetime.today(),fileName))
            files_cleaned.append(fileName)

        # oudste weekbackup hernoemen naar month
        if week == currentWeek - 4:
            # rename file
            logfile.write("{} Hernoemen van bestand {} naar maandbackup\n".format(datetime.today(),fileName))
            if fileName.split('.')[1] == "tar":
                fileNameArray = fileName.split('.')
                fileNameNew = backuppath + fileNameArray[0] + '-month.' + fileNameArray[1] + '.' + fileNameArray[2]
                os.rename(backuppath + fileName,backuppath + fileNameNew)
            else:
                os.rename(backuppath + fileName,backuppath + fileName.split('.')[0] + '-month.' + fileName.split('.')[1])
            files_renamed.append(fileName)

        # oude weekbackup verwijderen
        if (week in range(currentWeek - 4,currentWeek - 1)) and not "month" in fileName:
            if not (week in range(currentWeek - 4,currentWeek - 1)):
                print(currentWeek - 4)
            # remove file
            print(range(currentWeek - 4, currentWeek - 1))
            print(f"verwijderen weekbackup file: {fileName}")
            logfile.write("{} Verwijderen van bestand {}\n".format(datetime.today(),fileName))
            # os.remove(backuppath + fileName)
            logfile.write("{} Bestand {} zou verwijderd zijn\n".format(datetime.today(),fileName))
            files_cleaned.append(fileName)

    logfile.write("{} Files verwijderd: {}\n".format(datetime.today(),len(files_cleaned)))
    logfile.write("{} Files hernoemd: {}\n".format(datetime.today(),len(files_renamed)))

    message_text = """\
    De cleanup van oude files van {hostname} is succesvol voltooid.\n\n
    Het totaal aantal verwijderde bestanden is: {totalFilesCleaned}\n
    Het totaal aantal hernoemde bestanden is: {totalFilesRenamed}\n\n
    Zie ook bijgande logfile\n""".format(hostname=hostname,totalFilesCleaned=len(files_cleaned),totalFilesRenamed=len(files_renamed))
    subject = "Kopieren van files naar van server {} succesvol".format(hostname)

    mods.sendMail(subject,message_text,logfile)
    # except Exception:
    #     message="Cleanup van server {} is gefaald\n".format(hostname)
    #     mods.sendMailFailedCleanup(hostname,message)

if __name__ == '__main__':
    main()
