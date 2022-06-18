import os
import sys
import logging
import uuid
import traceback
import textwrap
import hashlib
from time import strftime
from importlib.machinery import SourceFileLoader
import pandas as pd

from patrol import checks
from patrol.connectors.connector_factory import ConnectorFactory
from patrol.conf import conf

log = logging.getLogger(__name__)

class CheckInstance(object):
    """
    CheckRegistry implements an instance of a (running) check
    """

    def __init__(self, check):
        self.check = check
        self.guid = uuid.uuid4()

    def run(self):
        check = self.check

        # TODO: Just drafting the very first prototype
        # Code below needs to be rewritten
        
        log.info("===>")
        log.info("Running check: %s", check.check_id)
        
        # Executing check steps
        for step_id, step in check.steps.items():
            log.info("===>")
            log.info("Running step: %s [%s]", step_id, step.step_type)        
            log.info("===>")

            connector_name = step.connection.connector_name
            log.info("Attempting to plug in the following connector: %s", connector_name)
            connector = ConnectorFactory().get_connector(connector_name)

            if step.step_type == checks.StepType.QUERY: 
                query = textwrap.dedent(step.query)
                log.info("The following query will be executed: %s", query)
                
                try:
                    df = connector.get_pandas_df(step.query, step.connection)
                except:
                    log.error("Failed to execute SQL step:")
                    log.error(traceback.print_exc())
                    return

            elif step.step_type == checks.StepType.PYTHON: 
                checks_dir = conf.get('core', 'CHECKS_FOLDER')
                filepath = checks_dir + '/' + step.query

                if not filepath.endswith(".py"):
                    raise ValueError('Python step file extension should be .py')

                try:
                    mod_name, _ = os.path.splitext(os.path.split(filepath)[-1])
                    path_hash = hashlib.sha1(filepath.encode('utf-8')).hexdigest()
                    mod_name = f'user_checks_{mod_name}_{path_hash}'
                    
                    if mod_name in sys.modules:
                        del sys.modules[mod_name]
    
                    mod = SourceFileLoader(mod_name, filepath).load_module()
                except:
                    log.error("Failed to load module: " + filepath)
                    log.error(traceback.print_exc())
                    return

                try:
                    df = mod.execute_step(connector.get_conn(step.connection))
                except:
                    log.error("Failed to execute Python step: %s", filepath)
                    log.error(traceback.print_exc())
                    return

            log.info("Step result is the following (first 10 rows): \n %s", 
            df.head(10).to_string(index=False))

            # Save detailed report to CSV file
            report_dir = f'{ conf.get('core', 'REPORTS_FOLDER') }/{ strftime('%Y-%m-%d') }'
            report_file = f'/{ check.check_id }__{ step.step_id }__{ strftime('%H%M%S') }__{ self.guid }.csv'
            report_file = report_dir + report_file

            if not os.path.exists(report_dir):
                os.makedirs(report_dir)
            
            log.info("Saving detailed report to file: %s", report_file)
            df.to_csv(report_file, sep = '\t', index=False)
