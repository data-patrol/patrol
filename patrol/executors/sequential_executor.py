from patrol.executors.base_executor import BaseExecutor

class SequentialExecutor(BaseExecutor):
    def __init__(self):
        super(SequentialExecutor, self).__init__()

    def execute_sync(self):
        for key in self.queued_checks:
            print("Executing check: ", str(key))

