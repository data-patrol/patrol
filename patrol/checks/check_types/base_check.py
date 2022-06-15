from patrol import executors

class BaseCheck(object):
    """
    Base Check class that should be inherited by all types of DQ check classes
    """
    def __init__(
            self,
            check_id,
            check_sql):
        self.check_id = check_id
        self.check_sql = check_sql
