import re
import coverage
from coverage import CoverageData
import nose
import json
from glob import glob
import os
import subprocess

def main():
    # Absolute path of project 
    project_dir = '/Users/mbc/Documents/git_repos/please-test-me/project/'

    # Absolute path of tests
    test_dir = '/Users/mbc/Documents/git_repos/please-test-me/'
    
    # TODO: Doesn't work
    #tests = collect_tests(test_dir)   

    tests = get_test_paths()
    test_paths = format_test_paths(tests)
    print "test paths: "+str(test_paths)
    test_map = {} 
    
    # List of project files 
    file_list =  [y for x in os.walk(project_dir) for y in glob(os.path.join(x[0], '*.py'))]
    
    for path in test_paths:
        cov = coverage.Coverage()
        cov.start()
        test_path = path[0]+'.py:'+path[1]
        result = nose.run(argv=['--nocapture', test_dir+test_path])
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
    
    with open('test_map.json', 'w') as fp:
        json.dump(test_map, fp)

def get_test_paths():
    with open('nose_output.txt') as f: 
        lines = f.readlines()
        return lines

'''
def collect_tests(test_dir):
    which_nosetests = 'nosetests'
    # nosetests -v --nocapture --collect-only > nose_output.txt 2>&1
    import ipdb; ipdb.sset_trace()
    # TODO: This doesn't return the output 
    output = subprocess.check_output([which_nosetests, '-v', '--nocapture', '--collect-only'])
    output = output.split('\n')
    return output
'''


def format_test_paths(nose_output):
        nose_args = []
        for line in nose_output:
            testpath = re.search(r"\(.*\)", line)
            if testpath:
                test_name = line.split(' ')[0]
                path = testpath.group().replace('(','').replace(')','')
                class_name = re.search(r'([A-Z][a-z0-9]+)+', path).group(0)
                test_file_path = path.split(class_name)[0][:-1].replace('.','/')
                dot_path = class_name+'.'+test_name
                nose_args.append((test_file_path, dot_path))
        return nose_args 


def get_covered_lines(path, cov):
    return cov.data.lines(path)


if __name__ == "__main__":
    main()
