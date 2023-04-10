import enum
import os

from patrol.conf import conf

CHECKS_DIR = conf.get('core', 'CHECKS_FOLDER')


class StepType(enum.Enum):
    QUERY = "QUERY"
    PYTHON = "PYTHON"


class SimpleCheckStep:
    """
    Implements a model class for a check step. Each check may have multiple steps.
    Each step executes its own command (e.g. SQL query)
    """

    def __init__(
            self,
            step_seq,
            step_type,
            query,
            connection,
            check_id=None
    ):
        self.step_seq = step_seq
        self.step_type = step_type
        if query and query[-4:].lower() == '.sql':
            with open(os.path.join(CHECKS_DIR, query)) as f:
                self.query = f.read()
        else:
            self.query = query
        self.connection = connection
        self.check_id = check_id
