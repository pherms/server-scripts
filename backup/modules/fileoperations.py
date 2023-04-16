import os, sys
from pathlib import Path

def isDirectory(path):
    p = Path(path.rstrip())
    isDirectory = p.is_dir()
    print("Directory {0} is een: {1}".format(path,isDirectory))
    return isDirectory
    