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
        return connect(conn.connection_string)
    
    def get_pandas_df(self, query, conn):
        my_conn = connect(conn.connection_string)
        
        with my_conn:
            df = pd.read_sql(query, my_conn)
            
        return df