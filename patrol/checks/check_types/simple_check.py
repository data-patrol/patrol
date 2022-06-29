from patrol.checks.check_types.base_check import BaseCheck


class SimpleCheck(BaseCheck):
    """
    Implements a SQL DQ check
    """
    def __init__(self,check_id,name,description=None,schedule_interval=None):
        self.steps = {}
        super(SimpleCheck, self).__init__(check_id,name,description,schedule_interval)

    def add_step(self, step):
        self.steps[step.step_id] = step
        step.check_id = self.check_id

        