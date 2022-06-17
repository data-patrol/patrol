class CheckStep():
    """
    Implements a model class for check step. Each check may have multiple steps.
    Each step executes its own command (e.g. SQL query)
    """
    def __init__(
            self,
            step_id,
            query,
            connection
            ):
        self.step_id = step_id
        self.query = query
        self.connection = connection
