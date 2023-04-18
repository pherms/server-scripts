import tarfile
import zipfile

def openArchiveWrite(filename,filetype):
    if filetype == 'tar':
        with tarfile.open(filename,'w:bz2') as bz2archive:
            return bz2archive
    elif filetype == 'zip':
        with zipfile.ZipFile(filename,'w', allowZip64=True) as ziparchive:
            return ziparchive
        
def closeArchiveWrite(archive,filetype):
    if filetype == 'tar':
        archive.close()
    elif filetype == 'zip':
        archive.close()

def addFilesToArchive(archive,fileToZip,filetype):
    if filetype == 'tar':
        archive.add(fileToZip)
    if filetype == 'zip':
        archive.write(fileToZip)