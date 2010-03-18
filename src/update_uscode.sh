#!/bin/sh
date
pushd ~/sources/uscode
git pull origin master
rm -rf code
python /home/shawn/sources/uscode/src/retrieve_code.py .
git add code
git status > /dev/null
if [ $? -eq 0 ]; then
    git commit -m "`date`" -a
    git tag -f -a -m "Daily tag" `date +"%F"`
    git push --tags origin master
fi
popd
