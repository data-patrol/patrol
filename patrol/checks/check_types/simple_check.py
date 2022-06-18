from patrol.checks.check_types.base_check import BaseCheck

class SimpleCheck(BaseCheck):
    """
    Implements a SQL DQ check
    """
    def __init__(
            self,
            check_id
            ):
        self.steps = {}
        super(SimpleCheck, self).__init__(check_id)

    def add_step(self, step):
        self.steps[step.step_id] = step
        