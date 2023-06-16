import logging

from flask import Blueprint, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (create_engine, text)

from patrol.conf import conf
from patrol.data_model import ProcessLog

PATROL_CONN = conf.get('core', 'patrol_conn')

engine = create_engine(PATROL_CONN, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()
ID_LEN = 250

log = logging.getLogger(__name__)

process_log_endpoints_bp = Blueprint('process_log', __name__)


@process_log_endpoints_bp.route('/process_log', methods=['GET'])
def get_dq_check_runs():
    process_logs = ProcessLog.query.all()
    result = []
    for process_log in process_logs:
        result.append({
            'command': process_log.command,
            'args': process_log.args,
            'start_time': process_log.start_time,
            'stop_time': process_log.stop_time
        })
    return jsonify(result)


@process_log_endpoints_bp.route('/dq_check_run/<check_id>', methods=['GET'])
def get_dq_check(check_id):
    process_log = ProcessLog.query.get(check_id)
    if process_log:
        result = {
            'command': process_log.command,
            'args': process_log.args,
            'start_time': process_log.start_time,
            'stop_time': process_log.stop_time
        }
        return jsonify(result)
    else:
        return jsonify({'error': 'DQCheck not found'}), 404
