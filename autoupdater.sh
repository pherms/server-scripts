#/bin/bash

cd /scripts/server-scripts
git pull
git branch | grep -v "main" | xargs git branch -D
# nu een verandering
