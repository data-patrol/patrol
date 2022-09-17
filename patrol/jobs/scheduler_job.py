import os
import logging

from patrol.jobs.base_job import BaseJob

log = logging.getLogger(__name__)

class SchedulerJob(BaseJob):
    """
    Implements a scheduler job
    """

    def __init__(
            self):
        super(SchedulerJob, self).__init__()

    def add_check_to_job(self, check):
        log.info(f'Adding check {check.check_id} for schedule_time {check.next_run}')
        command = f'python3 patrol run {check.check_id} {check.next_run}'
        self.executor.add_command_to_queue(check.check_id, command)    
    
    def _run(self):
        self.executor.start()
        self.executor.execute_sync()
    
        
        



