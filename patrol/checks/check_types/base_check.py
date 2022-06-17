from patrol.checks.check_types.check_step import CheckStep
class BaseCheck(object):
    """
    Base Check class that should be inherited by all types of DQ check classes
    """
    def __init__(self,check_id):
        self.steps = {}
        self.check_id = check_id

    def add_step(self, step):
        self.steps[step.step_id] = step
