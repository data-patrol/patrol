import logging

from flask import Blueprint, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (create_engine, text)

from patrol.conf import conf
from patrol.data_model import DQCheck

PATROL_CONN = conf.get('core', 'patrol_conn')

engine = create_engine(PATROL_CONN, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()
ID_LEN = 250

log = logging.getLogger(__name__)

dq_endpoints_bp = Blueprint('dq_check', __name__)


@dq_endpoints_bp.route('/dq_check', methods=['GET'])
def get_dq_checks():
    dq_checks = DQCheck.query.all()
    result = []
    for dq_check in dq_checks:
        result.append({
            'check_id': dq_check.check_id,
            'schedule_interval': dq_check.schedule_interval,
            'name': dq_check.name,
            'description': dq_check.description,
            'expiry_period': dq_check.expiry_period,
            'persist_rows': dq_check.persist_rows,
            'recipient_list': dq_check.recipient_list,
            'project_name': dq_check.project_name,
            'project_description': dq_check.project_description,
            'next_run': dq_check.next_run.isoformat() if dq_check.next_run else None
        })
    return jsonify(result)


@dq_endpoints_bp.route('/dq_check/<check_id>', methods=['GET'])
def get_dq_check(check_id):
    dq_check = DQCheck.query.get(check_id)
    if dq_check:
        result = {
            'check_id': dq_check.check_id,
            'schedule_interval': dq_check.schedule_interval,
            'name': dq_check.name,
            'description': dq_check.description,
            'expiry_period': dq_check.expiry_period,
            'persist_rows': dq_check.persist_rows,
            'recipient_list': dq_check.recipient_list,
            'project_name': dq_check.project_name,
            'project_description': dq_check.project_description,
            'next_run': dq_check.next_run.isoformat() if dq_check.next_run else None
        }
        return jsonify(result)
    else:
        return jsonify({'error': 'DQCheck not found'}), 404


@dq_endpoints_bp.route('/dq_check', methods=['POST'])
def create_dq_check():
    data = request.get_json()
    dq_check = DQCheck(
        check_id=data.get('check_id'),
        schedule_interval=data.get('schedule_interval'),
        name=data.get('name'),
        description=data.get('description'),
        expiry_period=data.get('expiry_period'),
        persist_rows=data.get('persist_rows'),
        recipient_list=data.get('recipient_list'),
        project_name=data.get('project_name'),
        project_description=data.get('project_description'),
        next_run=data.get('next_run')
    )
    db.session.add(dq_check)
    db.session.commit()
    return jsonify({'message': 'DQCheck created successfully'})


@dq_endpoints_bp.route('/dq_check/<check_id>', methods=['PUT'])
def update_dq_check(check_id):
    dq_check = DQCheck.query.get(check_id)
    if dq_check:
        data = request.get_json()
        dq_check.schedule_interval = data.get('schedule_interval')
        dq_check.name = data.get('name')
        dq_check.description = data.get('description')
        dq_check.expiry_period = data.get('expiry_period')
        dq_check.persist_rows = data.get('persist_rows')
        dq_check.recipient_list = data.get('recipient_list')
        dq_check.project_name = data.get('project_name')
        dq_check.project_description = data.get('project_description')
        dq_check.next_run = data.get('next_run')
        db.session.commit()
        return jsonify({'message': 'DQCheck updated successfully'})
    else:
        return jsonify({'error': 'DQCheck not found'}), 404


@dq_endpoints_bp.route('/dq_check/<check_id>', methods=['DELETE'])
def delete_dq_check(check_id):
    dq_check = DQCheck.query.get(check_id)
    if dq_check:
        db.session.delete(dq_check)
        db.session.commit()
        return jsonify({'message': 'DQCheck deleted successfully'})
    else:
        return jsonify({'error': 'DQCheck not found'}), 404
