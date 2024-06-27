import modules as mods
import io
import os
import json
import requests
import zipfile
from json import JSONDecodeError
from pathlib import Path
from datetime import datetime

def determineConfigFolder(type,tempFolder):
    """
    Het type config bepalen. De return waarde is een folder

    :param str type: Het type wat moet worden behandeld. Mogelijke waarden zijn: client en server
    :param str tempFolder: de tempFolder waar de bestanden naar zijn uitgepakt
    :return: sourceDir,destinationDir, De sourceDir en destinationDir path objecten
    :rtype: tuple
    """
    config = mods.readConfig()

    match type:
        case "client":
            sourceDir = os.path.join(tempFolder,"config/client/")
            destinationDir = config["clientConfigDir"]
        case "server":
            sourceDir = os.path.join(tempFolder,"config/server/")
            destinationDir = config["serverApiDir"]
            print("sourceDir in determineConfigFolder functie voor type {}: {}".format(sourceDir,type))
            print("destinationDir in determineConfigFolder functie voor type {}: {}".format(destinationDir,type))
    
    return (sourceDir,destinationDir)

def installFiles(type,tempFolder,logfile):
    """
    Het kopieren van de nieuwe bestanden

    :param str type: Het type wat moet worden behandeld. Mogelijke waarden zijn: client en server
    :param str tempFolder: de tempFolder waar de bestanden naar zijn uitgepakt
    :return: sourceDir,destinationDir, De sourceDir en destinationDir path objecten
    :rtype: tuple
    """
    logfile.write("{} Gevonden type installatie: {}\n".format(datetime.today(),type))
    logfile.write("{} Bepalen van de bron en doel directories\n".format(datetime.today()))

    try:
        (sourceDir,destinationDir) = mods.determineConfigFolder(type,tempFolder)
        workingDir = Path(os.path.join(sourceDir,"src"))
        print("Sourcedir in InstallFiles functie: {}".format(sourceDir))
        print("Destination in InstallFiles functie: {}".format(destinationDir))
        index = int(Path(workingDir).parts.index('src'))
        # print(Path(sourceDir).parts.index('src'))
        print("Index: {}".format(index))
        
    except Exception as error:
        print("Er is een fout opgetreden in eerste deel van installFiles functie: {}".format(error))
        exit()

    try:
        logfile.write("{} Kopieren van de gecompilede sources\n".format(datetime.today()))
        print("Kopieren van additionele files. functie: installFiles (2e deel)")
        os.system("cp -a {}/. {}".format(os.path.join(sourceDir,"dist"),Path(destinationDir)))

        if type == "server":
            logfile.write("{} Kopieren van additionele javascript files tbv server\n".format(datetime.today()))
            for file in workingDir.glob("**/*.js"):
                source = file.absolute()
                destination = Path(destinationDir).joinpath(*source.parts[index+1:])

                os.system("cp {} {}".format(source,destination))
            
            # yes | cp -a /scripts/server-scripts/config/server/dist/. $serverapidir
            # yes | cp /scripts/server-scripts/config/server/package.json $serverapidir
            # yes | cp -a /scripts/server-scripts/config/server/prisma/ $serverapidir
            logfile.write("{} Kopieren van package.json\n".format(datetime.today()))
            os.system("cp {} {}".format(os.path.join(sourceDir,"package.json"),Path(destinationDir)))

            logfile.write("{} Kopieren van prisma directory\n".format(datetime.today()))
            os.system("cp -r {} {}".format(os.path.join(sourceDir,"prisma"),Path(destinationDir)))

    except Exception as error:
        print("Er is een fout opgetreden. {}".format(error))
        logfile.write("{} Er is een fout opgetreden. De error is:\n{}".format(datetime.today(),error))
        exit()

def compileSource(type,logfile):
    logfile.write("{} Installeren van packages voor {} source\n".format(datetime.today(),type))
    os.system("npm install")
    logfile.write("{} Compileren van {} source\n".format(datetime.today(),type))
    os.system("npm run build")

def databaseSetup(logfile):
    logfile.write("{} Genereren database files\n".format(datetime.today()))
    os.system("npm run generate")

    logfile.write("{} Deployen van database wijzigingen\n".format(datetime.today()))
    os.system("npm run migrate")

def installDependencies(logfile):
    logfile.write("{} Installeren van dependencies\n".format(datetime.today()))
    os.system("npm install")

