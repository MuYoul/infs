#!/bin/bash

export INFS_VENV=$(pwd)/venv_infs
python -m venv $INFS_VENV

source $INFS_VENV/bin/activate
