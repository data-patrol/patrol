import logging
import subprocess

from patrol.checks.check_types.base_check import BaseCheck

log = logging.getLogger(__name__)

class BaseExecutor(object):
    """
    Base Executor class that should be inherited by all executor implementation classes
    """

    def __init__(self):
        self.queued_commands = {}

    def start(self):
        log.info(f'Starting executor: {self.__class__.__name__}')
        pass

    def add_command_to_queue(self, key, command):
        self.queued_commands[key] = command

    def run_shell_command(self, command):
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

    def execute_sync(self):
        raise NotImplementedError("This method needs to be overridden")

        