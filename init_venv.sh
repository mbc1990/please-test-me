#!/bin/sh

# Creates the virtualenv for PTM and installs requirements
# You need to have pip and virtualenv in your path for this to work

cd ~/.please-test-me
virtualenv venv 
. venv/bin/activate

# --no-cache-dir is a safeguard against people who "accidentally" ran
# pip as root and screwed up permissions in their cache dir
pip install -r requirements.txt --no-cache-dir
