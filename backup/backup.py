# import sys
# sys.path.append('./modules')
# from modules import readtext as readtext
import modules as mods
# from .modules/readsource import *
# dir(readsource)

def main():
    print("Proberen uit te voeren")
    result = mods.readtext("Pascal")
    print(result)

if __name__ == '__main__':
    main()