# import sys
# sys.path.append('./modules')
# from modules import readtext as readtext
import modules as mods
from pathlib import Path
# from .modules/readsource import *
# dir(readsource)

def main():
    config = mods.readConfig()

    server = config["server"]
    filename = config["filename"]
    compression = config["compression"]
    filesize = config["filesize"]
    filetype = config["filetype"]
    
    lines = mods.readSourcesFile()
    archive = mods.openArchiveWrite(filename,filetype)
    print(archive)

    for line in lines:
        if filetype == 'tar':
            mods.makeTarFile(filename,Path(line.rstrip()))

    
        if (mods.isDirectory(line)):
            print('Directory!')
        else:
            print('File')
    
    

    

if __name__ == '__main__':
    main()