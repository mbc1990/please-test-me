# please-test-me
Find &amp; run tests that cover a particular statement

## Setup
Put `build_map.py` and `test_current_line.py` in your repository directory

Add this to your .vimrc:

`nnoremap <F3> :execute ":!python test_current_line.py" expand('%:p') line('.')<CR>`

Then run `python build_map.py` to generate a `test_map.json` file

## Usage 
Left as an exercize to the reader

## TODO
    - Use the nose python client to collect tests instead of a shell command
    - Refactor into a class with abstract methods, and a python/nosetests implementation 
    - Write some tests haha 
    - Make it easier to use with a project.
        - Config file
        - Maybe some kind of global config file that specifies active project and test directories
        - Should not be something you "add" to a project, should be a global tool that you "point" at a project
        - Testmaps should be dotfiles and stored centrally (that could be configurable too I suppose)
        - Could run centrally and listen internally on a (configurable) port
            - Or could receive process level messages
    - Deal with "staleness" of test_map.json
        - Decide whether or not to make git a requirement, and see what kind of information can be produced from it
            - If git is used to handle staleness, at least make it disablable
        - Use a filewatcher to detect and respond to changes
    - Find a cleaner solution for dealing with pyenv/venv
        - Ideally, use the python from the project directory
    - Implement integrations for popular text editors, probably:
        - Sublime
        - Atom
        - Pycharm
    - Figure out why function and class definitions don't count for coverage
    - Wrap in a class, not module level functions 
    - Finish automating the test collection step
