import os
import re
import time
import getpass
import subprocess
import modules as mods
from pathlib import Path
from datetime import datetime, date, timedelta

def isDirectory(path):
    """
    Bepaald of de waarde van het argument een bestand of een directory is. Geeft een boolean waarde terug

    :param str path: het pad wat moet worden geevalueerd.
    :return: True of False
    :rtype: bool
    """
    p = Path(path)
    isDirectory = p.is_dir()
    
    return isDirectory

def generateFileName(hostname,filetype,compression,logfile):
    """
    Genereert een archief filename aan de hand van een aantal parameters. Geeft de waarde terug.

    :param str hostname: de hostname van het systeem
    :param str filetype: de filetype van het archief. Is configureerbaar in config.json
    :param str compression: het type compressie van het archief. Is configureerbaar in config.json
    :param obj logfile: de logfile waar naartoe moet worden gelogd
    :return: de bestandsnaam voor het archief
    :rtype: str
    """
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
    """
    Maakt een folder met de naam van het opgegeven argument. Wanneer deze al bestaat wordt er een melding weergegeven

    :param str folder: de naam van de folder, die moet worden gemaakt.
    """
    try:
        Path(folder).mkdir(mode=0o755,parents=True)
    except FileExistsError:
        print("{} Folder {} bestaat al".format(datetime.today(),folder))
    else:
        print("{} Folder {} gemaakt".format(datetime.today(),folder))

def getCreationTime(directory):
    """
    Vraagt van ieder bestand in de directory de creation date op en slaat dit op in een dictionary object

    :param str directory: de directory waarvan de bestanden moeten worden uitgelezen.
    :return: een dictionary object met bestandsnamen en de bijbehorende creatie tijden
    :rtype: dictionary
    """
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

def copyFileToServer(backupFullFile,backupserver,copycommand,remotefilepath,logfile,hostname):
    """
    Kopieer de backupfile naar een locatie op een andere server.

    :param str backupFullFile: het bestand met volledig pad wat moet worden gekopieerd
    :param str backupserver: de server waar het bestand naartoe moet worden geschreven. configureerbaar in config.json
    :param str copycommand: het commando waarmee moet worden gekopieerd. configureerbaar in config.json
    :param str remotefilepath: het pad op de server waar het bestand naartoe moet worden geschreven. configureerbaar in config.json
    :param str logfile: het logfile object waar naartoe moet worden gelogd
    :param str hostname: de hostname van de machine waar vandaan het backup bestand wordt geschreven. configureerbaar in config.json. Wanneer niet opgegeven, dan wordt de hostname van het systeem opgevraagd
    """
    try:
        username = getpass.getuser()
        print("Username is: {}".format(username))
        backupDestination = username + "@" + backupserver + ":" + remotefilepath + hostname + "/"
        subprocess.run([copycommand,backupFullFile,backupDestination]).stdout
        logfile.write("{} {} naar de backuplocatie {} gekopieerd\n".format(datetime.today(),backupFullFile,backupDestination))
    except Exception:
        logmessage = "{} Kan {} niet naar de backuplocatie {} kopieren\n".format(datetime.today(),backupFullFile,backupDestination)
        print(Exception)
        logfile.write(logmessage)
        mods.sendMailFailedCopyToServer(mods.getHostname(logfile),logmessage)
        exit()

def renameBackupFile(backuppath,fileName,logfile,type):
    """
    Rename de backup file naar week of maand.

    :param str backuppath: het volledige pad waar de backup file gevonden kan worden
    :param str fileName: het backup bestand wat moet worden hernoemd naar maand of week
    :param str logfile: het logfile object waar naartoe moet worden gelogd
    :param str type: Het type waar het bestand naar kan worden hernoemd. Mogelijke opties zijn: week en month
    """
    
    if fileName.split('.')[1] == "tar":
        if type == 'week':
            logfile.write("{} Hernoemen van bestand {} naar weekbackup\n".format(datetime.today(),backuppath + fileName))
            fileNameArray = fileName.split('.')
            fileNameNew = backuppath + fileNameArray[0] + '-week.' + fileNameArray[1] + '.' + fileNameArray[2]
            os.rename(backuppath + fileName,fileNameNew)
        
        if type == 'month':
            logfile.write("{} Hernoemen van bestand {} naar maandbackup\n".format(datetime.today(),backuppath + fileName))
            fileNameArray = fileName.split('.')
            fileNameNew = backuppath + fileNameArray[0] + '-month.' + fileNameArray[1] + '.' + fileNameArray[2]
            os.rename(backuppath + fileName,fileNameNew)

    elif fileName.split('.')[-1] == "zip":
        if type == 'week':
            logfile.write("{} Hernoemen van bestand {} naar weekbackup\n".format(datetime.today(),backuppath + fileName))
            os.rename(backuppath + fileName,backuppath + fileName.split('.')[0] + '-week.' + fileName.split('.')[1])
        else:
            logfile.write("{} Hernoemen van bestand {} naar maandbackup\n".format(datetime.today(),backuppath + fileName))
            os.rename(backuppath + fileName,backuppath + fileName.split('.')[0] + '-month.' + fileName.split('.')[1])  

