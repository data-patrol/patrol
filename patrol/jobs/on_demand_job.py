from patrol.jobs.base_job import BaseJob


class OnDemandJob(BaseJob):
    """
    Implements an on-demand job that can be executed either manually or automatically by trigger (such as API)
    """

    def __init__(self):
        super(OnDemandJob, self).__init__()

    def add_check_to_job(self, check):
        command = "python3 patrol run " + check.check_id
        self.executor.add_command_to_queue(check.check_id, command)

    def _run(self):
        self.executor.start()
        self.executor.execute_sync()
