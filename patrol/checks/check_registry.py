import logging
import os
import sys
import json
import copy

from patrol import checks
from patrol.conf import conf
from patrol.data_model import (session, DQCheck, DQCheckRun)
from patrol.connectors.connector_factory import ConnectorFactory
from patrol import class_lib

log = logging.getLogger(__name__)

CHECKS_DIR = conf.get('core', 'CHECKS_FOLDER')
INHERITED_PARAMS = ['name', 'description', 'schedule_interval', 'expiry_period', 'rows to persist', 'recipient_list']
coonection_map = {'my_conn_1': class_lib.Connection(
                                                'my_conn_1', 
                                                'Sqlite',
                                                'consumerdb.db')}

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
        db_chk = session.query(DQCheck).filter_by(check_id=check.check_id).first()
        check.next_run = db_chk.next_run if db_chk else None
        self.checks[check.check_id] = check
        session.merge(DQCheck(check))
        log.debug(f'==================== check {check.check_id} is added')
        
        session.commit()

    def import_params(self, dic_a, dic_b, keys):
        """
        updates dic_a with values from dic_b for keys
        if value is a list then value in dic_a is extended
        else it is replaced
        """
        for k in keys:
            if k in dic_b:
                if isinstance(dic_b[k], list) and (k in dic_a):
                    dic_a[k].extend(dic_b[k])
                else:
                    dic_a[k] = dic_b[k]

    def get_checks(self, tree, params={}, arr=[]):
        # inherit parameters from upstream
        self.import_params(params, tree, INHERITED_PARAMS)
        log.debug(f' ---- {tree.get("name","none")}, params = {params}')
        
        # register check elements
        if 'checks' in tree:
            for chk in tree['checks']:
                chk_params = copy.deepcopy(params)
                cfg_file = open(os.path.join( CHECKS_DIR,chk))
                cfg_check = json.load(cfg_file)
                self.import_params(chk_params, cfg_check, INHERITED_PARAMS)

                log.debug(f'check_id = {cfg_check["check_id"]}, chk_params = {chk_params}')
                simpleCheck = checks.SimpleCheck(check_id=cfg_check['check_id'],
                                                name=cfg_check['name'],
                                                description=cfg_check['description'],
                                                schedule_interval=chk_params['schedule_interval'],
                                                notification = {'expiry_period': chk_params['expiry_period'],
                                                                'rows to persist': chk_params['rows to persist'],
                                                                'recipient_list': chk_params['recipient_list']
                                                                },
                                                project_name=chk_params['name'],
                                                project_description=chk_params['description']
                                                )
                for step in cfg_check['steps']:
                    log.debug(f'step is {step["step_type"]}')
                    simpleCheck.add_step(checks.SimpleCheckStep(step_seq = step['step_seq'],
                                                                step_type = step['step_type'],
                                                                query = step['query'],
                                                                connection = coonection_map[step['connection']]))
                arr.append(simpleCheck)
                cfg_file.close()
        
        # Recursive processing
        if 'items' in tree:
            for item in tree['items']:
                self.get_checks(item, params, arr)
        return arr

    def discover_checks(self):
        log.debug('++++++++++++++++ discover_checks started')
        with open(os.path.join( CHECKS_DIR,'dq_checks.json')) as f:
            check_tree = json.load(f)
            check_list = self.get_checks(check_tree)
            for ch in check_list:
                self.add_check(ch)
        log.debug('++++++++++++++++ discover_checks finished')

        

                    
