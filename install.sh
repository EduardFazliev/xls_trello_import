#!/usr/bin/env bash

virtualenv venv || echo 'Please install virtualenv!'

. venv/bin/activate

wget -O ./get-pip.py https://bootstrap.pypa.io/get-pip.py
python get-pip.py || echo 'Can not install pip, aborting'
pip install -r requirements.txt

deactivate

echo -e '#####Instructions#####\nTo run script:\n1. Activate virtualenv (for example ". venv/bin/activate")\n2. Run script.'
