from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from patrol.conf import conf

PATROL_CONN = conf.get('core', 'patrol_conn')

engine = create_engine(PATROL_CONN)
Session = scoped_session(sessionmaker(autocommit=False,
        autoflush=False,
        bind=engine))
