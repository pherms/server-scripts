from datetime import *
from json import JSONDecodeError
import os
import requests
import zipfile
import io
import json
import modules as mods

def main():
    config = mods.readConfig()
    logfilepath = config["logfilepath"]
    debug = bool(config["debug"])
    scriptfolder = config["scriptspath"]
    apiurl = config["apiurl"]
    timers = config["timerUnits"]
    services = config["serviceUnits"]

    logfile = mods.openLogFile(logfilepath,"update",debug)
    hostname = mods.getHostname(logfile)

    try:
        versionfile = scriptfolder + "version.txt"

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
                    logfile.write("{} De zipfile is uitgepakt naar directory /tmp/{}\n".format(datetime.today(),tempFolder))
                
                if os.path.exists(tempFolder):
                    os.system("cp -r " + tempFolder + "/* /home/pascal/scripts/")
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
                        os.system("find " + scriptfolder + " -name \"*.sh\" -exec chmod +x {} \;")

                except Exception as error:
                    logfile.write("{} Er is een fout opgetreden tijdens het instellen van het execute bit op .sh files.".format(datetime.today()))

                # cleanup /tmp folder
                try:
                    if os.path.exists(tempFolder):
                        os.system("rm -rf " + tempFolder)
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

            # Installeer daemons
            for timer in timers:
                status = mods.checkIfDaemonIsInstalled(timer,logfile,debug)
                if status == "installed":
                    mods.startDaemon(timer,logfile,debug)
                if status == "updated":
                    mods.restartDaemon(timer,logfile,debug)
                if status == "error":
                    logfile.write("{} Er is een fout opgetreden tijden het installeren van timer: {}\n".format(datetime.today()))
                    if debug:
                        print("[DEBUG] Er is een fout opgetreden bij het installeren van timer: {}".format(timer))

            for service in services:
                status = mods.checkIfDaemonIsInstalled(service,logfile,debug)
                if status == "installed":
                    mods.startDaemon(service,logfile,debug)
                if status == "updated":
                    mods.restartDaemon(service,logfile,debug)
                if status == "error":
                    logfile.write("{} Er is een fout opgetreden tijden het installeren van service: {}\n".format(datetime.today()))
                    if debug:
                        print("[DEBUG] Er is een fout opgetreden bij het installeren van service: {}".format(service))

        else:
            if debug:
                print("[DEBUG] Laatste versie is al geïnstalleerd. Er hoeft niets te worden gedaan.")
            logfile.write("{} De laatste versie: {} is al geïnstalleerd. De updater wordt nu gesloten.\n".format(datetime.today(),installedVersion))

        subject = "Autoupdate op server {hostname} is succesvol uitgevoerd".format(hostname=hostname)
        message = "Autoupdate op server {hostname} is succesvol uitgevoerd\nZie de bijgevoegde logfile.\nDe geïnstalleerde versie is: {latestVersion}.".format(hostname=hostname,latestVersion=latestVersion)
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
        # mods.sendMailFailedUpdate(hostname,message)

    mods.closeLogFile(logfile)
    # mods.sendMail(subject,message,logfile)

if __name__ == '__main__':
    main()