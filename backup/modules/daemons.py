import os
import subprocess
from datetime import datetime

# def stopDaemon(daemon,logfile,debug):
#     try:
#         if debug:
#             print("[DEBUG] Stoppen van daemon {}".format(daemon))
#         logfile.write("{} Stoppen van daemon {}\n".format(datetime.today(),daemon))
#         os.system('systemctl stop {}'.format(daemon))

#         while True:
#             if not getDaemonStatus(daemon,logfile,debug).find('inactive') == -1:
#                 break

#         logfile.write("{} Daemon {} is gestopt\n".format(datetime.today(),daemon))

#         return True
#     except Exception as error:
#         logfile.write("{curtime} Er is iets fout gegaan tijdens het stoppen van daemon {daemon}\n{curtime} De error is: {error}".format(curtime=datetime.today(),daemon=daemon,error=error))
#         return False

def startDaemon(daemon,logfile,debug):
    try:
        if debug:
            print("[DEBUG] Starten van daemon {}".format(daemon))
        logfile.write("{} Starten van daemon {}\n".format(datetime.today(),daemon))
        os.system('systemctl start {}'.format(daemon))

        while True:
            if not getDaemonStatus(daemon,logfile,debug).find('active') == -1:
                break

        logfile.write("{} Daemon {} is gestart\n".format(datetime.today(),daemon))
        return True
    except Exception as error:
        logfile.write("{curtime} Er is iets fout gegaan tijdens het starten van daemon {daemon}\n{curtime} De error is: {error}".format(curtime=datetime.today(),daemon=daemon,error=error))
        return False

def restartDaemon(daemon,logfile,debug):
    try:
        if debug:
            print("[DEBUG] Herstarten van daemon {}".format(daemon))
        logfile.write("{} Herstarten van daemon {}\n".format(datetime.today(),daemon))
        os.system('systemctl restart {}'.format(daemon))

        while True:
            if not getDaemonStatus(daemon,logfile,debug).find('active') == -1:
                break

        logfile.write("{} Daemon {} is herstart\n".format(datetime.today(),daemon))
        return True
    except Exception as error:
        logfile.write("{curtime} Er is iets fout gegaan tijdens het herstarten van daemon {daemon}\n{curtime} De error is: {error}".format(curtime=datetime.today(),daemon=daemon,error=error))
        return False

def installDaemon(daemon,logfile,debug):
    try:
        if not os.path.exists("/etc/systemd/system/{}".format(daemon)):
            if debug:
                print("[DEBUG] De daemon is niet geinstalleerd. De bestanden worden gekopieerd")
            logfile.write("{} Daemon {} is niet geinstalleerd. De bestanden worden gekopieerd\n".format(datetime.today(),daemon))
            copyDaemonFiles(daemon,logfile)
            return "installed"
        else:
            with open("/etc/systemd/system/{}".format(daemon)) as iD:
                installedDaemon = iD.read()
                iD.close()

        with open("../systemd/{}".format(daemon)) as sD:
            scriptDaemon = sD.read()
            sD.close()

        if not installedDaemon == scriptDaemon:
            if debug:
                print("[DEBUG] De geinstalleerde daemon files wijken af. Nieuwe files kopieren")

            logfile.write("{} Daemon {} heeft updates. De nieuwe daemon wordt geinstalleerd\n".format(datetime.today(),daemon))
            copyDaemonFiles(daemon,logfile)
            return "updated"
        
    except Exception as error:
        return "error"

def copyDaemonFiles(daemon,logfile):      
    os.system("cp ../systemd/{} /etc/systemd/system/".format(daemon))

def enableDaemon(daemon,logfile,debug):
    if debug:
        print("[DEBUG] Enablen van daemon {}".format(daemon))
    logfile.write("{} Enablen van daemon {}".format(datetime.today(),daemon))
    os.system("systemctl enable {}".format(daemon))

def reloadDaemon(daemon,logfile,debug):
    if debug:
        print("[DEBUG] Herladen van daemon scripts")
    logfile.write("{} Herladen van daemon scripts\n".format(datetime.today()))
    os.system('systemctl daemon-reload')

def checkIfDaemonIsInstalled(daemon,logfile,debug):
    daemonName = getDaemonStatus(daemon,logfile,debug)
    if daemonName.find('could not be found'):
        if debug:
            print("[DEBUG] Daemon is niet geinstalleerd")
        logfile.write("{} Daemon {} is niet geinstalleerd\n".format(datetime.today(),daemon))
        return False
    else:
        if debug:
            print("[DEBUG] Daemon is geinstalleerd")
        logfile.write("{} Daemon {} is geinstalleerd\n".format(datetime.today(),daemon))
        return True

def getDaemonStatus(daemon,logifle,debug):
    daemonName = subprocess.check_output("systemctl status {}".format(daemon), shell=True).decode()
    return daemonName
