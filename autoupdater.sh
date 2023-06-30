#/bin/bash

cd /scripts/server-scripts

git checkout main
git fetch
changes=$(git diff origin/main)

if [[ -n "$changes"]]; then
    echo "Changes in remote gdetecteerd. Nu downloaden"
    git pull
    git branch | grep -v "main" | xargs git branch -D
else
    echo "Er zijn geen veranderingen"
fi