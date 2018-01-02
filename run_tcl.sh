#!/bin/sh


# Activate virtualenv
cd $1
. $2/bin/activate
nosetests -v --nocapture $3
