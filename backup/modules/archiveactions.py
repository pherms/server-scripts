import tarfile
import zipfile
import subprocess
import modules as mods
import getpass
from datetime import datetime
from datetime import date

def openArchiveWrite(filename,filetype,compression,logfile):
    """
    Open an archive to write to. The archive can be a tar.bz2 file or a zip file
    
    :param str filename: de naam van het archief bestand wat moet worden geopend
    :param str filetype: het bestandstype van het archief. Mogelijke opties zijn bz2 en zip. configureerbaar in config.json
    :param str compression: het niveau van compressie. configureerbaar in config.json
    :logfile obj logfile: het open logbestand waar naartoe wordt gelogd
    :return: het geopende archief in schrijf modus
    :rtype: obj
    """
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
    """
    Sluit het archief bestand
    
    :param obj archive: het archief bestand wat moet worden gesloten
    :param str filetype: het type archief wat moet worden gesloten. Mogelijke opties zijn bz2 en zip. configureerbaar in config.json
    """
    if filetype == 'tar':
        archive.close()
    elif filetype == 'zip':
        archive.close()

def addFilesToArchive(archive,fileToZip,filetype,logfile):
    """
    Toevoegen van bestand aan archief
    
    :param obj archive: het archief bestand waar het bestand naar toe moet worden geschreven
    :param str fileToZip: het bestand wat naar het archief moet worden geschreven
    :param str filetype: het type archief wat moet worden gesloten. Mogelijke opties zijn bz2 en zip. configureerbaar in config.json
    :logfile obj logfile: het open logbestand waar naartoe wordt gelogd
    """
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
    """
    Bepaal of een bestand of directory moet worden meegenomen in de backup of uitgesloten.
    De notatie in het sources bestand is:
    +/etc
    -/etc/default

    Dit zorgt ervoor dat de volledige folder /etc wordt gebackupped, met uitzondering van de default folder in de /etc folder

    :param str fileToZip: de regel uit het sources bestand, welke moet worden geevalueerd
    :return: True of False
    :rtype: bool
    """
    if str(fileToZip).startswith("+"):
        return True
    else:
        return False
    
def prepareFileToZip(line):
    """
    Verwijdert de verborgen tekens aan het einde van een regel uit het sources bestand

    :param str line: de regel uit het sources bestand, waarvan de verborgen tekens moeten worden verwijderd
    :return: de 'line' string
    :rtype: str
    """
    line = line[1:].rstrip()
    return line

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
        backupDestination = username + "@" + backupserver + ":" + remotefilepath + hostname
        subprocess.run([copycommand,backupFullFile,backupDestination])
        logfile.write("{} {} naar de backuplocatie {} gekopieerd\n".format(datetime.today(),backupFullFile,backupDestination))
    except Exception:
        logmessage = "{} Kan {} niet naar de backuplocatie {} kopieren\n".format(datetime.today(),backupFullFile,backupDestination)
        logfile.write(logmessage)
        mods.sendMailFailedCopyToServer(mods.getHostname(logfile),logmessage)
        exit()