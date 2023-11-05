import logging

from flask import Blueprint, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import (create_engine, text)

from patrol.conf import conf
from patrol.data_model import DQCheckRun
import checks.check_registry

# PATROL_CONN = conf.get('core', 'patrol_conn')

# engine = create_engine(PATROL_CONN, echo=False)
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# session = Session()

Base = declarative_base()
# ID_LEN = 250

log = logging.getLogger(__name__)

check_registry_endpoints_bp = Blueprint('check_registry', __name__)


@check_registry_endpoints_bp.route('/project_tree', methods=['GET'])
def get_project_tree():
    project_tree = CheckRegistry.get_project_tree()
    return project_tree

@check_registry_endpoints_bp.route('/check_file', methods=['GET'])
def get_check_file(check_file_name):
    check_file = CheckRegistry.get_check_file(check_file_name)
    return check_file

@check_registry_endpoints_bp.route('/query_file', methods=['GET'])
def get_query_file(query_file_name):
    query_file = CheckRegistry.get_query_file(query_file_name)
    return jsonify(query_file)

