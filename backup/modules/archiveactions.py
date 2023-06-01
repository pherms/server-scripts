import tarfile
import zipfile
import subprocess
import modules as mods
import getpass
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
        logmessage = "{} Kan {} niet openen. Backup wordt afgebroken.\n".format(datetime.today(),filename)
        logfile.write(logmessage)
        mods.sendMailFailedBackup(mods.getHostname(logfile),logmessage)
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
        logmessage = "{} Kan {} niet naar backup archief schrijven. Backup wordt afgebroken.\n".format(datetime.today(),fileToZip)
        logfile.write(logmessage)
        mods.sendMailFailedBackup(mods.getHostname(logfile),logmessage)
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

def copyFileToServer(backupFullFile,backupserver,copycommand,remotefilepath,logfile,hostname):
    try:
        username = getpass.getuser()
        backupDestination = username + "@" + backupserver + ":" + remotefilepath + hostname
        subprocess.run([copycommand,backupFullFile,backupDestination])
        logfile.write("{} {} naar de backuplocatie {} gekopieerd\n".format(datetime.today(),backupFullFile,backupDestination))
    except Exception:
        logmessage = "{} Kan {} niet naar de backuplocatie {} kopieren\n".format(datetime.today(),backupFullFile,backupDestination)
        logfile.write(logmessage)
        mods.sendMailFailedCopyToServer(mods.getHostname(logfile),logmessage)
        exit()