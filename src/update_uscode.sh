#!/bin/sh
LOGFILE=~/log/uscode.log
touch $LOGFILE
date >> $LOGFILE
cd ~/sources/uscode
git pull -q origin master
rm -rf code
python /home/shawn/sources/uscode/src/retrieve_code.py . >> $LOGFILE
git add code >> $LOGFILE
DIFFLOG=`git status --porcelain`
if [ ! -z "$DIFFLOG" ]; then
    echo "$DIFFLOG" >> $LOGFILE
    git commit -m "`date`"
    git tag -f -a -m "Daily tag" `date +"%F"`
    git push --tags origin master
fi

