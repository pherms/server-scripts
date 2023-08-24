import json

class config(object):
    def __init__(self,filetype, *args, **kwargs):
        self.filetype = filetype
        self.backuppath = kwargs['backuppath']
        self.logfilepath = logfilepath
        self.sourceslocation = sourcesLocation
        self.compression = compression
        self.filesize = filesize
        self.backupserver = backupserver
        self.copycommand = copycommand
        self.remotefilepath = remotefilepath
        self.mailserver = mailserver
        self.mailRecipient = mailRecipient
        self.mailSender = mailSender
        self.hostType = hostType

jsonData = json.loads("/etc/server-scripts/backup-config.json")
conf = config(**jsonData)

print(type(conf))
print(conf.backuppath)


# class app:

#     def __init__(self):
#         f = open("/etc/server-scripts/backup-config.json","rb")
#         jsonObject = json.load(f)
#         self.data = jsonObject
        
# filetype": "tar",
#     "backuppath": "/home/pascal/backup/",
#     "logfilepath": "/home/pascal/log/backup/",
#     "sourcesLocation": "/etc/server-scripts/sources",
#     "compression": "bz2",
#     "filesize": "2GB",
#     "backupserver": "brisbane.merel107.local",
#     "copycommand": "scp",
#     "remotefilepath": "/vol/data/fs/backup/",
#     "mailserver": "adelaide.merel107.local",
#     "mailRecipient": "pherms@outlook.com",
#     "mailSender": "no_reply@pascalherms.nl",
#     "hostType": "vm"        