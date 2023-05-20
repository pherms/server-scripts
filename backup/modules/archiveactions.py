import tarfile
import zipfile
import os.path
import modules as mods
from datetime import datetime
from datetime import date

def openArchiveWrite(filename,filetype,compression,logfile):
    try:
        if filetype == 'tar':
            # with tarfile.open(filename,'w:bz2') as bz2archive:
            bz2archive = tarfile.open(filename,'w:bz2')
            return bz2archive
        elif filetype == 'zip':
            ziparchive = zipfile.ZipFile(filename,'w', allowZip64=True)
            return ziparchive
    except Exception:
        logfile.write("{} Kan {} niet openen. Backup wordt afgebroken.\n".format(datetime.today(),filename))
        exit()
        
def closeArchiveWrite(archive,filetype):
    if filetype == 'tar':
        archive.close()
    elif filetype == 'zip':
        archive.close()

def addFilesToArchive(archive,fileToZip,filetype,logfile):
    if mods.isDirectory(fileToZip):
        logfile.write("{} Backup directory {}\n".format(datetime.today(),fileToZip))
    else:
        logfile.write("{} Backup file {}\n".format(datetime.today(),fileToZip))

    try:
        if filetype == 'tar':
            archive.add(fileToZip)
        elif filetype == 'zip':
            archive.write(fileToZip)
    except Exception:
        logfile.write("{} Kan {} niet naar backup archief schrijven. Backup wordt afgebroken.\n".format(datetime.today(),fileToZip))
        closeArchiveWrite(archive,fileToZip)
        exit()

def determineInclusion(fileToZip):
    if str(fileToZip).startswith("+"):
        return True
    else:
        return False
    
def prepareFileToZip(line):
    line = line[1:].rstrip()
    return line

def cleanupOldBackups(file):
    print("Cleanup old backup")
    dateModified = mods.getDateTime(file)
    
    week,dag = date.fromisoformat(dateModified).isocalendar()[:2]
    
    # Wanneer 7 dag backups, dan oudste verwijderen en de laatste wordt een weekbackup
    # wanneer 5 week backups, dan oudste verwijderen. Oudste wordt een maandbackup
    # wanneer 4 maand backups, dan de de oudste verwijderen
    
    print(week)
    print(dag)