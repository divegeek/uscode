#!/bin/sh
date
pushd ~/sources/uscode
git pull origin master
rm -rf code
python /home/shawn/sources/uscode/src/retrieve_code.py .
git commit -m "`date`" -a
git tag -f -a -m "Daily tag" `date +"%F"`
git push --tags origin master
popd
