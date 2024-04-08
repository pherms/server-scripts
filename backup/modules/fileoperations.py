import os
import re
import time
import getpass
import subprocess
import calendar
import modules as mods
from pathlib import Path
from datetime import datetime, date

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

def generateFileName(hostname,filetype,compression,logfile,debug):
    """
    Genereert een archief filename aan de hand van een aantal parameters. Geeft de waarde terug.

    :param str hostname: de hostname van het systeem
    :param str filetype: de filetype van het archief. Is configureerbaar in config.json
    :param str compression: het type compressie van het archief. Is configureerbaar in config.json
    :param bool debug: enable debug logging
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
    
    if debug:
        print("[DEBUG] Gegenereerde backup filename: {}".format(filename))
        
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

def getCreationTime(backuppath,debug):
    """
    Vraagt van ieder bestand in de directory de creation date op en slaat dit op in een dictionary object

    :param str directory: de directory waarvan de bestanden moeten worden uitgelezen.
    :return: een dictionary object met bestandsnamen en de bijbehorende creatie tijden
    :rtype: dictionary
    """
    # create an empty dictionary to store the file names and creation times
    file_times = {}
    # loop through all the files in the directory
    for file in os.listdir(backuppath):
        # get the full path of the file
        file_path = os.path.join(backuppath, file)
        # get the creation time of the file in seconds since epoch
        creation_time = os.path.getctime(file_path)        
        # convert the creation time to a human-readable format
        creation_time = time.ctime(creation_time)
        creation_datetime = datetime.strptime(creation_time,'%a %b %d %H:%M:%S %Y')
        # store the file name and creation time in the dictionary
        file_times[file] = creation_datetime.date()
    # return the dictionary
    if debug:
        print("[DEBUG] file times dictionary {}".format(file_times))

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

def renameBackupFile(backuppath,fileName,logfile,type,debug):
    """
    Rename de backup file naar week of maand.

    :param str backuppath: het volledige pad waar de backup file gevonden kan worden
    :param str fileName: het backup bestand wat moet worden hernoemd naar maand of week
    :param str logfile: het logfile object waar naartoe moet worden gelogd
    :param str type: Het type waar het bestand naar kan worden hernoemd. Mogelijke opties zijn: week en month
    :param bool debug: Inschakelen van debug logging. Er worden geen bestanden hernoemd
    """
    
    if fileName.split('.')[1] == "tar":
        if type == 'week':
            logfile.write("{} Hernoemen van bestand {} naar weekbackup\n".format(datetime.today(),backuppath + fileName))
            fileNameArray = fileName.split('.')
            fileNameNew = backuppath + fileNameArray[0] + '-week.' + fileNameArray[1] + '.' + fileNameArray[2]
            if not debug:
                os.rename(backuppath + fileName,fileNameNew)
            else:
                print("[DEBUG] {} wordt hernoemd naar {}".format(fileName,fileNameNew))
                logfile.write("{} [DEBUG] {} wordt hernoemd naar {}\n".format(datetime.today(),fileName,fileNameNew))
        
        if type == 'month':
            logfile.write("{} Hernoemen van bestand {} naar maandbackup\n".format(datetime.today(),backuppath + fileName))
            fileNameArray = fileName.split('.')
            fileNameNew = backuppath + fileNameArray[0].replace('-week','') + '-month.' + fileNameArray[1] + '.' + fileNameArray[2]
            if not debug:
                os.rename(backuppath + fileName,fileNameNew)
            else:
                print("[DEBUG] {} wordt hernoemd naar {}".format(fileName,fileNameNew))
                logfile.write("{} [DEBUG] {} wordt hernoemd naar {}\n".format(datetime.today(),fileName,fileNameNew))

    elif fileName.split('.')[-1] == "zip":
        if type == 'week':
            logfile.write("{} Hernoemen van bestand {} naar weekbackup\n".format(datetime.today(),backuppath + fileName))
            if not debug:
                os.rename(backuppath + fileName,backuppath + fileName.split('.')[0] + '-week.' + fileName.split('.')[1])
            else:
                print("[DEBUG] {} wordt hernoemd naar {}".format(fileName,fileName.split('.')[0] + '-week.' + fileName.split('.')[1]))
                logfile.write("{} [DEBUG] {} wordt hernoemd naar {}\n".format(datetime.today(),fileName,fileName.split('.')[0] + '-week.' + fileName.split('.')[1]))
        else:
            logfile.write("{} Hernoemen van bestand {} naar maandbackup\n".format(datetime.today(),backuppath + fileName))
            if not debug:
                os.rename(backuppath + fileName,backuppath + fileName.split('.')[0].replace('-week','') + '-month.' + fileName.split('.')[1])  
            else:
                print("[DEBUG] {} wordt hernoemd naar {}".format(fileName,fileName.split('.')[0] + '-month.' + fileName.split('.')[1]))
                logfile.write("{} [DEBUG] {} wordt hernoemd naar {}\n".format(datetime.today(),fileName,fileName.split('.')[0].replace('-week','') + '-month.' + fileName.split('.')[1]))

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

def determineRemoveOrBackup(files,hostType,logfile,backuppath,debug):
    """
    Bepalen of de backup file moet worden hernoemd of verwijderd

    :param str backuppath: het volledige pad waar de backup file gevonden kan worden
    :param str files: de array met files die moeten worden gerenamed, dan wel verwijderd
    :param str logfile: het logfile object waar naartoe moet worden gelogd
    :param str hostType: het host type waarop het script moet worden uitgevoerd. 2 opties: vm en host
    :param bool debug: Debug toggle. Wanneer true, dan worden geen files verwijderd
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
            backupFileDate = mods.determineCreationDateFromFileName(file,debug)
            folderArray = fileName.split('/')
            backupFolder = folderArray[:-1]
            fileName = folderArray[-1]
            backuppath = '/'.join(backupFolder) + '/'

            if debug:
                print("[DEBUG] BackupFileDate {}".format(backupFileDate))
                print("[DEBUG] folderArray {}".format(folderArray))
                print("[DEBUG] backupFolder {}".format(backupFolder))
                print("[DEBUG] fileName {}".format(fileName))
                print("[DEBUG] backuppath {}".format(backuppath))

        # behouden
        dag = date.fromisoformat(backupFileDate).isocalendar()[2]
        currentDag = date.fromisoformat(datetime.strftime(datetime.now(),'%Y-%m-%d')).isocalendar()[2]

        ageInDays = (datetime.now() - datetime.strptime(backupFileDate, '%Y-%m-%d')).days

        logfile.write("{} Beoordelen van bestand: {}\n".format(datetime.today(),file))
        try:
            # backup dag 7 hernoemen naar week
            if dag == 7 and not ("week" in fileName or "month" in fileName):
                if debug:
                        print("[DEBUG] {} wordt hernoemd naar week backup".format(fileName))
                        logfile.write("{} [DEBUG] {} wordt hernoemd naar week backup\n".format(datetime.today(),fileName))

                mods.renameBackupFile(backuppath,fileName,logfile,"week",debug)
                files_renamed.append(fileName)
            
            # oude dag en week backups verwijderen
            if dag < 7  and ageInDays >= 7 and not ("week" in fileName or "month" in fileName) and not dag == currentDag:
                if not debug:
                    # remove file
                    mods.removeBackupFile(backuppath,fileName,logfile)
                    files_cleaned.append(fileName)
                else:
                    print("[DEBUG] {} wordt verwijderd.".format(fileName))
                    logfile.write("{} [DEBUG] {} wordt verwijderd\n".format(datetime.today(),fileName))

            # oudste weekbackup hernoemen naar month. max age in weeks 4
            if ageInDays >= 28 and "week" in fileName and not "month" in fileName:
                if debug:
                    print("[DEBUG] {} wordt hernoemd naar maand backup".format(fileName))
                    logfile.write("{} [DEBUG] {} wordt hernoemd naar maand backup\n".format(datetime.today(),fileName))

                # rename file
                mods.renameBackupFile(backuppath,fileName,logfile,"month",debug)
                files_renamed.append(fileName)

                # oude weekbackup verwijderen
                if ageInDays in range(7,27) and "week" in fileName:
                    if not debug:
                        mods.removeBackupFile(backuppath,fileName,logfile)
                        files_cleaned.append(fileName)
                    else:
                        print("[DEBUG] {} wordt verwijderd.".format(fileName))
                        logfile.write("{} [DEBUG] {} wordt verwijderd\n".format(datetime.today(),fileName))

            # Oude Maand backup verwijderen, welke niet de laatste vrijdag van de maand als datum heeft.
            if "month" in fileName:
                jaar = backupFileDate.year
                maand = backupFileDate.month
                dag = int(backupFileDate.day)

                laatsteVrijdag = int(determineLastFridayOfMonth(jaar,maand))
                print("Laatste vrijdag: {}".format(laatsteVrijdag))
                if not debug:
                    if dag != laatsteVrijdag:
                        mods.removeBackupFile(backuppath,fileName,logfile)
                        files_cleaned.append(fileName)
                else:
                    print("[DEBUG] {} wordt verwijderd.".format(fileName))
                    logfile.write("{} [DEBUG] {} wordt verwijderd\n".format(datetime.today(),fileName))

            # oude maand backup verwijderen. max age in months 3 (12 weken, ~84 dagen)
            if ageInDays >= 84 and "month" in fileName:
                if not debug:
                    mods.removeBackupFile(backuppath,fileName,logfile)
                    files_cleaned.append(fileName)
                else:
                    print("[DEBUG] {} wordt verwijderd.".format(fileName))
                    logfile.write("{} [DEBUG] {} wordt verwijderd\n".format(datetime.today(),fileName))
        except Exception:
            
            print(Exception)
            
            
            exit()

    return files_cleaned,files_renamed

