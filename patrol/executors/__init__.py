from patrol.conf import conf

_EXECUTOR = conf.get('core', 'EXECUTOR')

if _EXECUTOR == 'ParallelExecutor':
    from patrol.executors.parallel_executor import ParallelExecutor
    DEFAULT_EXECUTOR = ParallelExecutor()

elif _EXECUTOR == 'SequentialExecutor':
    from patrol.executors.sequential_executor import SequentialExecutor
    DEFAULT_EXECUTOR = SequentialExecutor()
    
else:
    raise Exception(f"Executor {_EXECUTOR} not supported.")


def get_default_executor():
    return DEFAULT_EXECUTOR
