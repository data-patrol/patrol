import logging
import json

from sqlalchemy import (
        Column, Integer, String, DateTime, Text, Boolean, ForeignKey)
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (create_engine, text)

from patrol.conf import conf
from patrol import checks




PATROL_CONN = conf.get('core', 'patrol_conn')

engine = create_engine(PATROL_CONN, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()
ID_LEN = 250

log = logging.getLogger(__name__)


class ProcessLog(Base):
        __tablename__ = 'process_log'

        command = Column('command', String(32), primary_key = True)
        args = Column('args', String(128))
        start_time = Column('start_time', DateTime, primary_key = True)
        stop_time = Column('stop_time', DateTime)

        def __init__(self, command, args=None, start_time=None, stop_time=None):
             Base.__init__(self
                        , command = command
                        , args = args
                        , start_time = start_time
                        , stop_time = stop_time
                        )   

        def __repr__(self):
                return f"<ProcessLog(command='{self.command}', start_time='{self.start_time}', stop_time='{self.stop_time}' )>"
    
class DQCheck(Base):
        __tablename__ = 'dq_check'

        check_id = Column('check_id', String(ID_LEN), primary_key = True)
        schedule_interval = Column('schedule_interval', String(16))
        name = Column('name', String(256))
        description = Column('description', String(8192))
        expiry_period = Column('expiry_period', String(16))
        persist_rows = Column('persist_rows', Integer())
        recipient_list = Column('recipient_list', String(1024))
        project_name = Column('project_name', String(256))
        project_description = Column('project_description', String(8192))
        next_run = Column('next_run', DateTime)

        def __init__(self, check):
             Base.__init__(self
                        , check_id = check.check_id
                        , schedule_interval = check.schedule_interval
                        , name = check.name
                        , description = check.description
                        , expiry_period = check.notification['expiry_period'] if check.notification else None
                        , persist_rows = check.notification['rows to persist'] if check.notification else None
                        , recipient_list = json.dumps(check.notification['recipient_list'] if check.notification else [])
                        , project_name = check.project_name
                        , project_description = check.project_description
                        , next_run = check.next_run
                        )   

        def __repr__(self):
                return f"<DQ_Check(check_id='{self.check_id}', name='{self.name}', schedule_interval='{self.schedule_interval}' )>"
    
class DQCheckRun(Base):
        __tablename__ = 'dq_check_run'

        guid = Column('guid', String(ID_LEN), primary_key = True)
        check_id = Column('check_id', String(ID_LEN), primary_key = True)
        step_seq = Column('step_seq', Integer, primary_key = True)
        schedule_time = Column('schedule_time', DateTime)
        start_time = Column('start_time', DateTime)
        end_time = Column('end_time', DateTime)
        status = Column('status', String(16))
        severity = Column('severity', Integer)
        report_file = Column('report_file', String(1024))
        err_code = Column('err_code', String(16))
        err_description = Column('err_description', String(1024))

        def __init__(self, check_step):
             Base.__init__(self
                        , guid = check_step.guid
                        , check_id = check_step.check_id
                        , step_seq = check_step.step_seq
                        , status = 'INITIAL')   

        def __repr__(self):
                return f"<DQ_Check_Run(check_id='{self.check_id}', step_seq='{self.step_seq}', start_time='{self.start_time}', status='{self.status}' )>"

def initdb(args): #TODO
        Base.metadata.create_all(engine)
        session.commit()
        log.info('Database created')

def getChecksToRun():
        qry = """\
                SELECT a.check_id, a.name, a.schedule_interval, strftime ('%Y-%m-%dT%H:%M', COALESCE(a.next_run, datetime('now'))) as next_run
        FROM dq_check a
        LEFT join dq_check_run b
        ON b.check_id = a.check_id
        AND b.schedule_time > a.next_run
        WHERE b.check_id IS NULL
        AND a.schedule_interval IS NOT NULL
        AND (a.next_run IS NULL OR a.next_run < datetime('now'))
        """
        with engine.connect() as conn:
                rows = conn.execute(qry)
                # next_ = [next_run for (check_id, name, schedule_interval, next_run) in rows]
                # print(next_[0], type(next_[0])) 
                result = [checks.SimpleCheck(check_id=check_id, name=name, schedule_interval=schedule_interval, next_run=next_run) for (check_id, name, schedule_interval, next_run) in rows]
        return result