import modules as mods
import os
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
        print("Sourcedir in InstallFiles functie: {}".format(sourceDir))
        print("Destination in InstallFiles functie: {}".format(destinationDir))
        index = Path(sourceDir).parts.index('src')
        print("Index: {}".format(index))
        workingDir = Path(os.path.join(sourceDir,"src"))
    except Exception as error:
        print("Er is een fout opgetreden: {}".format(error))
        exit()

    try:
        logfile.write("{} Kopieren van de gecompilede sources\n".format(datetime.today()))
        os.system("cp -r {}/ {}".format(os.path.join(sourceDir,"dist"),destinationDir))

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
            os.system("cp {} {}".format(source,destinationDir))

            logfile.write("{} Kopieren van prisma directory\n".format(datetime.today()))
            os.system("cp -r {} {}".format(os.path.join(sourceDir,"prisma"),destinationDir))

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
