import tarfile
import zipfile
import os
import modules as mods
from datetime import datetime
from pathlib import Path

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

def addFilesToArchive(archive,filetype,logfile,listToBackup,debug):
    """
    Toevoegen van bestand aan archief
    
    :param obj archive: het archief bestand waar het bestand naar toe moet worden geschreven
    :param str filetype: het type archief wat moet worden gesloten. Mogelijke opties zijn bz2 en zip. configureerbaar in config.json
    :param obj logfile: het open logbestand waar naartoe wordt gelogd
    :param list listToBackup: Lijst met te backuppen bestanden en directories
    :param bool debug: Enable debug print in de console
    :return: success of failure
    :rtype: str
    """
    for folderToBackup in listToBackup:
        errorMessage = ""
        folderToBackup = Path(folderToBackup)

        if debug:
            print("[DEBUG] Backuppen van folder: {}".format(folderToBackup))

        if mods.isDirectory(folderToBackup):
            logfile.write("{} Backup directory {}\n".format(datetime.today(),folderToBackup))
        else:
            logfile.write("{} Backup file {}\n".format(datetime.today(),folderToBackup))

        try:
            if filetype == 'tar':
                try:
                    archive.add(folderToBackup)
                except IOError as ioError:
                    errorMessage = str(ioError)
                    pass
            elif filetype == 'zip':
                archive.write(folderToBackup)
        except Exception:
            if errorMessage != "":
                logmessage = "{}\n".format(datetime.today(),errorMessage)

            logmessage = "{} Kan {} niet naar backup archief schrijven. Backup wordt afgebroken.\n".format(datetime.today(),folderToBackup)
            logfile.write(logmessage)
            mods.sendMailFailedBackup(mods.getHostname(logfile),logmessage)
            closeArchiveWrite(archive,folderToBackup)
            exit()
    
    return "success"

def determineFolderlists(line,exclusionList,inclusionList,debug): # line uit sources
    """
    Bepaal of een bestand of directory moet worden meegenomen in de backup of uitgesloten.
    De notatie in het sources bestand is:
    +/etc
    -/etc/default

    Dit zorgt ervoor dat de volledige folder /etc wordt gebackupped, met uitzondering van de default folder in de /etc folder

    :param str line: de regel uit het sources bestand, welke moet worden geevalueerd
    :param list inclusionList: een lijst met te backup bestanden
    :param list exclusionList: een lijst met te skippen bestanden en directories
    :param bool debug: enable debug logging
    """
    if str(line).startswith("-"):
        if debug:
            print("[DEBUG] toevoegen pad {} aan exclusionlist.".format(line))
        exclusionList.insert(len(exclusionList),line[1:].rstrip())
    elif str(line).startswith("+"):
        if debug:
            print("[DEBUG] toevoegen pad {} aan inclusionlist.".format(line))
        inclusionList.insert(len(inclusionList),line[1:].rstrip())

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

def prepareSourceListToBackup(logfile,listToBackup,exclusionList,inclusionList,debug):
    """
    Prepare sources to bakup and exclude de exclusions

    :param str line: de folder uit de sources file
    :param list listToBackup: Lijst met folders welke moet worden gebackupped
    :param list exclusionList: Lijst met folders welke moeten worden geskipped
    :param bool debug: debug print op console. true is aan
    """
    logfile.write("{} Bepalen van te backuppen folders\n".format(datetime.today()))
    for inclusion in inclusionList:
        for root, dirs, files in os.walk(Path(inclusion)):
            for file in files:
                listToBackup.append(os.path.join(root,file))

    logfile.write("{} Filteren van de exclusies\n".format(datetime.today()))
    for exclusion in exclusionList:
        while True:
            indexes = [index for index in range(len(listToBackup)) if exclusion in listToBackup[index]]
            if not len(indexes) == 0:
                if debug:
                    print("[DEBUG] found matches: {}".format(indexes))
                for index in indexes:
                    listToBackup.pop(indexes[0])
            else:
                break

    if debug:
        print("[DEBUG] lijst met folders die worden gebackupped: {}".format(listToBackup))