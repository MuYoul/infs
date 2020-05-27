#!/bin/bash

export INFS_VENV=$(pwd)/venv_infs
source ${INFS_VENV}/bin/activate

export FLASK_APP=$(pwd)/inf/app.py
flask run -h 0.0.0.0 -p 9001
