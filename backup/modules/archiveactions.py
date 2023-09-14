import tarfile
import zipfile
import modules as mods
from datetime import datetime

def openArchiveWrite(filename,filetype,logfile,debug):
    """
    Open an archive to write to. The archive can be a tar.bz2 file or a zip file
    
    :param str filename: de naam van het archief bestand wat moet worden geopend
    :param str filetype: het bestandstype van het archief. Mogelijke opties zijn bz2 en zip. configureerbaar in config.json
    :logfile obj logfile: het open logbestand waar naartoe wordt gelogd
    :return: het geopende archief in schrijf modus
    :rtype: obj
    """
    try:
        if filetype == 'tar':
            # with tarfile.open(filename,'w:bz2') as bz2archive:
            bz2archive = tarfile.open(filename,'w:bz2')
            backuparchive = bz2archive
        elif filetype == 'zip':
            ziparchive = zipfile.ZipFile(filename,'w', allowZip64=True)
            backuparchive = ziparchive

        if debug:
            print("[DEBUG] het backup archief {} is gereed".format(filename))
        
        return backuparchive
        
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

def archiveSize(num, suffix="B"):
    """
    Functie voor het converteren van bytes naar human readable

    :param int num: De waarde in bytes
    :return: string in human readable vorm
    :rtype: str
    """
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
