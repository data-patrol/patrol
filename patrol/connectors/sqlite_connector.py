import pandas as pd
from sqlite3 import connect

from patrol.connectors.base_connector import BaseConnector


class SqliteConnector(BaseConnector):
    """
    Connector for SQLite
    """

    def __init__(self):
        pass

    def get_conn(self, conn):
        return connect(conn.conn_string)

    def get_pandas_df(self, query, conn):
        my_conn = connect(conn.conn_string)

        with my_conn:
            df = pd.read_sql(query, my_conn)

        return df

    def test_conn(self, conn):
        try:
            my_conn = connect(conn.conn_string)
            cur = my_conn.cursor()
            cur.execute("SELECT 'test'")
        except Exception as e:
            return False, str(e)
        return True, ""
