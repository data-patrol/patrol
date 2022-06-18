import os
import sys

from patrol import checks
from patrol.conf import conf

class CheckRegistry(object):
    """
    CheckRegistry contains information about all the DQ checks in the system
    """
    
    def __init__(self):
        self.checks = {}
        self.discover_checks()

    def add_check(self, check):
        #TODO: This function is created for fast prototyping/tests and should be 
        # replaced with a proper implementation in future
        self.checks[check.check_id] = check

    def discover_checks(self):
        checks_dir = conf.get('core', 'CHECKS_FOLDER')
        for root, dirs, files in os.walk(checks_dir):
            for file in files:
                pass  #TODO

        

                    
