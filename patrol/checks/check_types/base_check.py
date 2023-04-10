class BaseCheck(object):
    """
    Base Check class that should be inherited by all types of DQ check classes
    """
    def __init__(self, check_id, name, description=None, schedule_interval=None):
        self.check_id = check_id
        self.schedule_interval = schedule_interval
        self.name = name
        self.description = description
