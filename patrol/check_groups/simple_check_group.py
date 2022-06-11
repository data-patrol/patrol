from patrol.check_groups.base_check_group import BaseCheckGroup
from patrol.checks.base_check import BaseCheck

class SimpleCheckGroup(BaseCheckGroup):
    """
    SimpleCheckGroup is a simple container for grouping DQ checks together
    """

    def __init__(
            self,
            group_id,
            group_name):
        super(SimpleCheckGroup, self).__init__(group_id, group_name)
        



