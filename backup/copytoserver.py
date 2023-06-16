from datetime import datetime
import modules as mods
import os
# from datetime import datetime

def main():
    config = mods.readConfig()
    backupdir = config['backuppath']
    logfiledir = config['logfilepath']
    backupserver = config['backupserver']
    copycommand = config['copycommand']
    remotefilepath = config['remotefilepath']
    hostType = config['hostType']

    if hostType == 'vm':
        logfile = mods.openLogFile(logfiledir,"copy")
        hostname = mods.getHostname(logfile)

        logfile.write("{} Beginnen met kopieren van backupfiles naar server {}\n".format(datetime.today(),backupserver))
        filesCopied = []

        for file in os.listdir(backupdir):
            backupFullFile = backupdir + file
            mods.copyFileToServer(backupFullFile,backupserver,copycommand,remotefilepath,logfile,hostname)
            filesCopied.append(file)

        logfile.write("{} Kopieren van files naar server {} is voltooid\n".format(datetime.today(),backupserver))
        logfile.write("{} Totaal aantal files gekopieerd: {}\n".format(datetime.today(),len(filesCopied)))

        message_text = """\
        De backup files van {hostname} zijn succesvol naar de server gekopieerd.\n
        Het totaal aantal gekopieerde bestanden is: {totalFilesCopied}\n
        Zie ook bijgande logfile\n""".format(hostname=hostname,totalFilesCopied=len(filesCopied))
        subject = "Kopieren van files naar van server {} succesvol".format(hostname)

    mods.sendMail(subject,message_text,logfile)

if __name__ == '__main__':
    main()