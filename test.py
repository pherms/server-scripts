from pathlib import Path
import os

working_dir = Path("./config/server/src")
index = working_dir.parts.index('src')
target_dir = "/opt/server-api/"

for path in working_dir.glob("**/*.js"):
    source = path.absolute()
    destination = Path(target_dir).joinpath(*path.parts[index+1:])

    print(destination)

# for filename in glob.iglob("config/server/src/*.js"):
#     print(filename)