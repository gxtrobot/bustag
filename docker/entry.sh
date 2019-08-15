#!/bin/bash

# start cron
service cron start

python bustag/app/index.py
