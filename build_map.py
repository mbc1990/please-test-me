import re
import coverage
from coverage import CoverageData
import nose
import json
from glob import glob
import os

def main():
    test_paths = get_test_paths()
    test_map = {} 

    # Absolute path of project 
    # TODO: Make relative, pass as argument
    project_dir = '/Users/mbc/Documents/git_repos/please-test-me/project/'
    file_list =  [y for x in os.walk(project_dir) for y in glob(os.path.join(x[0], '*.py'))]
    print file_list
    for path in test_paths:
        cov = coverage.Coverage()
        cov.start()
        test_path = path[0]+'.py:'+path[1]
        result = nose.run(argv=['--nocapture', test_path])
        cov.stop()
        cov.save()

        # For each project file
        for file_name in file_list:
            line_numbers_covered = get_covered_lines(file_name, cov)
            if line_numbers_covered:
                print "coverage detected"
                if file_name not in test_map:
                    test_map[file_name] = {}
                for line in line_numbers_covered:
                    if line not in test_map[file_name]:
                        test_map[file_name][line] = []
                    test_map[file_name][line].append(test_path)
    
    print test_map
    with open('test_map.json', 'w') as fp:
        json.dump(test_map, fp)


def get_test_paths():
    with open('nose_output.txt') as f: 
        lines = f.readlines()
        nose_args = []
        for line in lines:
            testpath = re.search(r"\(.*\)", line)
            if testpath:
                path = testpath.group().replace('(','').replace(')','')
                class_name = re.search(r'([A-Z][a-z0-9]+)+', path).group(0)
                test_file_path = path.split(class_name)[0][:-1].replace('.','/')
                dot_path = class_name+path.split(class_name)[1]
                nose_args.append((test_file_path, dot_path))
        return nose_args 


def get_covered_lines(path, cov):
    return cov.data.lines(path)


if __name__ == "__main__":
    main()
