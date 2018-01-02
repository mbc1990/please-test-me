#!/bin/sh

# This is kind of hacky but you can thank python dependency management for that.
# Basically, this is the script invoked by the text editor to run tests for the
# current line. It activates the please test me virtualenv, and invokes the
# test_current_line.py script which reads from the map data to find the tests
# that cover this line. 

# THEN, please_test_me.py uses subprocess.popen to invokes run_tcl.sh, which
# activates the virtualenv of the *project* directory and then runs the relevant
# tests in the project dir, with the project virtualenv

cd ~/.please-test-me
. venv/bin/activate
python test_current_line.py $1 $2
