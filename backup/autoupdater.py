from datetime import *
from json import JSONDecodeError
from pathlib import Path
import os
import requests
import zipfile
import io
import json
import shutil
import modules as mods
import installconfig

def main():
    
    config = mods.readConfig()
    logfilepath = config["logfilepath"]
    debug = bool(config["debug"])
    scriptfolder = config["scriptspath"]
    apiurl = config["apiurl"]
    timers = config["timerUnits"]
    servicesToInstall = config["servicesToInstall"]
    servicesToCopy = config["servicesToCopy"]
    serverApiDir = config["serverApiDir"]
    clientConfigDir = config["clientConfigDir"]

    logfile = mods.openLogFile(logfilepath,"update",debug)
    hostname = mods.getHostname(logfile)

    try:
        versionfile = scriptfolder + "version.txt"

        latestVersion,zipUrl = mods.getReleaseInfo(apiurl,debug,logfile)
            
        if os.path.exists(versionfile):
            try:
                with open(versionfile,"r") as vf:
                    installedVersion = vf.readline()
                    vf.close()
                if debug:
                    print("[DEBUG] Geïnstalleerde versie: {}".format(installedVersion))

            except Exception as error:
                logfile.write("{} Er is iets fout gegaan bij het inlezen van de versiefile: {}\n".format(datetime.today(),versionfile))
                print("Er is iets fout gegaan bij het inlezen van de versiefile {}".format(versionfile))
                installedVersion = ''
        else:
            installedVersion = ''
            logfile.write("{} Er is geen versiefile gevonden\n".format(datetime.today()))
            print("Er is geen versiefile gevonden")

        if installedVersion == '' or installedVersion != latestVersion:
            try:
                tempFolder = mods.downloadZip(zipUrl,debug,logfile)
                    
                # delete tests directory
                if os.path.exists(os.path.join(tempFolder,"backup/tests/")):
                    # shutil.rmtree(os.path.join(tempFolder,"backup/tests/"))
                    mods.deleteDirectory(os.path.join(tempFolder,"backup/tests/"),logfile)
                
                if os.path.exists(tempFolder):
                    os.system("cp -r {}/* {}".format(tempFolder,scriptfolder))
                    # remove config dir
                    # shutil.rmtree(os.path.join(scriptfolder,"config"))
                    mods.deleteDirectory(os.path.join(scriptfolder,"config"),logfile)

                    # Installing API server and client
                    mods.installApiServer(tempFolder,serverApiDir,debug,logfile)
                    mods.installWebClient()

                    logfile.write("{} De bestanden zijn gekopieerd naar directory: {}\n".format(datetime.today(),scriptfolder))
                    if debug:
                        print("[DEBUG] Bestanden zijn gekopieerd naar de scriptsfolder")
                           
                try:
                    with open(versionfile,"w") as vf:
                        vf.write(latestVersion)
                        vf.close()
                        if debug:
                            print("[DEBUG] Versiefile {} is aangemaakt".format(vf.name))

                    logfile.write("{} Latest versienummer {} schrijven naar versiefile: {}\n".format(datetime.today(),latestVersion,versionfile))
                except Exception as writeError:
                    print("Er is fout opgetreden tijdens het schrijven van de latest {} version naar de versiefile {} van de logfile".format(latestVersion,versionfile))
                    logfile.write("{} Er is een fout opgetreden bij het schrijven van {} naar de versiefile {}\nDe foutmelding is: {}\n".format(datetime.today(),latestVersion,versionfile,writeError))

                # reset execute bit op .sh files
                try:
                    logfile.write("{} Instellen van het execute bit op .sh files\n".format(datetime.today()))
                    if debug:
                        setModeFile = scriptfolder + "setmode.txt"
                        print("[DEBUG] Setting atributes van .sh files naar executable")
                        os.system("find {folder} -name \"*.sh\" -exec chmod -c +x {} \; > {modeResult}".format(folder=scriptfolder,modeResult=setModeFile))
                        with open(setModeFile,"r") as setmode:
                            print(setmode.read())
                        os.system("rm {}".format(setModeFile))

                    else:
                        os.system("find {scriptfolder} -name \"*.sh\" -exec chmod +x {} \;".format(scriptfolder=scriptfolder))

                except Exception as error:
                    logfile.write("{} Er is een fout opgetreden tijdens het instellen van het execute bit op .sh files.\n".format(datetime.today()))

                # cleanup /tmp folder
                try:
                    if os.path.exists(tempFolder):
                        os.system("rm -rf {}".format(tempFolder))
                        logfile.write("{} De tempfolder is opgeruimd\n".format(datetime.today()))
                        if debug:
                            print("[DEBUG] Tempfolder is opgeruimd")
                except Exception as error:
                    print("Er is een fout opgetreden bij het opruimen van de temp folder\nError: {}".format(error))
                    logfile.write("{} Er is een fout opgetreden tijdens het opruimen van de tempfolder. De error is: {}\n".format(datetime.today(),error))

            except Exception as error:
                logfile.write("{} Er is iets fout gegaan tijdens het downloaden van de zipfile\n".format(datetime.today()))
                logfile.write("{} De foutmelding is: {}\n".format(datetime.today(),error))
                if debug:
                    print("[DEBUG] Er is iets fout gegaan tijdens het downloaden van de zip. De error is: {}".format(error))
                exit()

            try:
                # Installeer daemons. Eerst daemons, dan timers
                # Service moet worden geïnstalleerd, maar wordt gestart door een timer
                for serviceToInstall in servicesToInstall:
                    status = mods.checkIfDaemonIsNotInstalled(serviceToInstall,logfile,debug)

                    if status:
                        installedService = mods.installDaemon(serviceToInstall,logfile,debug,scriptfolder,status)
                    else:
                        compareResult = mods.compareDaemonFiles(serviceToInstall,logfile,scriptfolder,debug) # False betekent files zijn niet gelijk, nieuwe kopieren
                        installedService = mods.installDaemon(serviceToInstall,logfile,debug,scriptfolder,compareResult)

                    if installedService == 'installed':
                        mods.enableDaemon(serviceToInstall,logfile,debug)
                    if installedService == 'updated':
                        mods.reloadDaemon(logfile,debug)
                    if installedService == 'error':
                        logfile.write("{} Er is een fout opgetreden tijden het installeren van service: {}\n".format(datetime.today(),serviceToInstall))
                        if debug:
                            print("[DEBUG] Er is een fout opgetreden bij het installeren van service: {}".format(serviceToInstall))

            except Exception as error:
                logfile.write("{} Er is iets fout gegaan tijdens het installeren van de service {}\n".format(datetime.today(),servicesToInstall))
                logfile.write("{} De foutmelding is: {}\n".format(datetime.today(),error))
                if debug:
                    print("[DEBUG] Er is iets fout gegaan tijdens het installeren van de service {}. De error is: {}".format(servicesToInstall,error))
                exit()

            try:          
                for serviceToCopy in servicesToCopy:
                    compareResult = mods.compareDaemonFiles(serviceToCopy,logfile,scriptfolder,debug) # False betekent files zijn niet gelijk, dus updaten

                    if not compareResult:
                        mods.copyDaemonFiles(serviceToCopy,scriptfolder,logfile,debug)
            except Exception as error:
                logfile.write("{} Er is iets fout gegaan tijdens het Kopieren van de service {}\n".format(datetime.today(),serviceToCopy))
                logfile.write("{} De foutmelding is: {}\n".format(datetime.today(),error))
                if debug:
                    print("[DEBUG] Er is iets fout gegaan tijdens het installeren van de service {}. De error is: {}".format(serviceToCopy,error))
                exit()

            try:
                for timer in timers:
                    status = mods.checkIfDaemonIsNotInstalled(timer,logfile,debug)
                    
                    if status:
                        installedTimer = mods.installDaemon(timer,logfile,debug,scriptfolder,status)
                    else:
                        compareResult = mods.compareDaemonFiles(timer,logfile,scriptfolder,debug)
                        installedTimer = mods.installDaemon(timer,logfile,debug,scriptfolder,compareResult)
                    
                    if installedTimer == 'installed':
                        mods.enableDaemon(timer,logfile,debug)
                        mods.startDaemon(timer,logfile,debug)
                    if installedTimer == 'updated':
                        mods.reloadDaemon(logfile,debug)
                        mods.restartDaemon(timer,logfile,debug)
                    if installedTimer == 'error':
                        logfile.write("{} Er is een fout opgetreden tijden het installeren van timer: {}\n".format(datetime.today()))
                        if debug:
                            print("[DEBUG] Er is een fout opgetreden bij het installeren van timer: {}".format(timer))

            except Exception as error:
                logfile.write("{} Er is iets fout gegaan tijdens het installeren van de timer {}\n".format(datetime.today(),timer))
                logfile.write("{} De foutmelding is: {}\n".format(datetime.today(),error))
                if debug:
                    print("[DEBUG] Er is iets fout gegaan tijdens het installeren van de timer {}. De error is: {}".format(timer,error))
                exit()

            subject = "Autoupdate op server {hostname} is succesvol uitgevoerd".format(hostname=hostname)
            message = "Autoupdate op server {hostname} is succesvol uitgevoerd\nZie de bijgevoegde logfile.\nDe geïnstalleerde versie is: {latestVersion}.".format(hostname=hostname,latestVersion=latestVersion)
            mods.closeLogFile(logfile)
            mods.sendMail(subject,message,logfile)

        else:
            if debug:
                print("[DEBUG] Laatste versie is al geïnstalleerd. Er hoeft niets te worden gedaan.")
            logfile.write("{} De laatste versie: {} is al geïnstalleerd. De updater wordt nu gesloten.\n".format(datetime.today(),installedVersion))
            mods.closeLogFile(logfile)

        
    except Exception as error:
        if debug:
            print("[DEBUG] Error bij uitvoeren van Autoupdater")
            print("[DEBUG] error is: {}".format(error))

        subject = "Autoupdate op server {hostname} is gefaald"
        message="""\
        Update downloaden op server {hostname} is gefaald\n
        {error}""".format(hostname=hostname,error=error)
        logfile.write("{} Er is een fout opgetreden bij het uitvoeren van de update\n".format(datetime.today()))
        logfile.write("{} De opgetreden error is: {}\n".format(datetime.today(),error))
        mods.sendMailFailedUpdate(hostname,message)

    mods.closeLogFile(logfile)

if __name__ == '__main__':
    main()