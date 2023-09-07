import os
import subprocess
from datetime import datetime

def stopDaemon(daemon,logfile,debug):
    isRunning = checkIfDaemonIsRunnning(daemon,logfile,debug)
    if isRunning:
        if debug:
            print("Stoppen van daemon {}".format(daemon))
        logfile.write("{} Stoppen van daemon {}\n".format(datetime.today(),daemon))
        os.system('systemctl stop {}'.format(daemon))

def startDaemon(daemon,logfile,debug):
    isRunning = checkIfDaemonIsRunnning(daemon,logfile,debug)
    if not isRunning:
        if debug:
            print("Starten van daemon {}".format(daemon))
        logfile.write("{} Starten van daemon {}\n".format(datetime.today(),daemon))
        os.system('systemctl start {}'.format(daemon))

def restartDaemon(daemon,logfile,debug):
    isRunning = checkIfDaemonIsRunnning(daemon,logfile,debug)
    if isRunning:
        if debug:
            print("Herstarten van daemon {}".format(daemon))
        logfile.write("{} Herstarten van daemon {}\n".format(datetime.today(),daemon))
        os.system('systemctl restart {}'.format(daemon))

def installDaemon(daemon,logfile,debug):
    pass

def reloadDaemon(daemon,logfile,debug):
    isRunning = checkIfDaemonIsRunnning(daemon,logfile,debug)
    if isRunning:
        if debug:
            print("Herladen van daemon scripts")
        logfile.write("{} Herladen van daemon scripts\n".format(datetime.today()))
        os.system('systemctl daemon-reload')

def checkIfDaemonIsRunnning(daemon,logfile,debug):
    ps = subprocess.Popen(('ps', '-ef'), stdout=subprocess.PIPE)
    grep = subprocess.Popen(('grep', '-v', 'grep'), stdin=ps.stdout, stdout=subprocess.PIPE)

    ps.stdout.close()  # Allow ps to receive a SIGPIPE if grep exits.

    grep_daemon = subprocess.Popen(('grep', 'sshd'), stdin=grep.stdout)

    grep.stdout.close() # Allow grep to receive a SIGPIPE if grep_daemon exits

    output = grep_daemon.communicate()[0]
    if output.lower() == "none":
        if debug:
            print("[DEBUG] Daemon {} is niet actief".format(daemon))
        logfile.write("{} Daemon {} is niet actief\n".format(datetime.today(),daemon))
        return False
    else:
        if debug:
            print("[DEBUG] daemon {} is actief. Return True".format(daemon))
        logfile.write("{} Daemon {} is actief\n".format(datetime.today(),daemon))
        return True
