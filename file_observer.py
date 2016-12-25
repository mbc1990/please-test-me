from filewatch import ObserverBase
from git import Repo

class MapMakerObserver(ObserverBase):
    
    map_maker = None
    watch_path = ''
    last_branch = ''
    repo = None

    def __init__(self, map_maker, watch_path):
        self.map_maker = map_maker
        self.watch_path = watch_path
        self.repo = Repo(watch_path)
        self.last_branch = self.repo.active_branch.name

    def notify(self, *args, **kwargs):
        current_branch = self.repo.active_branch.name
        if current_branch != self.last_branch:
            self.last_branch = current_branch
            self.map_maker.branch_change(self.watch_path)
        else:
            self.map_maker.file_change(self.watch_path)
