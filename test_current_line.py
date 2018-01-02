import os
import json
import sys
import nose
import subprocess

def main():
    file_path = sys.argv[1]
    line_number = sys.argv[2]

    print file_path + ":" + line_number

    which_nosetests = "nosetests"
    working_dir = os.path.expanduser("~") + "/.please-test-me/"
  
    # If you ran install.py, this file will always exist
    with open(working_dir + "test_map.json") as fp:    
        test_map = json.load(fp)

    if file_path not in test_map:
        print "WARNING: "+file_path+" has no known tests"
        return

    if line_number not in test_map[file_path]:
        print "WARNING: Line number "+line_number+" has no known tests"
        return

    tests = test_map[file_path][line_number]

    with open(working_dir + "conf.json") as fp:    
        conf = json.load(fp)
        for option in conf["dirs_to_track"]:
            if option["dir"] in file_path:
                dir = option["dir"]
                venv = option["venv"]
                for test in tests:
                    subprocess.call(["./bootstrap_run_test.sh", dir, venv, test])
                return

    print "Unable to find matching project directory"

if __name__ == "__main__":
    main()
