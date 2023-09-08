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
            statusDaemonActive = isDaemonActive(daemon)
            print(type(statusDaemonActive))
            if statusDaemonActive == 'active':
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
            statusDaemonActive = isDaemonActive(daemon)
            if statusDaemonActive == 'active':
                break

        logfile.write("{} Daemon {} is herstart\n".format(datetime.today(),daemon))
        return True
    except Exception as error:
        logfile.write("{curtime} Er is iets fout gegaan tijdens het herstarten van daemon {daemon}\n{curtime} De error is: {error}".format(curtime=datetime.today(),daemon=daemon,error=error))
        return False

def installDaemon(daemon,logfile,debug,scriptfolder):
    try:
        if not os.path.exists("/etc/systemd/system/{}".format(daemon)):
            if debug:
                print("[DEBUG] De daemon is niet geinstalleerd. De bestanden worden gekopieerd")
            logfile.write("{} Daemon {} is niet geinstalleerd. De bestanden worden gekopieerd\n".format(datetime.today(),daemon))
            copyDaemonFiles(daemon,scriptfolder)
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
            copyDaemonFiles(daemon,scriptfolder)
            return "updated"
        
    except Exception as error:
        return "error"

def copyDaemonFiles(daemon,scriptfolder):
    # change source folder before commit to scriptfolder
    os.system("cp /server-scripts/backup/systemd/{} /etc/systemd/system/".format(daemon))

def enableDaemon(daemon,logfile,debug):
    if os.path.exists("/etc/systemd/system/{}".format(daemon)):
        if debug:
            print("[DEBUG] Enablen van daemon {}".format(daemon))
        logfile.write("{} Enablen van daemon {}\n".format(datetime.today(),daemon))
        os.system("systemctl enable {}".format(daemon))
    else:
        logfile.write("{} Daemon file {} bestaat niet\n".format(datetime.today(),daemon))
        exit()

def reloadDaemon(daemon,logfile,debug):
    if debug:
        print("[DEBUG] Herladen van daemon scripts")
    logfile.write("{} Herladen van daemon scripts\n".format(datetime.today()))
    os.system('systemctl daemon-reload')

def checkIfDaemonIsInstalled(daemon,logfile,debug):
    # daemonName = getDaemonStatus(daemon)
    # statusDaemonActive = isDaemonActive(daemon)
    statusDaemonEnabled = isDaemonEnabled(daemon)
    print("[DEBUG] statusDaemonInstalled: {}".format(statusDaemonEnabled))

    if not statusDaemonEnabled == 'enabled':
    # if daemonName.find('could not be found'):
        if debug:
            print("[DEBUG] Daemon {} is niet geinstalleerd".format(daemon))
        logfile.write("{} Daemon {} is niet geinstalleerd\n".format(datetime.today(),daemon))
        return False
    else:
        if debug:
            print("[DEBUG] Daemon {} is geinstalleerd".format(daemon))
        logfile.write("{} Daemon {} is geinstalleerd\n".format(datetime.today(),daemon))
        return True

# def getDaemonStatus(daemon):
#     try:
#         daemonName = subprocess.check_output("systemctl status {}".format(daemon), shell=True).decode("utf-8",errors="ignore")
#         return daemonName
#     except subprocess.CalledProcessError as e:
#         raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd,e.returncode,e.output))

def isDaemonActive(daemon):
    try:
        status = subprocess.check_output(["systemctl", "is-active", "{}".format(daemon)])
        status = status.decode("utf-8")
        print(status)
        return status
    except subprocess.CalledProcessError as e:
        # raise RuntimeError("command '{}'\n[DEBUG] return with error (code {})\n[DEBUG] returned output: {}".format(e.cmd,e.returncode,e.output))
        status = e.returncode
        return status

def isDaemonEnabled(daemon):
    try:
        status = subprocess.check_output(["systemctl", "is-enabled", "{}".format(daemon)])
        status = status.decode("utf-8")
        print(status)
        return status
    except subprocess.CalledProcessError as e:
        # raise RuntimeError("command '{}'\n[DEBUG] return with error (code {})\n[DEBUG] returned output: {}".format(e.cmd,e.returncode,e.output))
        status = e.returncode
        return status