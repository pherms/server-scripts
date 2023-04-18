# import sys
# sys.path.append('./modules')
# from modules import readtext as readtext
import modules as mods
# from .modules/readsource import *
# dir(readsource)

def main():
    config = mods.readConfig()

    server = config["server"]
    filename = config["filename"]
    compression = config["compression"]
    filesize = config["filesize"]
    
    lines = mods.readSourcesFile()
    for line in lines:
        
        if (mods.isDirectory(line)):
            print('Directory!')
        else:
            print('File')

    

if __name__ == '__main__':
    main()