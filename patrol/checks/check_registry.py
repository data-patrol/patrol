from patrol import checks

class CheckRegistry(object):
    """
    CheckRegistry contains information about all the DQ checks in the system
    """
    
    def __init__(
            self):
            self.checks = {}

    def add_check(self, check):
        #TODO: This function is created for fast prototyping/tests and should be 
        # replaced with a proper implementation in future
        self.checks[check.check_id] = check