from datetime import *
from json import JSONDecodeError
import os
import subprocess
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

    logfile = mods.openLogFile(logfilepath,"update",debug)
    hostname = mods.getHostname(logfile)

    try:
        os.chdir('/tmp')
        versionfile = scriptfolder + "version.txt"

        try:
            response = requests.get(apiurl)

            if response.status_code == 200:
                if debug:
                    print("[DEBUG] API request succesvol uitgevoerd: {}".format(response.status_code))

                logfile.write("{} API request naar {} succesvol uitgevoerd. Status code: {}\n".format(datetime.today(),apiurl,response.status_code))    
                # responseObject = json.loads(json.dumps(response.json()))
                responseDictionary = response.json()
                
                if debug:
                    prettyJson = json.dumps(responseDictionary, indent=4)
                    print(prettyJson)

                latestVersion = responseDictionary.get('tag_name')
                zipUrl = responseDictionary.get('zipball_url')
                if debug:
                    print("[DEBUG] latest version {}\n[DEBUG] zipUrl: {}".format(latestVersion,zipUrl))
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
                installedVersion = open(versionfile,"r").readline()
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
                if debug:
                    print("[DEBUG] zipfile is gedownload. statuscode: {}".format(requestZip.status_code))
                    
                if requestZip.ok:
                    zipFile = zipfile.ZipFile(io.BytesIO(requestZip.content))
                    zipcontent = zipFile.namelist()
                    zipinfo = zipFile.getinfo()
                    if debug:
                        print("[DEBUG] zipcontent: {}".format(zipcontent))
                        print("[DEBUG] zipinfo: {}".format(zipinfo))
                    zipFile.extractall(".")
            except Exception as error:
                logfile.write("{} Er is iets fout gegaan tijdens het downloaden van de zipfile\n".format(datetime.today()))
                logfile.write("{} De foutmelding is: {}\n".format(datetime.today(),error))
                

            # https://api.github.com/repos/pherms/server-scripts/releases/latest return json
            # tag_name en zipbal_url
# Stappen:
# - installeren requirements file
# - versiefile inlezen
# - request naar api doen
# - inlezen response van api velden tag_name en zipball_url opslaan
# - versie vergelijken met geïnstalleerde versie
# - wanneer versies verschillen, dan zipball downloaden
# - zipball uitpakken of kopieren naar scriptsfolder
# - tagname wegschrijven naar versiefile


        subject = "Autoupdate op server {hostname} is succesvol uitgevoerd"
        message = "Autoupdate op server {hostname} is succesvol uitgevoerd"
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