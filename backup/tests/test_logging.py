import os
import glob
import unittest
import shutil
import modules as mods
from pathlib import Path
from datetime import datetime, timedelta

# Global vars
backuppath = "/home/pascal/backup/unittest/"

class Testing(unittest.TestCase):
    @classmethod
    def setupClass(cls):        
        if not os.path.exists(backuppath):
            mods.createFolder(os.path.join(backuppath,"logging/"))
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(backuppath)

    def test_openLogFile_backup(self):
        logfile = mods.openLogFile(os.path.join(backuppath,"logging/"),'backup',False)
        result = glob.glob("{}/*backup*".format(os.path.join(backuppath,"logging/")))
        self.assertTrue("backup" in result[0])
        logfile.close()

    def test_openLogFile_cleanup(self):
        logfile = mods.openLogFile(os.path.join(backuppath,"logging/"),'cleanup',False)
        result = glob.glob("{}/*cleanup*".format(os.path.join(backuppath,"logging/")))
        self.assertTrue("cleanup" in result[0])
        logfile.close()
    
    def test_openLogFile_copy(self):
        logfile = mods.openLogFile(os.path.join(backuppath,"logging/"),'copy',False)
        result = glob.glob("{}/*copy*".format(os.path.join(backuppath,"logging/")))
        self.assertTrue("copy" in result[0])
        logfile.close()

    def test_openLogFile_update(self):
        logfile = mods.openLogFile(os.path.join(backuppath,"logging/"),'update',False)
        result = glob.glob("{}/*update*".format(os.path.join(backuppath,"logging/")))
        self.assertTrue("update" in result[0])
        logfile.close()
    # cleanup, copy, update

if __name__ == '__main__':
    unittest.main()
