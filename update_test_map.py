import os
import re
import sys
import coverage
import nose
import json
from glob import glob


def main():
    """
    Runs the tests one at a time, tracking what files they cover

    N.B. This runs in the host virtual environment
    """
    # Get tests
    dir = sys.argv[1]
    test_paths = get_test_paths(dir)

    # Get test map from disk
    test_map = None
    working_dir = os.path.expanduser("~") + "/.please-test-me/"
    with open(working_dir + "test_map.json") as fp:
        test_map = json.load(fp)

    # Absolute path of project
    project_dir = dir

    # List of project files
    file_list =  [y for x in os.walk(project_dir) for y in glob(os.path.join(x[0], '*.py'))]  # noqa

    for path in test_paths:
        cov = coverage.Coverage()
        cov.start()
        test_path = path[0]+'.py:'+path[1]
        nose.run(argv=['--nocapture', dir + test_path])
        cov.stop()
        cov.save()

        # For each project file
        for file_name in file_list:
            line_numbers_covered = get_covered_lines(file_name, cov)
            if line_numbers_covered:
                if file_name not in test_map:
                    test_map[file_name] = {}
                for line in line_numbers_covered:
                    if line not in test_map[file_name]:
                        test_map[file_name][line] = []
                    test_map[file_name][line].append(test_path)

    with open(working_dir + "test_map.json", "w") as fp:
        json.dump(test_map, fp)


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
                path = testpath.group().replace('(', '').replace(')', '')
                class_name = re.search(r'([A-Z][a-z0-9]+)+', path).group(0)
                test_file_path = path.split(class_name)[0][:-1].replace('.','/')  # noqa
                dot_path = class_name+'.'+test_name
                nose_args.append((test_file_path, dot_path))
        return nose_args


def get_covered_lines(path, cov):
    return cov.data.lines(path)


if __name__ == "__main__":
    main()
