import os
import time
from pathlib import Path
from datetime import datetime

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
