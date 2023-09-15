import os
import subprocess
from datetime import datetime

def startDaemon(daemon,logfile,debug):
    """
    Start een daemon. Geeft de waarde terug.

    :param str daemon: de daemon die moet worden gestart
    :param bool debug: enable debug logging
    :param obj logfile: de logfile waar naartoe moet worden gelogd
    :return: boolean wanneer de service is gestart
    :rtype: bool
    """
    try:
        if debug:
            print("[DEBUG] Starten van daemon {}".format(daemon))
        logfile.write("{} Starten van daemon {}\n".format(datetime.today(),daemon))
        os.system('systemctl start {}'.format(daemon))

        while True:
            statusDaemonActive = isDaemonActive(daemon)
            print(statusDaemonActive)
            if statusDaemonActive.find('active') >= 0:
                break

        logfile.write("{} Daemon {} is gestart\n".format(datetime.today(),daemon))
        return True
    except Exception as error:
        logfile.write("{curtime} Er is iets fout gegaan tijdens het starten van daemon {daemon}\n{curtime} De error is: {error}".format(curtime=datetime.today(),daemon=daemon,error=error))
        return False

def restartDaemon(daemon,logfile,debug):
    """
    Herstart een daemon. Geeft de waarde terug.

    :param str daemon: de daemon die moet worden gestart
    :param bool debug: enable debug logging
    :param obj logfile: de logfile waar naartoe moet worden gelogd
    :return: boolean wanneer de service is gestart
    :rtype: bool
    """
    try:
        if debug:
            print("[DEBUG] Herstarten van daemon {}".format(daemon))
        logfile.write("{} Herstarten van daemon {}\n".format(datetime.today(),daemon))
        os.system('systemctl restart {}'.format(daemon))

        while True:
            statusDaemonActive = isDaemonActive(daemon)
            if not statusDaemonActive.find('active') == -1 or statusDaemonActive == 3:
                break

        logfile.write("{} Daemon {} is herstart\n".format(datetime.today(),daemon))
        return True
    except Exception as error:
        logfile.write("{curtime} Er is iets fout gegaan tijdens het herstarten van daemon {daemon}\n{curtime} De error is: {error}".format(curtime=datetime.today(),daemon=daemon,error=error))
        return False

def installDaemon(daemon,logfile,debug,scriptfolder,status):
    """
    Installeer een daemon. Geeft een waarde terug.

    :param str daemon: de daemon die moet worden gestart
    :param str scriptfolder: de daemon die moet worden gestart
    :param str status: True wanneer de bestaande daemon config file afwijkt van de nieuwe. False wanneer dit niet het geval is (zie compareDaemonFiles)
    :param bool debug: enable debug logging
    :param bool compared: de compare functie heeft verschillen gevonden, dus bijwerken.
    :param obj logfile: de logfile waar naartoe moet worden gelogd
    :return: Installed status. Geldige waarden zijn: "installed", "updated", "error"
    :rtype: str
    """
    try:
        if not status:
            if not os.path.exists("/etc/systemd/system/{}".format(daemon)):
                if debug:
                    print("[DEBUG] De daemon is niet geinstalleerd. De bestanden worden gekopieerd")
                logfile.write("{} Daemon {} is niet geinstalleerd. De bestanden worden gekopieerd\n".format(datetime.today(),daemon))
                copyDaemonFiles(daemon,scriptfolder,logfile,debug)
                return 'installed'
            else:
                if debug:
                    print("[DEBUG] De daemon is al geinstalleerd, maar er zijn wijzigingen.")
                logfile.write("{} Daemon {} is al geinstalleerd, maar er zijn wijzigingen. De bestanden worden gekopieerd\n".format(datetime.today(),daemon))
                copyDaemonFiles(daemon,scriptfolder,logfile,debug)
                return 'updated'
        else:
            if debug:
                print("[DEBUG] De daemon is al geinstalleerd of er zijn geen wijzigingen.")
            logfile.write("{} Daemon {} is al geinstalleerd of er zijn geen wijzigingen\n".format(datetime.today(),daemon))
            return 'done'
          
    except Exception as error:
        return "error"

def compareDaemonFiles(daemon,logfile,scriptfolder,debug):
    """
    Vergelijk de bestaande daemon met de nieuwe. Geeft de waarde terug.

    :param str daemon: de daemon die moet worden gestart
    :param str scriptfolder: de daemon die moet worden gestart
    :param bool debug: enable debug logging
    :param obj logfile: de logfile waar naartoe moet worden gelogd
    :return: False wanneer files ongelijk zijn, wat betekent dat de nieuwe moet worden geïnstalleerd. True er hoeft niets te worden gedaan
    :rtype: bool
    """
    if not os.path.exists("/etc/systemd/system/{}".format(daemon)):
        return False
    else:
        with open("/etc/systemd/system/{}".format(daemon)) as iD:
            contentInstalledDaemon = iD.read()
            iD.close()

        with open("{}backup/systemd/{}".format(scriptfolder,daemon)) as sD:
            contentScriptDaemon = sD.read()
            sD.close()

    if not contentInstalledDaemon == contentScriptDaemon:
        if debug:
            print("[DEBUG] De geinstalleerde daemon files wijken af. Nieuwe files kopieren")

        logfile.write("{} Daemon {} heeft updates. De nieuwe daemon wordt geinstalleerd\n".format(datetime.today(),daemon))
        return False
    else:
        return True

