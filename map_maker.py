import re
import subprocess
from file_observer import MapMakerObserver
from filewatch import file_updated_subject, Watcher

class MapMaker:
    
    # List of absolute paths to directories that are being watched
    watch_paths = []

    # Re-run build_map when this % of the codebase has changed
    delta_threshold = 0.1
    
    # Observers that notify the mapmaker when a file or git branch changes 
    observers = []
    
    def __init__(self, watch_paths, delta_threshold):
        # Initialize observers for each watch_path
        for path in watch_paths:
            # TODO: Put this in its own function since it's going to be called from file and branch change

            # Build initial maps
            # TODO: Check for map existence/branch/change delta
            tests = self.collect_tests(path)
            self.build_map(path, tests)

            # Initialize file watchers
            obs = MapMakerObserver(self, path)
            file_updated_subject.register_observer(obs)

        print "Watchers initialized" 
        watcher = Watcher()
        watcher.run()

    def branch_change(self, watch_path):
        """ Called from file observer on git branch change"""
        print "Branch change: "+watch_path

    def file_change(self, watch_path):
        """ Called from file observer on file change without git branch change"""
        print "file in directory changed: "+watch_path

    def collect_tests(self, watch_path):
        """ Gets a list of tests to run """        
        
        # nose prints to stderr
        p = subprocess.Popen(['nosetests', '-v', '--nocapture', '--collect-only', watch_path], stderr=subprocess.PIPE)
        _, test_output= p.communicate()
        lines = test_output.split('\n')
        nose_args = self._format_test_paths(lines)
    
    def build_map(self, watch_path, test_list):
        """ Builds a test map for a watch path """
        pass

    def get_change_delta(self, watch_path):
        """ Returns the % change of code since the last map """
        pass

    def poll_paths(self):
        """ Runs an infinite loop checking for changes """
        pass

    def _format_test_paths(self, nose_output):
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
