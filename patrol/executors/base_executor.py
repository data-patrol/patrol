from patrol.checks.check_types.base_check import BaseCheck

class BaseExecutor(object):
    """
    Base Executor class that should be inherited by all executor implementation classes
    """

    def __init__(self):
        self.queued_checks = {}

    def start(self):
        pass

    def add_check_to_queue(self, check):
        self.queued_checks[check.check_id] = check

    def execute_sync(self):
        raise NotImplementedError("This method needs to be overridden")

        