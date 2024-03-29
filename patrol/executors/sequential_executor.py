import logging
import subprocess

from patrol.executors.base_executor import BaseExecutor

log = logging.getLogger(__name__)


class SequentialExecutor(BaseExecutor):
    def __init__(self):
        super(SequentialExecutor, self).__init__()

    def execute_sync(self):
        for key, command in self.queued_commands.items():
            log.info("===>")
            log.info(f'Executor: Executing command: {command}')
            try:
                subprocess.Popen(command, shell=True).wait()
            except Exception as e:
                raise e
