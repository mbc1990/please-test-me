import re
import sys
import coverage
from coverage import CoverageData
import nose
import json
from glob import glob

def main():
    # Get tests
    dir = sys.argv[1]
    test_paths = get_test_paths(dir)
    print test_paths

def get_test_paths(dir):
    """
    Parses .nose_output.txt to get a list of available tests in the project
    
    N.B. All tests must be members in classes inheriting from unittest.TestCase
    """
    with open(dir + ".nose_output.txt") as f: 
        lines = f.readlines()
        nose_args = []
        for line in lines:
            testpath = re.search(r"\(.*\)", line)
            if testpath:
                test_name = line.split(' ')[0]
                path = testpath.group().replace('(','').replace(')','')
                class_name = re.search(r'([A-Z][a-z0-9]+)+', path).group(0)
                test_file_path = path.split(class_name)[0][:-1].replace('.','/')
                dot_path = class_name+'.'+test_name
                nose_args.append((test_file_path, dot_path))
        return nose_args 

if __name__ == "__main__":
    main()
