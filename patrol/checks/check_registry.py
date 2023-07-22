import logging
import os
import json
import copy

from patrol import checks
from patrol.conf import conf
from patrol.data_model import (session, DQCheck)
from patrol import class_lib

log = logging.getLogger(__name__)

CHECKS_DIR = conf.get('core', 'CHECKS_FOLDER')
CONNECTIONS_DIR = conf.get('core', 'CONNECTIONS_FOLDER')
PROJECT_TREE_FILE = os.path.join(CHECKS_DIR, 'dq_checks.json')
INHERITED_PARAMS = ['schedule_interval', 'expiry_period', 'rows_to_persist', 'recipient_list']
REQUIRED_PARAMS = ['name', 'description']
#connection_map = {'my_conn_1': class_lib.Connection('my_conn_1', 'SqlAlchemy', 'postgresql://patuser:Amego475@ptdb:5432/consumerdb')} #TODO: Fix this
#connection_map = {'my_conn_1': class_lib.Connection('my_conn_1', 'Sqlite', 'consumerdb.db')} 


class CheckRegistry(object):
    """
    CheckRegistry contains information about all the DQ checks in the system
    """

    def __init__(self):
        self.checks = {}
        self.discover_checks()

    def add_check(self, check):
        # TODO: This function is created for fast prototyping/tests and should be
        #  replaced with a proper implementation in future
        db_chk = session.query(DQCheck).filter_by(check_id=check.check_id).first()
        check.next_run = db_chk.next_run if db_chk else None
        self.checks[check.check_id] = check
        session.merge(DQCheck(check))
        log.debug(f'==================== check {check.check_id} is added')

        session.commit()

    def import_params(self, dic_a, dic_b):
        """
        updates dic_a with values from dic_b for keys
        if value is a list then value in dic_a is extended
        else it is replaced
        """
        for k in REQUIRED_PARAMS:
            dic_a[k] = dic_b[k]

        for k in INHERITED_PARAMS:
            if k in dic_b:
                if isinstance(dic_b[k], list) and (k in dic_a):
                    dic_a[k].extend(dic_b[k])
                else:
                    dic_a[k] = dic_b[k]

    def get_checks(self, tree, params={}, arr=[]):
        """
        Recursive method processing tree in the format of dq_checks.json

        tree - hierarchy of elements organized as nested arrays. Arrays are of
            2 types, items and checks. Checks are the leaf elements. Nested items
            represent logical grouping of checks. Every element of an array may
            have attributes, name, description, schedule_interval, espiry_period,
            rows_to_persist, recipient_list. All these attributes are considered 
            inherited from upper level if not specified.
        params - values of the attributes from the parent level.
        arr - output array of objects of SimpleCheck
        """
        # takes inherited parameters from upper level and replaces them if any by the current level 
        self.import_params(params, tree)
        log.debug(f' ---- {tree.get("name", "none")}, params = {params}')

        # register check elements
        if 'checks' in tree:
            for chk in tree['checks']:
                chk_params = copy.deepcopy(params)
                cfg_file = open(os.path.join(CHECKS_DIR, chk))
                cfg_check = json.load(cfg_file)
                self.import_params(chk_params, cfg_check, INHERITED_PARAMS)

                log.debug(f'check_id = {cfg_check["check_id"]}, chk_params = {chk_params}')
                simpleCheck = checks.SimpleCheck(check_id=cfg_check['check_id'],
                                                 name=cfg_check['name'],
                                                 description=cfg_check['description'],
                                                 schedule_interval=chk_params['schedule_interval'],
                                                 notification={'expiry_period': chk_params['expiry_period'],
                                                               'rows_to_persist': chk_params['rows_to_persist'],
                                                               'recipient_list': chk_params['recipient_list']
                                                               },
                                                 project_name=chk_params['name'],
                                                 project_description=chk_params['description']
                                                 )
                for step in cfg_check['steps']:
                    log.debug(f'step is {step["step_type"]}')
                    simpleCheck.add_step(checks.SimpleCheckStep(step_seq=step['step_seq'],
                                                                step_type=step['step_type'],
                                                                query=step['query'],
                                                                connection=connection_map[step['connection']]))
                arr.append(simpleCheck)
                cfg_file.close()

        # Recursive processing
        if 'items' in tree:
            for item in tree['items']:
                self.get_checks(item, params, arr)
        return arr

    @property
    def get_connection_map(self):
        return self.connection_map or self.get_connection_map_from_json()

    def get_connection_map_from_json(self):
        with open(os.path.join(CONNECTIONS_DIR, 'connections.json')) as f:
            map = json.load(f)
            conn_map={}
            for conn in map:
                conn_map[conn] = class_lib.Connection(conn_name=map[conn]['conn_name'],
                                                    connector_name=map[conn]['connector_name'],
                                                    conn_string=map[conn]['conn_string'],
                                                    login=map[conn]['login'],
                                                    pwd=map[conn]['pwd'],
                                                    other_params=map[conn]['other_params'])

        return conn_map

    def discover_checks(self):
        log.debug('++++++++++++++++ discover_checks started')
        with open(PROJECT_TREE_FILE) as f:
            check_tree = json.load(f)
            check_list = self.get_checks(check_tree)
            for ch in check_list:
                self.add_check(ch)
        log.debug('++++++++++++++++ discover_checks finished')

    def _backup_project_tree_file(self):
        bkp_fname = os.path.join(CHECKS_DIR, 'backup', f"dq_checks{datetime.utcnow().strftime('%y%m%d%H%M%S')}.json")
        os.popen(f'cp {PROJECT_TREE_FILE} {bkp_fname}')

    def _validate_project_tree(project_tree):
        return project_tree is not None

    def _validate_check_file(check_file_name, check_conf):
        return True

    def _validate_query_file(query_file_name, query):
        return True

    def _delete_file(file_name):
        file = os.path.join(CHECKS_DIR, file_name)
        if os.path.isfile(file):
            os.remove(file)

    def get_project_tree():
        if os.path.isfile(PROJECT_TREE_FILE):
            with open(PROJECT_TREE_FILE) as f:
                project_tree = json.load(f)
        else:
            project_tree = {'error': 'File not found'}
        return project_tree
    
    def create_project_tree(project_tree):
        update_project_tree(project_tree)

    def update_project_tree(project_tree):
        if _validate_project_tree(project_tree):
            if os.path.isfile(PROJECT_TREE_FILE):
                _backup_project_tree_file()
            json_object = json.dumps(project_tree, indent=4)
            with open(PROJECT_TREE_FILE) as f:
                f.write(json_object)
    
    def delete_project_tree():
        if os.path.isfile(PROJECT_TREE_FILE):
            _backup_project_tree_file()
            os.remove(PROJECT_TREE_FILE)

    def get_check_file(check_file_name):
        fname = os.path.join(CHECKS_DIR, check_file_name)
        if os.path.isfile(fname):
            with open(fname) as f:
                check_file = json.load(f)
        else:
            check_file = {'error': 'File not found'}
        return check_file

    def create_check_file(check_file_name, check_conf):
        update_check_file(check_file_name, check_conf)

    def update_check_file(check_file_name, check_conf):
        if _validate_check_file(check_file_name, check_conf):
            json_object = json.dumps(check_conf, indent=4)
            with open(os.path.join(CHECKS_DIR, check_file_name)) as f:
                f.write(json_object)

    def delete_check_file(check_file_name):
        _delete_file(check_file_name)

    def get_query_file(query_file_name):
        fname = os.path.join(CHECKS_DIR, query_file_name)
        if os.path.isfile(fname):
            with open(fname) as f:
                query = f.read()
        else:
            query = 'File not found'
        return query

    def create_query_file(query_file_name, query):
        update_query_file(query_file_name, query)

    def update_query_file(query_file_name, query):
        if _validate_query_file(query_file_name, query):
            with open(os.path.join(CHECKS_DIR, query_file_name)) as f:
                f.write(query)

    def delete_query_file(query_file_name):
        _delete_file(query_file_name)


    def add_modify_item(parent_item_names, name, description, schedule_interval, expiry_period, rows_to_persist, recipient_list):
        if parent_item_names:
            pass
            