def determineCreationDateFromFileName(fileName,debug):
    """
    Bepalen van de creation date van de backupfile op basis van de datum in de bestandsnaam

    :param fileName: het backup bestand waarvan de creation date moet worden bepaald.
    :param debug: debug toggle voor het tonen van extra informatie.
    :return: datetime object
    :rtype: obj
    """
    regexPattern = "(?<=-)\d+"
    match = re.search(regexPattern,fileName)
    creationDateString = match[0]
    
    if len(creationDateString) == 6:
        creationDate = datetime.strftime(datetime.strptime(creationDateString, '%y%m%d'), '%Y-%m-%d')
    else:
        creationDate = datetime.strftime(datetime.strptime(creationDateString, '%Y%m%d'), '%Y-%m-%d')
    
    if debug:
        print("[DEBUG] creationDate of file {} is: {}".format(fileName,creationDate))

    return creationDate

def determineLastFridayOfMonth(year,month):
    """
    Functie om de laatste vrijdag van de maand te bepalen

    :param int year: Het jaar
    :param bool month: De maand waarvan de laatste vrijdag moet worden bepaald.
    :return: integer dagnummer
    """
    last_day = calendar.monthrange(year, month)[1]
    last_weekday = calendar.weekday(year, month, last_day)
    last_friday = last_day - ((7 - (4 - last_weekday)) % 7)

    return last_friday

def cleanupLogs(logPath,debug):
    """
    Opschonen van de log directory.

    :param str logPath: Het pad waar de logfiles worden opgeslagen
    :param bool debug: Debug toggle. Er wordt meer info weergegeven in de console of logfile
    """
    for file in os.listdir(logPath):
        if file != 'updatelog.log':
            logfileDate = mods.determineCreationDateFromFileName(file,debug)
            if debug:
                print("[DEBUG] logfileDate: {}".format(logfileDate))

            ageInDays = (datetime.now() - datetime.strptime(logfileDate, '%Y-%m-%d')).days
            
            if ageInDays >= 84:
                if debug:
                    print("[DEBUG] het bestand {} zou worden verwijderd wanneer debugging=True".format(file))
                else:
                    os.remove(logPath + file)

def getArchiveFileSize(archive):
    """
    Opvragen van bestand grootte van het backup bestand in Human Readable formaat

    :param archive: Het archief bestand waarvan de grootte moet worden bepaald
    :retrun: str: de waarde in human readable formaat
    """
    fullArchivePath = os.path.abspath(archive.name)
    sizeHumanReadable = mods.archiveSize(os.path.getsize(fullArchivePath))

    return sizeHumanReadable