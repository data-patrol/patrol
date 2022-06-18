import enum

class StepType(enum.Enum):
    QUERY = "query"
    PYTHON = "python"

class SimpleCheckStep():
    """
    Implements a model class for a check step. Each check may have multiple steps.
    Each step executes its own command (e.g. SQL query)
    """
    def __init__(
            self,
            step_id,
            step_type,
            query,
            connection
            ):
        self.step_id = step_id
        self.step_type = step_type
        self.query = query
        self.connection = connection
