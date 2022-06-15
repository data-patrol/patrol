import os

from patrol.jobs.base_job import BaseJob
from patrol import executors

class OnDemandJob(BaseJob):
    """
    Implements an on-demand job that can be executed either manually or automatically by trigger (such as API)
    """

    def __init__(
            self):
        super(OnDemandJob, self).__init__()

    def add_check_to_job(self, check):
        self.executor.add_check_to_queue(check)    
    
    def _run(self):
        self.executor.start()
        self.executor.execute_sync()

