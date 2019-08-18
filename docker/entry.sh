#!/bin/bash

# check if crontab.txt exists

echo `pwd`

if [ -e './data/crontab.txt' ]
then
    crontab data/crontab.txt
    echo 'use new crontab.txt'
else
    echo 'use default crontab.txt'
fi
# start cron
service cron start

python bustag/app/index.py
