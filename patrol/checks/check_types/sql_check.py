from patrol.checks.check_types.base_check import BaseCheck

class SqlCheck(BaseCheck):
    """
    Implements a SQL DQ check
    """
    def __init__(
            self,
            check_id,
            check_sql,
            connection
            ):
        super(SqlCheck, self).__init__(check_id, check_sql, connection)

        
