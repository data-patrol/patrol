import logging
import os
import sys

from patrol import checks
from patrol.conf import conf
from patrol.data_model import (session, DQ_Check, DQ_Check_Run)

log = logging.getLogger(__name__)

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
        session.merge(DQ_Check(check))
        log.debug(f'==================== check {check.check_id} is added')
        
        session.commit()

    def discover_checks(self):
        checks_dir = conf.get('core', 'CHECKS_FOLDER')
        for root, dirs, files in os.walk(checks_dir):
            for file in files:
                pass  #TODO

        

                    
