import os
import io
import json
import requests
import zipfile
from json import JSONDecodeError
import modules as mods
from datetime import datetime
from pathlib import Path

def main():
    config = mods.readConfig()
    logfilepath = config["logfilepath"]
    debug = bool(config["debug"])
    scriptfolder = config["scriptspath"]
    apiurl = config["apiurl"]
    serverApiDir = config["serverApiDir"]
    tempFolder = ""

    logfile = mods.openLogFile(logfilepath,"update",debug)

# Get latestVersion en zipUrl from repository
    latestVersion,zipUrl = mods.getReleaseInfo(apiurl,debug,logfile)

# Downloaden zip file
    tempFolder = mods.downloadZip(zipUrl,debug,logfile)

# Installeer daemons
    try:
        # Installeer daemons. Eerst daemons, dan timers
        # Service moet worden geïnstalleerd, maar wordt gestart door een timer
        
        serviceToInstall = "config-server-api.service"
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
        logfile.write("{} Er is iets fout gegaan tijdens het installeren van de service {}\n".format(datetime.today(),serviceToInstall))
        logfile.write("{} De foutmelding is: {}\n".format(datetime.today(),error))
        if debug:
            print("[DEBUG] Er is iets fout gegaan tijdens het installeren van de service {}. De error is: {}".format(serviceToInstall,error))
        exit()

# Installeren API server
    mods.installApiServer(tempFolder,serverApiDir,debug,logfile)

# Installeren web client
    mods.installWebClient(tempFolder,debug,logfile)

if __name__ == '__main__':
    main()