def getReleaseInfo(apiurl,debug,logfile):
    """
    Opvragen van laatste release informatie van Github

    :param str apiurl: De url waar de query naar gemaakt moet worden
    :param str logfile: Het logfile object
    :param bool debug: aanzetten debug logging
    :return: latestVersion: Het laatste versie nummer
    :return: zipUrl: de url om de zipfile te downloaden
    :rtype: tuple
    """
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
            
            return (latestVersion,zipUrl)

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

def downloadZip(zipUrl,debug,logfile):
    """
    Downloaden van zipfile. Return data is tempFolder

    :param str zipUrl: De url waar de zipfile kan worden gedownload
    :param str logfile: Het logfile object
    :param bool debug: aanzetten debug logging
    :return: tempFolder: de folder op het OS waar de bestanden in worden uitgepakt
    :rtype: tuple
    """
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
        
        return tempFolder
            
    except Exception as error:
        logfile.write("{} Er is iets fout gegaan tijdens het downloaden van de zipfile\n".format(datetime.today()))
        logfile.write("{} De foutmelding is (line 108): {}\n".format(datetime.today(),error))
        if debug:
            print("[DEBUG] Er is iets fout gegaan tijdens het downloaden van de zip. De error is: {}".format(error))
        exit()

def installApiServer(tempFolder,serverApiDir,debug,logfile):
    """
    Installeert de Node.js API server

    :param str tempFolder: De folder waar de zipfile naartoe is uitgepakt
    :param str serverApiDir: De directory waar de server API uit draait
    :param bool debug: aanzetten debug logging
    :param str logfile: het logfile object
    """
    logfile.write("{} Installeren van de API server\n".format(datetime.today()))
    serverDir = Path(os.path.join(tempFolder,"config/server/"))
    # index = serverDir.parts.index('src')
    # workingDir = os.path.join(serverDir,"src")

    os.chdir(serverDir)
    # shutil.rmtree("dist")
    mods.deleteDirectory(os.path.join(serverDir,"dist"),logfile)

    # recreate build folder en build app
    dirsToCreate = ["middlewares/authorization","config"]
    for directoryToCreate in dirsToCreate:
        path = Path(os.path.join(serverApiDir,directoryToCreate))
        print(path)
        path.mkdir(parents=True, exist_ok=True)
    # os.system("npm run build")
    try:
        compileSource("server",logfile)
    except Exception as error:
        print("Er is een error in compileSource: {}".format(error))
        exit()

    try:
        installFiles("server",tempFolder,logfile)
    except Exception as error:
        print("Er is een error in InstallFiles {}".format(error))
        exit()

    os.chdir(serverApiDir)

    try:    
        installDependencies(logfile)
    except Exception as error:
        print("Er is een fout opgetreden bij het installeren van de dependencies")
        exit()

    try:
        databaseSetup(logfile)
    except Exception as error:
        print("Er is een error in database setup {}".format(error))
        exit()

    try:
        mods.restartDaemon("config-server-api",logfile,debug)
    except Exception as error:
        print("Er is een error in restart Daemon: {}".format(error))
        exit()

def installWebClient(tempFolder,debug,logfile):
    """
    Installeert de Web client onder apache

    :param str tempFolder: De folder waar de zipfile naartoe is uitgepakt
    :param bool debug: aanzetten debug logging
    :param str logfile: het logfile object
    """
    try:
        # config client
        logfile.write("{} Installeren van de web client\n".format(datetime.today()))
        clientDir = Path(os.path.join(tempFolder,"config/client/"))
        os.chdir(clientDir)
        
        mods.deleteDirectory(os.path.join(clientDir,"dist"),logfile)

        # recreate build folder en build app
        os.mkdir("dist")
        
        compileSource("client",logfile)
        installFiles("client",tempFolder,logfile)
        mods.restartDaemon("apache2",logfile,debug)
        # end config client

        logfile.write("{} De bestanden zijn gekopieerd naar directory: {}\n".format(datetime.today(),scriptfolder))
        if debug:
            print("[DEBUG] Bestanden zijn gekopieerd naar de scriptsfolder")
        logfile.write("{} De webclient is geinstallleerd\n".format(datetime.today()))
    except Exception as error:
        logfile.write("{} Er is iets fout gegaan bij het installeren van de web client. De error is: {}\n".format(datetime.today(),error))
        exit()