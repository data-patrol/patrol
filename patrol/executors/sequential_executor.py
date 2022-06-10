import logging

from patrol.executors.base_executor import BaseExecutor

class SequentialExecutor(BaseExecutor):
    def test(self):
        return "OK"
