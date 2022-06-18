from patrol.checks.check_types.simple_check_step import SimpleCheckStep
class BaseCheck(object):
    """
    Base Check class that should be inherited by all types of DQ check classes
    """
    def __init__(self,check_id):
        self.check_id = check_id

    
