import logging
import concurrent.futures

from patrol.executors.base_executor import BaseExecutor

log = logging.getLogger(__name__)

class ParallelExecutor(BaseExecutor):
    def __init__(self):
        super(ParallelExecutor, self).__init__()

    def execute_sync(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for key,command in self.queued_commands.items():
                log.info("===>")
                log.info(f'Executor: Executing command: {command}')
                executor.submit(self.run_shell_command, command)
