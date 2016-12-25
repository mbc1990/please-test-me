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
        pass
    
    def build_map(self, watch_path):
        """ Builds a test map for a watch path """
        pass

    def get_change_delta(self, watch_path):
        """ Returns the % change of code since the last map """
        pass

    def poll_paths(self):
        """ Runs an infinite loop checking for changes """
        pass
