from patrol.checks.check_types.base_check import BaseCheck

class BaseExecutor(object):
    """
    Base Executor class that should be inherited by all executor implementation classes
    """

    def __init__(self):
        self.queued_commands = {}

    def start(self):
        pass

    def add_command_to_queue(self, key, command):
        self.queued_commands[key] = command

    def execute_sync(self):
        raise NotImplementedError("This method needs to be overridden")

        