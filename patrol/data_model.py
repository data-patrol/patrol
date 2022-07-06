import logging

from sqlalchemy import (
        Column, Integer, String, DateTime, Text, Boolean, ForeignKey)
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from patrol.conf import conf



PATROL_CONN = conf.get('core', 'patrol_conn')

engine = create_engine(PATROL_CONN, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()
ID_LEN = 250

log = logging.getLogger(__name__)


class DQ_Check(Base):
        __tablename__ = 'dq_check'

        check_id = Column('check_id', String(ID_LEN), primary_key = True)
        schedule_interval = Column('schedule_interval', String(16))
        name = Column('name', String(256))
        description = Column('description', String(8192))
        next_run = Column('next_run', DateTime)

        def __init__(self, check):
             Base.__init__(self
                        , check_id = check.check_id
                        , schedule_interval = check.schedule_interval
                        , name = check.name
                        , description = check.description)   

        def __repr__(self):
                return f"<QD_Check(check_id='{self.check_id}', name='{self.name}', schedule_interval='{self.schedule_interval}' )>"
    
class DQ_Check_Run(Base):
        __tablename__ = 'dq_check_run'

        guid = Column('guid', String(ID_LEN), primary_key = True)
        check_id = Column('check_id', String(ID_LEN), primary_key = True)
        step_id = Column('step_id', String(ID_LEN), primary_key = True)
        start_time = Column('start_time', DateTime)
        end_time = Column('end_time', DateTime)
        status = Column('status', String(16))
        severity = Column('severity', Integer)
        err_code = Column('err_code', String(16))
        err_description = Column('err_description', String(1024))

        def __init__(self, check_step):
             Base.__init__(self
                        , guid = check_step.guid
                        , check_id = check_step.check_id
                        , step_id = check_step.step_id
                        , status = 'INITIAL')   

        def __repr__(self):
                return f"<QD_Check_Run(check_id='{self.check_id}', step_id='{self.step_id}', start_time='{self.start_time}', status='{self.status}' )>"

def initdb(args): #TODO

        # dq_check = DQ_Check()
        # dq_check_run = DQ_Check_Run()
        # log.info(DQ_Check.__table__)

        Base.metadata.create_all(engine)
