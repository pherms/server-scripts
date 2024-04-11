import os
import glob
import unittest
import shutil
import modules as mods
from pathlib import Path
from datetime import datetime, timedelta

# Global variables
backuppath = "/home/pascal/backup/unittest/"
class Testing(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        if not os.path.exists(backuppath):
            mods.createFolder(backuppath)
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(backuppath)

    def test_isDirectory(self):
        isDirectory = mods.isDirectory(backuppath)
        self.assertTrue(isDirectory)

    def test_createfilename_tar_bz2(self):
        logfile = mods.openLogFile(backuppath,'backup',False)
        date = datetime.today().strftime('%Y%m%d')
        fileName = mods.generateFileName("pc10702","tar","bz2",logfile,False)
        logfile.close()
        self.assertEqual("pc10702-{}.tar.bz2".format(date),fileName)

    def test_createfilename_zip(self):
        logfile = mods.openLogFile(backuppath,'backup',False)
        date = datetime.today().strftime('%Y%m%d')
        fileName = mods.generateFileName("pc10702","zip","",logfile,False)
        logfile.close()
        self.assertEqual("pc10702-{}.zip".format(date),fileName)
    
    def test_createfolder(self):
        folder = os.path.join(backuppath,"test-folder")
        mods.createFolder(folder)
        isDirectory = mods.isDirectory(folder)
        self.assertTrue(isDirectory)
        Path.rmdir(folder)
    
    def test_creationTime(self):
        folder = "/home/pascal/.config"
        result = mods.getCreationTime(folder,False)
        self.assertTrue(isinstance(result,dict))

    def test_renameBackupFile_to_week(self):
        logfile = mods.openLogFile(backuppath,'backup',False)
        fileName = mods.generateFileName("pc10702","tar","bz2",logfile,False)
        with open(os.path.join(backuppath, fileName), 'w') as fp:
            pass
        mods.renameBackupFile(backuppath,fileName,logfile,'week',False)
        result = glob.glob("{}/*week*".format(backuppath))
        logfile.close()
        self.assertTrue("week" in result[0])

    def test_renameBackupFile_to_month(self):
        logfile = mods.openLogFile(backuppath,'backup',False)
        fileName = mods.generateFileName("pc10702","tar","bz2",logfile,False)
        with open(os.path.join(backuppath, fileName), 'w') as fp:
            pass
        mods.renameBackupFile(backuppath,fileName,logfile,'month',False)
        result = glob.glob("{}/*month*".format(backuppath))
        logfile.close()
        self.assertTrue('month' in result[0])

    def test_determineRemoveOrBackup_day(self):
        for num in range(0,85):
            date = (datetime.today() - timedelta(days=num)).strftime('%Y%m%d')
            fileName = "pc10702-{}.tar.bz2".format(date)
            with open(os.path.join(backuppath, fileName), 'w') as fp:
                fp.write("Dit is een test")
                fp.close()

        files = mods.getCreationTime(backuppath,False)
        logfile = mods.openLogFile(backuppath,'backup',False)
        files_cleaned, files_renamed = mods.determineRemoveOrBackup(files,"",logfile,backuppath,False)
        logfile.close()

        self.assertGreaterEqual(len(files_cleaned),1)
        self.assertGreaterEqual(len(files_renamed),1)

    def test_creationDate(self):
        date = datetime.today().strftime('%Y%m%d')
        fileName = "pc10702-{}.tar.bz2".format(date)
        creationDate = mods.determineCreationDateFromFileName(fileName,False)
        self.assertRegex(creationDate,"(\d{4})-(\d{2})-(\d{2})")

if __name__ == '__main__':
    unittest.main()
