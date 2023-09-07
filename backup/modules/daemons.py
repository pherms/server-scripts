import os
import subprocess
from datetime import datetime

def stopDaemon(daemon,logfile):
    pass

def startDaemon(daemon,logfile):
    pass

def restartDaemon(daemon,logfile):
    pass

def installDaemon(daemon,logfile):
    pass

def reloadDaemon(daemon,logfile):
    pass

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
