#!/usr/bin/zsh

# Copyright: 2016, olf, olf@querfunk.de
# Inspired by: http://blog.philippklaus.de/2013/03/start-a-python-tool-or-web-app-that-uses-virtualenv-on-system-startup-using-systemd/

# CONSTANTS
HOME=/home/qfrecord
VENVNAME=qfmediathek
VENVDIR=${HOME}/.virtualenvs/${VENVNAME}
APPDIR=${HOME}/qfmediathek
APPNAME=qfmediathek.py

# ACTIVATE THE VIRTUALENV
source ${VENVDIR}/bin/activate

# START THE APPLICATION
python ${APPDIR}/${APPNAME}