def removeBackupFile(backuppath,fileName,logfile):
    """
    Het verwijderen van oude backup bestanden

    :param str backuppath: het volledige pad waar de backup file gevonden kan worden
    :param str fileName: het backup bestand wat moet worden hernoemd naar maand of week
    :param str logfile: het logfile object waar naartoe moet worden gelogd
    """
    print(f"verwijderen dagbackup file: {fileName}")
    logfile.write("{} Verwijderen van bestand {}\n".format(datetime.today(),fileName))
    os.remove(backuppath + fileName)
    logfile.write("{} Bestand {} zou verwijderd zijn\n".format(datetime.today(),backuppath + fileName))

def determineRemoveOrBackup(files,hostType,logfile,backuppath):
    """
    Bepalen of de backup file moet worden hernoemd of verwijderd

    :param str backuppath: het volledige pad waar de backup file gevonden kan worden
    :param str files: de array met files die moeten worden gerenamed, dan wel verwijderd
    :param str logfile: het logfile object waar naartoe moet worden gelogd
    :param str hostType: het host type waarop het script moet worden uitgevoerd. 2 opties: vm en host
    :return: een tuple, bestaande uit files_cleaned en files_renamed
    :rtype: tuple
    """
    files_cleaned = []
    files_renamed = []

    for file in files.keys():
        fileName = file
        
        if hostType == 'vm':
            backupFileDate = datetime.strftime(files.get(fileName),'%Y-%m-%d')
            
        elif hostType == 'host':
            backupFileDate = mods.determineCreationDateFromFileName(file)
            folderArray = fileName.split('/')
            backupFolder = folderArray[:-1]
            fileName = folderArray[-1]
            backuppath = '/'.join(backupFolder) + '/'

        # behouden
        dag = date.fromisoformat(backupFileDate).isocalendar()[2]
        currentDag = date.fromisoformat(datetime.strftime(datetime.now(),'%Y-%m-%d')).isocalendar()[2]

        ageInDays = (datetime.now() - datetime.strptime(backupFileDate, '%Y-%m-%d')).days

        logfile.write("{} Beoordelen van bestand: {}\n".format(datetime.today(),file))

        # backup dag 7 hernoemen naar week
        if dag == 7 and not ("week" in fileName or "month" in fileName):
            mods.renameBackupFile(backuppath,fileName,logfile,"week")
            files_renamed.append(fileName)

        # oude dag en week backups verwijderen
        if dag < 7  and ageInDays >= 7 and not ("week" in fileName or "month" in fileName) and not dag == currentDag:
            # remove file
            mods.removeBackupFile(backuppath,fileName,logfile)
            files_cleaned.append(fileName)

        # oudste weekbackup hernoemen naar month. max age in weeks 4
        if ageInDays >= 28 and "week" in fileName and not "month" in fileName:
            # rename file
            mods.renameBackupFile(backuppath,fileName,logfile,"month")
            files_renamed.append(fileName)

        # oude weekbackup verwijderen
        if ageInDays in range(7,28) and not "month" in fileName and "week" in fileName:
            mods.removeBackupFile(backuppath,fileName,logfile)
            files_cleaned.append(fileName)

        # oude maand backup verwijderen. max age in months 3 (12 weken, ~84 dagen)
        if ageInDays >= 84 and "month" in fileName:
            mods.removeBackupFile(backuppath,fileName,logfile)
            files_cleaned.append(fileName)

    return files_cleaned,files_renamed

def determineCreationDateFromFileName(fileName):
    """
    Bepalen van de creation date van de backupfile op basis van de datum in de bestandsnaam

    :param fileName: het backup bestand waarvan de creation date moet worden bepaald.
    :return: datetime object
    :rtype: obj
    """
    regexPattern = "(?<=-)\d+"
    match = re.search(regexPattern,fileName)
    creationDateString = match[0]

    creationDate = datetime.strftime(datetime.strptime(creationDateString, '%Y%m%d'), '%Y-%m-%d')
    
    return creationDate

def cleanupLogs(logPath):
    """
    Opschonen van de log directory.

    :param logPath: Het pad waar de logfiles worden opgeslagen
    """
    for file in os.listdir(logPath):
        logfileDate = mods.determineCreationDateFromFileName(file)
        
        if len(logfileDate) == 6:
            logfileDate = '20' + logfileDate
        
        ageInDays = (datetime.now() - datetime.strptime(logfileDate, '%Y-%m-%d')).days
        
        if ageInDays >= 84:
            os.remove(os.path.abspath(file))