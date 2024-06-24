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
    tempFolder = ""

    logfile = mods.openLogFile(logfilepath,"update",debug)

# Downloading zip
    try:
        response = requests.get(apiurl)

        if response.status_code == 200:
            if debug:
                print("[DEBUG] API request succesvol uitgevoerd: {}".format(response.status_code))

            logfile.write("{} API request naar {} succesvol uitgevoerd. Status code: {}\n".format(datetime.today(),apiurl,response.status_code))
            responseDictionary = response.json()
            
            if debug:
                prettyJson = json.dumps(responseDictionary, indent=4)
                print(prettyJson)

            latestVersion = responseDictionary.get('tag_name')
            zipUrl = responseDictionary.get('zipball_url')
            if debug:
                print("[DEBUG] latest version: {}\n[DEBUG] zipUrl: {}".format(latestVersion,zipUrl))
        else:
            print("Er is iets fout gegaan bij het uitvoeren van de API request naar Github. Het script wordt afgebroken")
            logfile.write("{} Er is iets fout gegaan bij het uitvoeren van de API request naar Github. Het proces wordt gestopt\n".format(datetime.today()))
            exit()

    except JSONDecodeError as jsonerror:
        if debug:
            print("[DEBUG] Er is iets fout gegaan tijdens het decoden van de JSON.\n[DEBUG] De error is: {}".format(jsonerror))

        logfile.write("{} Er is iets fout gegaan tijdens het decoden van de JSON. De error is: {}\n".format(datetime.today(),jsonerror))
        exit()

    except Exception as error:
        logfile.write("{} Er is iets fout gegaan tijdens het uitvoeren van de API request. Status code: {}\n".format(datetime.today(),response.status_code))
        logfile.write("{} De error is: {}\n".format(datetime.today(),error))
        if debug:
            print("[DEBUG] fout bij uitvoeren API request: {}. Zie logfile".format(response.status_code))
        exit()

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

# Downloaden zip file
    try:
        requestZip = requests.get(zipUrl)
        print(requestZip)
        if debug:
            print("[DEBUG] zipfile is gedownload. statuscode: {}".format(requestZip.status_code))
            
        if requestZip.ok:
            logfile.write("{} De zipfile {} is succesvol gedownload\n".format(datetime.today(),zipUrl))
            zipFile = zipfile.ZipFile(io.BytesIO(requestZip.content))
            folderInZip = zipFile.namelist()[0]
            tempFolder = "/tmp/" + folderInZip[:-1]

            os.chdir('/tmp')
            zipFile.extractall()
            logfile.write("{} De zipfile is uitgepakt naar directory {}\n".format(datetime.today(),tempFolder))
            
    except Exception as error:
        logfile.write("{} Er is iets fout gegaan tijdens het downloaden van de zipfile\n".format(datetime.today()))
        logfile.write("{} De foutmelding is (line 108): {}\n".format(datetime.today(),error))
        if debug:
            print("[DEBUG] Er is iets fout gegaan tijdens het downloaden van de zip. De error is: {}".format(error))
        exit()

# Installing script files
    try:
        # delete tests directory
        logfile.write("{} Installeren van de server-scripts:\n".format(datetime.today()))
        if os.path.exists(os.path.join(tempFolder,"backup/tests/")):
            logfile.write("{} Verwijderen van de unit-tests directories\n".format(datetime.today()))
            mods.deleteDirectory(os.path.join(tempFolder,"backup/tests/"),logfile)
        
        if os.path.exists(tempFolder):
            logfile.write("{} Kopieren van de scripts naar de scriptfolder: {}\n".format(datetime.today(),scriptfolder))
            os.system("cp -r {}/* {}".format(tempFolder,scriptfolder))
            # remove config dir
            logfile.write("{} Verwijderen van de config dir uit de folder: {}\n".format(datetime.today(),os.path.join(scriptfolder,"config")))
            mods.deleteDirectory(os.path.join(scriptfolder,"config"),logfile)

        logfile.write("{} De server scripts zijn geinstalleerd\n".format(datetime.today()))
    except Exception as error:
        logfile.write("{} Er is iets fout gegaan tijdens het installeren van de scriptfiles\n".format(datetime.today()))
        logfile.write("{} De foutmelding is: {}\n".format(datetime.today(),error))
        if debug:
            print("[DEBUG] Er is iets fout gegaan tijdens het installeren van de scriptfiles. De error is: {}".format(error))
        exit()

# Installeren API server
    try:
        # api server
        logfile.write("{} Installeren van de API server\n".format(datetime.today()))
        serverDir = Path(os.path.join(tempFolder,"config/server/"))
        # index = serverDir.parts.index('src')
        # workingDir = os.path.join(serverDir,"src")

        os.chdir(serverDir)
        # shutil.rmtree("dist")
        mods.deleteDirectory(os.path.join(serverDir,"dist"),logfile)

        # recreate build folder en build app
        os.mkdir("dist")
        # os.system("npm run build")
        mods.compileSource("server",logfile)

        mods.installFiles("server",tempFolder,logfile)
        mods.databaseSetup(logfile)
        mods.restartDaemon("config-server-api",logfile,debug)
    except Exception as error:
        logfile.write("{} Er is iets fout gegaan bij het installeren van de API server.\nDe error is: {}\n".format(datetime.today(),error))
        exit()

# Installeren web client
    try:
        # config client
        logfile.write("{} Installeren van de web client\n".format(datetime.today()))
        clientDir = Path(os.path.join(tempFolder,"config/client/"))
        os.chdir(clientDir)
        
        mods.deleteDirectory(os.path.join(clientDir,"dist"),logfile)

        # recreate build folder en build app
        os.mkdir("dist")
        
        mods.compileSource("client",logfile)
        mods.installFiles("client",tempFolder,logfile)
        mods.restartDaemon("apache2",logfile,debug)
        # end config client

        logfile.write("{} De bestanden zijn gekopieerd naar directory: {}\n".format(datetime.today(),scriptfolder))
        if debug:
            print("[DEBUG] Bestanden zijn gekopieerd naar de scriptsfolder")
        logfile.write("{} De webclient is geinstallleerd\n".format(datetime.today()))
    except Exception as error:
        logfile.write("{} Er is iets fout gegaan bij het installeren van de web client. De error is: {}\n".format(datetime.today(),error))
        exit()

if __name__ == '__main__':
    main()
