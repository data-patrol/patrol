import json
import pandas as pd
from sqlalchemy import create_engine

from patrol.connectors.base_connector import BaseConnector


class SqlAlchemyConnector(BaseConnector):
    """
    SqlAlchemy connector
    """

    def __init__(self):
        pass

    def get_conn(self, conn):
        return create_engine(conn.conn_string)

    def get_pandas_df(self, query, conn):
        engine = self.get_conn(conn)
        df = pd.read_sql_query(query, con=engine)

        return df

    def test_conn(self, conn):
        try:
            engine = self.get_conn(conn)
            query = "SELECT 'test'"
            df = pd.read_sql_query(query, con=engine)

        except Exception as e:
            return False, str(e)
        return True, ""
