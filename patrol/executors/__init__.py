import logging

from patrol.conf import conf

_EXECUTOR = conf.get('core', 'EXECUTOR')

if _EXECUTOR == 'LocalExecutor':
    DEFAULT_EXECUTOR = LocalExecutor()
elif _EXECUTOR == 'CeleryExecutor':
    DEFAULT_EXECUTOR = CeleryExecutor()
elif _EXECUTOR == 'SequentialExecutor':
    from patrol.executors.sequential_executor import SequentialExecutor
    DEFAULT_EXECUTOR = SequentialExecutor()
else:
    raise Exception("Executor {0} not supported.".format(_EXECUTOR))

logging.info("Using executor " + _EXECUTOR)

def get_default_executor():
    return DEFAULT_EXECUTOR
