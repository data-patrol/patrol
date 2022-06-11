from patrol import executors

class BaseJob(object):
    """
    Base CheckGroup class that should be inherited by all types of jobs
    """

    def __init__(
            self,
            executor=None):
        self.executor = executor or executors.get_default_executor()
        self.executor_class = self.executor.__class__.__name__

    def run(self):
        self._run()

    def _run(self):
        raise NotImplementedError("This method needs to be overridden")
