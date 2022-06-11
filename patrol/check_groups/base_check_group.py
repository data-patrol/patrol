from patrol.checks.base_check import BaseCheck

class BaseCheckGroup(object):
    """
    Base CheckGroup class that should be inherited by all types of DQ check group classes
    """

    def __init__(
            self,
            group_id,
            group_name):
        self.group_id = group_id
        self.group_name = group_name
        self.checks = {}

    def add_check(self, check):
        self.checks[check.check_id] = check