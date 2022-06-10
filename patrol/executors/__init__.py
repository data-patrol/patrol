import logging

from patrol.conf import conf
from patrol.executors.sequential_executor import SequentialExecutor

_EXECUTOR = conf.get('core', 'EXECUTOR')

if _EXECUTOR == 'LocalExecutor':
    DEFAULT_EXECUTOR = LocalExecutor()
elif _EXECUTOR == 'CeleryExecutor':
    DEFAULT_EXECUTOR = CeleryExecutor()
elif _EXECUTOR == 'SequentialExecutor':
    DEFAULT_EXECUTOR = SequentialExecutor()
else:
    raise Exception("Executor {0} not supported.".format(_EXECUTOR))

logging.info("Using executor " + _EXECUTOR)