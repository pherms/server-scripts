import tarfile
import zipfile
import os.path
import modules as mods
from datetime import datetime

def openArchiveWrite(filename,filetype,compression):
    if filetype == 'tar':
        # with tarfile.open(filename,'w:bz2') as bz2archive:
        bz2archive = tarfile.open(filename,'w:bz2')
        return bz2archive
    elif filetype == 'zip':
        ziparchive = zipfile.ZipFile(filename,'w', allowZip64=True)
        return ziparchive
        
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

    if filetype == 'tar':
        archive.add(fileToZip)
    elif filetype == 'zip':
        archive.write(fileToZip)

def determineInclusion(fileToZip):
    if str(fileToZip).startswith("+"):
        return True
    else:
        return False
    
def prepareFileToZip(line):
    line = line[1:].rstrip()
    return line