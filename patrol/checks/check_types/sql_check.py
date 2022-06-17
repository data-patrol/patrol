from patrol.checks.check_types.base_check import BaseCheck

class SqlCheck(BaseCheck):
    """
    Implements a SQL DQ check
    """
    def __init__(
            self,
            check_id
            ):
        super(SqlCheck, self).__init__(check_id)
        

        
