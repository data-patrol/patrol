from patrol.checks.check_types.base_check import BaseCheck


class SimpleCheck(BaseCheck):
    """
    Implements a SQL DQ check
    """
    def __init__(
        self,
        check_id,
        name,
        description=None,
        schedule_interval=None,
        notification=None,
        project_name=None,
        project_description=None):
        """
            check_id -- check identifier,
            name -- check name,
            description -- text describing the check used in notification,
            schedule_interval -- cron expression specify recurrent runs,
            notification -- dictionary with keys:
                expiry_period - in format [digit] [unit measure], e.g. 2 day, 5 hour, etc
                rows to persist - number of rows of output used to send in notification
                recipient_list - list of dictionaries with keys:
                    to - coma separated list of emails
                    min_severity - specifies severity range for which recipient is used 
                    max_severity - specifies severity range for which recipient is used 
        """
        self.steps = {}
        super(SimpleCheck, self).__init__(check_id,name,description,schedule_interval)
        self.notification = notification
        self.project_name = project_name
        self.project_description = project_description

    def __repr__(self):
            return f"""<SimpleCheck(check_id='{self.check_id}',
                name : '{self.name}', 
                schedule_interval : '{self.schedule_interval}', 
                notification : {self.notification})>"""

    def add_step(self, step):
        self.steps[step.step_seq] = step
        step.check_id = self.check_id

        