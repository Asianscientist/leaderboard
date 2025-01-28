#!/bin/bash
export PYTHONPATH=/home/samandar/samandar/leaderboard:$PYTHONPATH
export DJANGO_SETTINGS_MODULE="config.settings"
cd /home/samandar/samandar/leaderboard
source venv/bin/activate
/usr/bin/python3 /home/samandar/samandar/leaderboard/main/utils.py

