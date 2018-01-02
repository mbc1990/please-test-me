import json
import sys
import nose
import subprocess

def main():
    # which_nosetests = '/Users/malcolm/.pyenv/shims/nosetests'
    file_path = sys.argv[1]
    line_number = sys.argv[2]

    print file_path + ":" + line_number
    return

    which_nosetests = 'nosetests'

    with open('test_map.json') as fp:    
        test_map = json.load(fp)

    if file_path not in test_map:
        print "WARNING: "+file_path+" has no known tests"
        return

    if line_number not in test_map[file_path]:
        print "WARNING: Line number "+line_number+" has no known tests"
        return
    '''
    tests = test_map[file_path][line_number]
    for test in tests:
        print test
        print subprocess.check_output([which_nosetests, '-v', '--nocapture', test])
    '''

if __name__ == "__main__":
    main()
