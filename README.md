# please-test-me
Find &amp; run tests that cover a particular statement

## Setup
Put `build_map.py` and `test_current_line.py` in your repository directory

Add this to your .vimrc:

`nnoremap <F3> :execute ":!python test_current_line.py" expand('%:p') line('.')<CR>`

Run `nosetests -v --nocapture --collect-only > nose_output.txt 2>&1` to generate a list of all your tests 

Then run `python build_map.py` to generate a `test_map.json` file

## Usage 
Left as an exercize to the reader

## TODO
    - Use the nose python client to collect tests instead of a shell command
    - Refactor into a class with abstract methods, and a python/nosetests implementation 
    - Tests
    - Deal with "staleness" of test_map.json
