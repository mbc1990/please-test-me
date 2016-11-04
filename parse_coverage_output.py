import re
import coverage
from coverage import CoverageData
import nose
import tests
from subprocess import call

def main():
    test_paths = get_test_paths()
    for path in test_paths:
        cov = coverage.Coverage()
        cov.start()
        test_path = path[0]+'.py:'+path[1]
        result = nose.run(argv=['--nocapture', test_path])
        cov.stop()
        cov.save()
        # For each project file
        line_numbers_covered = get_covered_lines('/Users/mbc/Documents/git_repos/please-test-me/product.py', cov)
        print test_path
        print '--->'+str(line_numbers_covered)

    # TODO: Save in map of filename -> line number -> testname


def get_test_paths():
    with open('nose_output.txt') as f: # Generate this file by running nosetests -v --nocapture > filename 2>&1
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
                # nose_arg = test_file_path + '.'+
                #nose_args.append(nose_arg)
        return nose_args 

def get_covered_lines(path, cov):
    return cov.data.lines(path)


if __name__ == "__main__":
    main()
