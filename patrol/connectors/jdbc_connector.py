import pandas

from patrol.connectors.base_connector import BaseConnector 

class JdbcConnector(BaseConnector):
    """
    JDBC connector
    """

    def __init__(self):
        pass

    def get_pandas_df(self, query, conn):
        pass
        
