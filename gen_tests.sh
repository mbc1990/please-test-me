#!/bin/sh

# Goes to the repository's directory ($1), activates its venv ($2)
# then runs the tests (with collect only mode) and writes the 
# output to .nose_output.txt

cd $1
. $2/bin/activate
nosetests -v --nocapture --collect-only > .nose_output.txt 2>&1 
