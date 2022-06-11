from patrol.checks.base_check import BaseCheck

class SqlCheck(BaseCheck):
    """
    Implements a SQL DQ check
    """
    def __init__(
            self,
            check_id,
            check_sql):
        super(SqlCheck, self).__init__(check_id, check_sql)
        
