import os

from patrol.jobs.base_job import BaseJob
from patrol.check_groups.base_check_group import BaseCheckGroup

class SimpleJob(BaseJob):
    """
    Implements a simple job, which is executed on demand
    """

    def __init__(
            self,
            check_group):
        super(SimpleJob, self).__init__()

    def _run(self):
        print("Running a job...")

    
        
        



