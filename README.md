# please-test-me
Find &amp; run tests that cover a particular statement

## Setup
1. Download the repository
2. Create a new virtualenv, install requirements.txt 
3. run `python install.py`
4. Add the directories you want to track to `~/.please-test-me/conf.json`
5. Create a cron job that runs `~/.please-test-me/build_maps.py` however frequently you like
6. Add this to your `.vimrc`: `nnoremap <F3> :execute ":!~/.please-test-me/bootstrap_tcl.sh" expand('%:p') line('.')<CR>`

## Usage 
1. Highlight a line and run F3
