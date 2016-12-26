import os
import re
import json
import nose
import coverage
import subprocess
import hashlib
from glob import glob
from file_observer import MapMakerObserver
from filewatch import file_updated_subject, Watcher
from git import Repo
from git.exc import NoSuchPathError, GitCommandError

class MapMaker:
    
    # dict of path/ignore objects
    watch_paths = {} 

    # Re-run build_map when this % of the codebase has changed
    delta_threshold = 0.1
    
    # Observers that notify the mapmaker when a file or git branch changes 
    observers = []
    
    def __init__(self, watch_paths, delta_threshold):

        # Initialize local data store directories
        if not os.path.isdir('.map_data'):
            os.mkdir('.map_data')
        if not os.path.isdir('.repo_data'):
            os.mkdir('.repo_data')

        self.delta_threshold = delta_threshold
        # Initialize observers for each watch_path
        for path in watch_paths:
            # Build initial maps

            # TODO: Check for map existence/branch/change delta
            self._make_test_map_current(path['path'], path['ignore'])

            # Initialize file watchers
            obs = MapMakerObserver(self, path['path'])
            file_updated_subject.register_observer(obs)
            self.watch_paths[path['path']] = path['ignore']
            
            # TODO: Debugging - delete
            # self._get_delta(path['path'])
            # End debugging

        watcher = Watcher()
        watcher.run()

    def _make_test_map_current(self, path, ignore):
        """ Create or ovewrite map data for a repository's current branch """
        tests = self._collect_tests(path)
        repo = Repo(path)
        branch = repo.active_branch.name
        commit = self._make_new_commit(path, branch)
        self._build_map(path, ignore, tests, branch, commit)

    def _make_new_commit(self, path, branch):
        """ 
            Makes a new commit on MapMaker's branch for this map version 

            This is used to compute a diff against the working copy of the 
            user's branch, which provides a heuristic for change
        """
        path_hash = hashlib.md5(path).hexdigest()

        # Create mirror repo
        try:
            repo = Repo('.repo_data/'+path_hash)
        except NoSuchPathError:
            repo = Repo.init('.repo_data/'+path_hash)

        git = repo.git
        # TODO: Add working repo as remote
            # TODO: Use subprocess if the git wrapper can't do it

        # Create and checkout mirror branch if it doesn't exist
        try: 
            git.checkout(branch)         
        except GitCommandError:
            git.checkout(b=branch)

        # TODO: Copy all the files from working path/branch over to data path/branch

        # TODO: Commit them

    def _collect_tests(self, watch_path):
        """ Gets a list of tests to run """        
        
        # nose prints to stderr
        p = subprocess.Popen(['nosetests', '-v', '--nocapture', '--collect-only', watch_path], stderr=subprocess.PIPE)
        _, test_output= p.communicate()
        lines = test_output.split('\n')
        nose_args = self._format_test_paths(lines)
        return nose_args
    
    def _build_map(self, watch_path, ignore, test_list, branch, commit):
        """ Builds a test map for a watch path/git branch combination """
        test_map = {'commit_hash': commit} 
         
        # List of project files 
        file_list =  [y for x in os.walk(watch_path) for y in glob(os.path.join(x[0], '*.py'))]
        filtered = []
        for f in file_list:
            for ig in ignore:
                if not f.startswith(ig):
                    filtered.append(f)
        file_list = filtered

        for path in test_list:
            cov = coverage.Coverage()
            cov.start()
            test_path = path[0]+'.py:'+path[1]
            result = nose.run(argv=['--nocapture', watch_path+'/'+test_path])
            cov.stop()
            cov.save()

            for file_name in file_list:
                line_numbers_covered = cov.data.lines(file_name)
                if line_numbers_covered:
                    if file_name not in test_map:
                        test_map[file_name] = {}
                    for line in line_numbers_covered:
                        if line not in test_map[file_name]:
                            test_map[file_name][line] = []
                        test_map[file_name][line].append(test_path)
        
        # Save the test map data in a directory referencing its repo and branch
        watch_path_hash = hashlib.md5(watch_path).hexdigest()
        branch_hash = hashlib.md5(branch).hexdigest()
        if not os.path.isdir('.map_data/'+watch_path_hash):
            os.mkdir('.map_data/'+watch_path_hash)
        if not os.path.isdir('.map_data/'+watch_path_hash+'/'+branch_hash):
            os.mkdir('.map_data/'+watch_path_hash+'/'+branch_hash)

        with open('.map_data/'+watch_path_hash+'/'+branch_hash+'/test_map.json', 'w') as fp:
            json.dump(test_map, fp)

    def _get_delta(self, watch_path):
        """ Returns the % change of code since the last map """
        working_repo = Repo(watch_path)
        # TODO: Get data repo         

        # TODO: Compare
        diff = repo.head.commit.diff()

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

    def branch_change(self, watch_path):
        """ Called from file observer on git branch change"""
        print "Branch change: "+watch_path

    def file_change(self, watch_path):
        """ Called from file observer on file change without git branch change"""
        print "file in directory changed: "+watch_path