def copyDaemonFiles(daemon,scriptfolder,logfile,debug):
    """
    Kopieert de daemon files uit de script folder naar de system folder.

    :param str daemon: de daemon die moet worden gestart
    :param str scriptfolder: de daemon die moet worden gestart
    """
    # change source folder before commit to scriptfolder
    try:
        os.system("cp {}backup/systemd/{} /etc/systemd/system/".format(scriptfolder,daemon))
    except Exception as error:
        if debug:
            print("[DEBUG] Error tijdens kopieren van unit file: {}. De error is: {}".format(daemon,error))
        print("Error tijdens kopieren van de unit file {}".format(daemon))
        print("De error is: {}".format(error))
        logfile.write("{} Fout bij kopieren unit file {}. De error is: {}\n".format(datetime.today(),daemon,error))


def enableDaemon(daemon,logfile,debug):
    """
    Enabled de daemon file wanneer deze in de systemfolder is gekopieerd.

    :param str daemon: de daemon die moet worden gestart
    :param bool debug: enable debug logging
    :param obj logfile: de logfile waar naartoe moet worden gelogd
    """
    if os.path.exists("/etc/systemd/system/{}".format(daemon)):
        if debug:
            print("[DEBUG] Enablen van daemon {}".format(daemon))
        logfile.write("{} Enablen van daemon {}\n".format(datetime.today(),daemon))
        os.system("systemctl enable {}".format(daemon))
    else:
        logfile.write("{} Daemon file {} bestaat niet\n".format(datetime.today(),daemon))
        exit()

def reloadDaemon(logfile,debug):
    """
    Herlaad de daemon config files van de disk

    :param bool debug: enable debug logging
    :param obj logfile: de logfile waar naartoe moet worden gelogd
    """
    if debug:
        print("[DEBUG] Herladen van daemon scripts")
    logfile.write("{} Herladen van daemon scripts\n".format(datetime.today()))
    
    os.system('systemctl daemon-reload')

def checkIfDaemonIsNotInstalled(daemon,logfile,debug):
    """
    Raadpleegt via systemctl is-enabled of een daemon is geïnstalleerd.

    :param str daemon: de daemon die moet worden gestart
    :param bool debug: enable debug logging
    :param obj logfile: de logfile waar naartoe moet worden gelogd
    :return: True wanneer daemon niet is geinstalleerd, False wanneer deze is geinstalleerd
    :rtype: bool
    """
    statusDaemonEnabled = isDaemonEnabled(daemon)
    print("[DEBUG] Waarde statusDaemonEnabled: {}".format(statusDaemonEnabled))

    if statusDaemonEnabled == 'disabled' or statusDaemonEnabled == 'error' or statusDaemonEnabled == 'not-found':
        if debug:
            print("[DEBUG] Daemon {} is niet geinstalleerd".format(daemon))
        logfile.write("{} Daemon {} is niet geinstalleerd\n".format(datetime.today(),daemon))
        return True
    elif statusDaemonEnabled == 'enabled':
        if debug:
            print("[DEBUG] Daemon {} is geinstalleerd".format(daemon))
        logfile.write("{} Daemon {} is geinstalleerd\n".format(datetime.today(),daemon))
        return False
    else:
        print("[DEBUG] Er is een andere status. {}".format(statusDaemonEnabled))

def isDaemonActive(daemon):
    """
    Raadpleegt via systemctl is-active of de daemon gestart is. Geeft str of int terug

    :param str daemon: de daemon die moet worden geraadpleegd
    :return: String wanneer service gevonden is, active wanneer deze is gestart, inactive wanneer deze is gestopt. Int wanneer de service niet is gevonden (code 3)
    :rtype: Str or Int
    """
    print("[DEBUG] in funtie isDaemonActive")

    try:
        # isActive = subprocess.check_output(["systemctl", "is-active", "{}".format(daemon)]).decode("utf-8")
        isActive = subprocess.run(["systemctl", "is-active", "{}".format(daemon)],capture_output=True).stdout.decode("utf-8").strip()
        return isActive
    except subprocess.CalledProcessError as e:
        # De service kan niet worden gevonden en systemctl returned code 3
        if e.returncode == 3:
            isActive = 'notactive'
        else:
            isActive = 'error'
        return isActive

def isDaemonEnabled(daemon):
    """
    Raadpleegt via systemctl is-enabled of de daemon geinstalleerd is. Geeft str of int terug

    :param str daemon: de daemon die moet worden geraadpleegd
    :return: String wanneer service gevonden is, enabled wanneer deze is geinstalleerd. disabled wanneer deze servicefile aanwezig is, maar nog niet is ge-enabled,not-found wanneer deze niet is geinstalleerd en error wanneer er een andere status is.
    :rtype: Str
    """
    print("[DEBUG] in funtie isDaemonEnabled")
    try:
        # isEnabled = subprocess.check_output(["systemctl", "is-enabled", "{}".format(daemon)]).decode("utf-8")
        isEnabled = subprocess.run(["systemctl", "is-enabled", "{}".format(daemon)],capture_output=True).stdout.decode("utf-8").strip()
        return isEnabled
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        # De service kan niet worden gevonden en systemctl returned code 3
        if e.returncode == 3:
            isEnabled = 'not-found'
        else:
            print("Returncode is not 3. Value: {}".format(e.returncode))
            isEnabled = 'error'
        return isEnabled
