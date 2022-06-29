import os
import sys
import logging
import uuid
import traceback
import textwrap
import hashlib
from time import strftime
import datetime as dt
from importlib.machinery import SourceFileLoader
import pandas as pd

from patrol import checks
from patrol.connectors.connector_factory import ConnectorFactory
from patrol.conf import conf
from patrol.data_model import (session, DQ_Check, DQ_Check_Run)

log = logging.getLogger(__name__)


class Step_Exception(Exception):
    # Exception_codes
    INVALID_FILENAME = 10001
    SQL_EXEC = 10011
    PYTHON_LOAD = 10021
    PYTHON_EXEC = 10031

    def __init__(self, message, code):
        super(Step_Exception, self).__init__(message)
        self.message = message
        self.code = code

class CheckInstance(object):
    """
    CheckRegistry implements an instance of a (running) check
    """

    def __init__(self, check):
        self.check = check
        self.guid = str(uuid.uuid4())
        log.debug(f'==================== check Instance {check.check_id} is added')
        for step in check.steps.values():
            step.guid = self.guid
            log.debug(f'guid = {step.guid}, check_id = {step.check_id}, step_id = {step.step_id}')
            session.add(DQ_Check_Run(step))
            log.debug(f'==================== step {check.check_id}.{step.step_id} is added')
        session.commit()

    def run(self):
        check = self.check

        # TODO: Just drafting the very first prototype
        # Code below needs to be rewritten
        
        log.info("===>")
        log.info("Running check: %s", check.check_id)
        
        try:
            # Executing check steps
            for step_id, step in check.steps.items():
                log.info("===>")
                log.info("Running step: %s [%s]", step_id, step.step_type)        
                log.info("===>")

                db_step = session.query(DQ_Check_Run).filter_by(guid=step.guid, step_id=step_id).first()
                db_step.start_time = dt.datetime.utcnow()
                db_step.status = 'IN PROGRESS'

                connector_name = step.connection.connector_name
                log.info("Attempting to plug in the following connector: %s", connector_name)
                connector = ConnectorFactory().get_connector(connector_name)

                if step.step_type == checks.StepType.QUERY: 
                    query = textwrap.dedent(step.query)
                    log.info("The following query will be executed: %s", query)
                    
                    try:
                        df = connector.get_pandas_df(step.query, step.connection)
                    except Exception as e:
                        log.error("Failed to execute SQL step:")
                        log.error(traceback.print_exc())
                        raise Step_Exception(message = str(e), code = Step_Exception.SQL_EXEC)

                elif step.step_type == checks.StepType.PYTHON: 
                    checks_dir = conf.get('core', 'CHECKS_FOLDER')
                    filepath = checks_dir + '/' + step.query

                    if not filepath.endswith(".py"):
                        raise Step_Exception(message = 'Python step file extension should be .py', code = Step_Exception.INVALID_FILENAME)

                    try:
                        mod_name, _ = os.path.splitext(os.path.split(filepath)[-1])
                        path_hash = hashlib.sha1(filepath.encode('utf-8')).hexdigest()
                        mod_name = f'user_checks_{mod_name}_{path_hash}'
                        
                        if mod_name in sys.modules:
                            del sys.modules[mod_name]
        
                        mod = SourceFileLoader(mod_name, filepath).load_module()
                    except Exception as e:
                        log.error("Failed to load module: " + filepath)
                        log.error(traceback.print_exc())
                        raise Step_Exception(message = str(e), code = Step_Exception.PYTHON_LOAD)

                    try:
                        df = mod.execute_step(connector.get_conn(step.connection))
                    except Exception as e:
                        log.error("Failed to execute Python step: %s", filepath)
                        log.error(traceback.print_exc())
                        raise Step_Exception(message = str(e), code = Step_Exception.PYTHON_EXEC)

                log.info("Step result is the following (first 10 rows): \n %s", 
                df.head(10).to_string(index=False))

                # Save detailed report to CSV file
                report_dir = '{}/{}'.format(conf.get('core', 'REPORTS_FOLDER'), strftime('%Y-%m-%d'))
                report_file = '/{}__{}__{}__{}.csv'.format(check.check_id, step.step_id, strftime('%H%M%S'), self.guid)
                report_file = report_dir + report_file

                if not os.path.exists(report_dir):
                    os.makedirs(report_dir)
                
                log.info("Saving detailed report to file: %s", report_file)
                df.to_csv(report_file, sep = '\t', index=False)

                db_step.status = 'COMPLETED'
                db_step.err_code = 0
                db_step.err_description = ''
                db_step.severity = int(df['severity'].loc[0]) if 'severity' in [c.lower() for c in list(df.columns)] else -10
                db_step.end_time = dt.datetime.utcnow()
        except Step_Exception as ex:
            db_step.status = 'FAILED'
            db_step.err_code = ex.code
            db_step.err_description = ex.message
            db_step.severity = -1
            db_step.end_time = dt.datetime.utcnow()
        except Exception as e:
            db_step.status = 'FAILED'
            db_step.err_code = 999
            db_step.err_description = str(e)
            db_step.severity = -1
            db_step.end_time = dt.datetime.utcnow()

        session.commit()