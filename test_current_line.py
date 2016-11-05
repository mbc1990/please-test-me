import json
import sys
import nose

def main():
    with open('test_map.json') as fp:    
        test_map = json.load(fp)

    file_path = sys.argv[1]
    line_number = sys.argv[2]

    if file_path not in test_map:
        print "WARNING: "+file_path+" has no known tests"
        return

    if line_number not in test_map[file_path]:
        print "WARNING: Line number "+line_number+" has no known tests"

    tests = test_map[file_path][line_number]
    for test in tests:
        print test
        nose.run(argv=['-vv', '--nocapture', test])

if __name__ == "__main__":
    main()
