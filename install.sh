#!/bin/bash

[ ! -d .env ] && python3 -m venv .env
source .env/bin/activate

pip3 install --upgrade pip
pip3 install numpy==1.19.0 wheel
pip3 install -r venv_requirements.txt
python3 setup.py develop
