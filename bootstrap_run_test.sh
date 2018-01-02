#!/bin/sh

# Goes to the repository's directory ($1), activates its venv ($2),
# then runs a single test ($3)

cd $1
. $2/bin/activate
nosetests -v --nocapture $3
