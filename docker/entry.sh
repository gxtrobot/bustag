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

gunicorn bustag.app.index:app --bind='0.0.0.0:8080'
