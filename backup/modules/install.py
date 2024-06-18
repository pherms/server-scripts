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
            sourceDir = Path(os.path.join(tempFolder,"config/client/"))
            destinationDir = config["clientConfigDir"]
        case "server":
            sourceDir = Path(os.path.join(tempFolder,"config/server/"))
            destinationDir = config["serverApiDir"]
    
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

    (sourceDir,destinationDir) = mods.determineConfigFolder(type,tempFolder)
    index = sourceDir.parts.index('src')
    workingDir = os.path.join(sourceDir,"src")

    try:
        logfile.write("{} Kopieren van de gecompilede sources\n".format(datetime.today()))
        os.system("cp -r {}/ {}".format(os.path.join(sourceDir,"dist"),destinationDir))

        if (type == "server"):
            logfile.write("{} Kopieren van additionele javascript files tbv server\n".format(datetime.today()))
            for file in workingDir.glob("**/*.js"):
                source = file.absolute()
                destination = Path(destinationDir).joinpath(*source.parts[index+1:])

                os.system("cp {} {}".format(source,destination))
    except Exception as error:
        print("Er is een fout opgetreden. {}".format(error))
        logfile.write("{} Er is een fout opgetreden. De error is:\n{}".format(datetime.today(),error))
        exit()

def compileSource(type,logfile):
    logfile.write("{} Installeren van packages voor {} source\n".format(datetime.today(),type))
    os.system("npm install")
    logfile.write("{} Compileren van {} source\n".format(datetime.today(),type))
    os.system("npm run build")