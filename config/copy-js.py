import os
from pathlib import Path

workingDir = /usr/src/server-api/src
for file in workingDir.glob("**/*.js"):
    source = file.absolute()
    destination = Path(destinationDir).joinpath(*source.parts[index+1:])

    os.system("cp {} {}".format(source,destination))