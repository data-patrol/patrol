import logging

from flask import Blueprint, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (create_engine, text)

from patrol.conf import conf
from patrol.data_model import DQCheckRun

PATROL_CONN = conf.get('core', 'patrol_conn')

engine = create_engine(PATROL_CONN, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()
ID_LEN = 250

log = logging.getLogger(__name__)

dq_run_endpoints_bp = Blueprint('dq_check_run', __name__)


@dq_run_endpoints_bp.route('/dq_check_run', methods=['GET'])
def get_dq_check_runs():
    dq_check_runs = DQCheckRun.query.all()
    result = []
    for dq_check_run in dq_check_runs:
        result.append({
            'guid': dq_check_run.guid,
            'check_id': dq_check_run.check_id,
            'step_seq': dq_check_run.step_seq,
            'schedule_time': dq_check_run.schedule_time,
            'start_time': dq_check_run.start_time,
            'end_time': dq_check_run.end_time,
            'status': dq_check_run.status,
            'severity': dq_check_run.severity,
            'report_file': dq_check_run.report_file,
            'err_code': dq_check_run.err_code,
            'err_description': dq_check_run.err_description
        })
    return jsonify(result)


@dq_run_endpoints_bp.route('/dq_check_run/<check_id>', methods=['GET'])
def get_dq_check(check_id):
    dq_check_run = DQCheckRun.query.get(check_id)
    if dq_check_run:
        result = {
            'guid': dq_check_run.guid,
            'check_id': dq_check_run.check_id,
            'step_seq': dq_check_run.step_seq,
            'schedule_time': dq_check_run.schedule_time,
            'start_time': dq_check_run.start_time,
            'end_time': dq_check_run.end_time,
            'status': dq_check_run.status,
            'severity': dq_check_run.severity,
            'report_file': dq_check_run.report_file,
            'err_code': dq_check_run.err_code,
            'err_description': dq_check_run.err_description
        }
        return jsonify(result)
    else:
        return jsonify({'error': 'DQCheck not found'}), 404


@dq_run_endpoints_bp.route('/dq_check_run/<check_id>', methods=['PUT'])
def update_dq_check(check_id):
    dq_check_run = DQCheckRun.query.get(check_id)
    if dq_check_run:
        data = request.get_json()
        dq_check_run.guid = data.get('guid')
        dq_check_run.check_id = data.get('check_id')
        dq_check_run.step_seq = data.get('step_seq')
        dq_check_run.schedule_time = data.get('schedule_time')
        dq_check_run.start_time = data.get('start_time')
        dq_check_run.end_time = data.get('end_time')
        dq_check_run.status = data.get('status')
        dq_check_run.severity = data.get('severity')
        dq_check_run.report_file = data.get('report_file')
        dq_check_run.err_code = data.get('err_code')
        dq_check_run.err_description = data.get('err_description')

        db.session.commit()
        return jsonify({'message': 'DQCheckRun updated successfully'})
    else:
        return jsonify({'error': 'DQCheckRun not found'}), 404


@dq_run_endpoints_bp.route('/dq_check_run/<check_id>', methods=['DELETE'])
def delete_dq_check(check_id):
    dq_check_run = DQCheckRun.query.get(check_id)
    if dq_check_run:
        db.session.delete(dq_check_run)
        db.session.commit()
        return jsonify({'message': 'DQCheckRun deleted successfully'})
    else:
        return jsonify({'error': 'DQCheckRun not found'}), 404
