#!/bin/sh

# Goes to the repository's directory ($1), activates its venv ($2),
# then runs each test, storing its coverage output

cd $1
. $2/bin/activate
# This isn't great, but we *need* it in the virtualenv to get coverage details
pip install coverage
python ~/.please-test-me/update_test_map.py $1
