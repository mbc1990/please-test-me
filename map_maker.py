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
    
    # Directory where "mirror" repositories are stored 
    repo_data_dir = '' 
    
    def __init__(self, watch_paths, delta_threshold, repo_data_dir='/Users/mbc/.repo_data/'):

        self.delta_threshold = delta_threshold
        self.repo_data_dir = repo_data_dir 

        # Initialize local data store directories
        if not os.path.isdir('.map_data'):
            os.mkdir('.map_data')
        if not os.path.isdir(self.repo_data_dir):
            os.mkdir(self.repo_data_dir)

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
            self._get_delta(path['path'])
            # End debugging
        
        # Start file change watcher registered by file_updated_subject
        watcher = Watcher()
        watcher.run()

    def _make_test_map_current(self, path, ignore):
        """ Create or ovewrite map data for a repository's current branch """
        tests = self._collect_tests(path)
        repo = Repo(path)
        branch = repo.active_branch.name
        try:
            commit = self._make_new_commit(path, branch)
            self._build_map(path, ignore, tests, branch, commit)
        except GitCommandError:
            print "No changes, not building new map"

    def _make_new_commit(self, path, branch):
        """ 
            Makes a new commit on MapMaker's branch for this map version 

            This is used to compute a diff against the working copy of the 
            user's branch, which provides a heuristic for change
        """
        path_hash = hashlib.md5(path).hexdigest()

        # Create mirror repo
        try:
            repo = Repo(self.repo_data_dir+path_hash)
        except NoSuchPathError:
            repo = Repo.init(self.repo_data_dir+path_hash)

        git = repo.git

        # Create and checkout mirror branch if it doesn't exist
        try: 
            git.checkout(branch)         
        except GitCommandError:
            git.checkout(b=branch)
        
        # Add working repo as remote, whose working copy we'll diff against in _get_delta
        #working_repo = Repo(path)
        #repo.create_remote('working', path)

        # Remove everything from the last recorded state
        try:
            git.rm(".", r=True)
        except GitCommandError as e:
            # trivial case, nothing in repository
            # TODO: Make assertion
            pass
        
        # Copy the current working copy of the working repo into the data repo
        subprocess.call(['cp', '-R', path, self.repo_data_dir+path_hash])
        git.add(A=True)
        git.commit(m="Working changes at %s" % "TODO: Add timestamp")
        commit_hash = repo.head.commit.hexsha
        return commit_hash

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

    def _get_mirror_repo(self, path):
        """ Returns the mirror Repo instance, with the working repo's current branch checked out """
        path_hash = hashlib.md5(path).hexdigest()
        mirror_repo = Repo(self.repo_data_dir+path_hash)
        working_repo = Repo(path)
        branch = working_repo.active_branch.name
        mirror_repo.git.checkout(branch)
        return mirror_repo

    def _get_delta(self, watch_path):
        """ Returns the % change of code since the last map """
        working_repo = Repo(watch_path)
        mirror_repo = self._get_mirror_repo(watch_path)

        # TODO: Compare to mirror repo/branch
        #diff = repo.head.commit.diff()

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
        # TODO: If branch doesn't exist in mirror repo 
            # TODO: Create new branch in/Users/mbc/.repo_data and make new test map

    def file_change(self, watch_path):
        """ Called from file observer on file change without git branch change"""
        print "file in directory changed: "+watch_path
        # TODO: if delta is > threshold
            # TODO: Make new test map 
