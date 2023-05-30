import datetime
import modules as mods
# from datetime import datetime

config = mods.readConfig()
backupdir = config['backuppath']
# jaar,week,dag = datetime.today().isocalendar()[:3]
# date = "2023-05-04"

# jaar,week,dag = datetime.date.fromisoformat(date).isocalendar()[:3]
# print(jaar)
# print(week)
# print(dag)

files = mods.getCreationTime(backupdir)

for file in files.keys():
    fileName = file
    backupFileDate = datetime.datetime.strftime(files.get(fileName),'%Y-%m-%d')
    
    print(fileName)
    print(backupFileDate)
    jaar,week,dag = datetime.date.fromisoformat(backupFileDate).isocalendar()[:3]
    currentJaar,currentWeek,currentDag = datetime.date.fromisoformat(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')).isocalendar()[:3]
    print(jaar)
    print(week)
    print(dag)
    print(currentJaar)
    print(currentWeek)
    print(currentDag)

    # 