import json
import pandas as pd
from databricks import sql

from patrol.connectors.base_connector import BaseConnector


class DatabricksConnector(BaseConnector):
    """
    Databricks connector
    """

    def __init__(self):
        pass

    def get_conn(self, conn):
        conn_params = json.loads(conn.other_params)
        return sql.connect(server_hostname=conn.conn_string,
                           http_path=conn_params['http_path'],
                           access_token=conn.pwd)

    def get_pandas_df(self, query, conn):
        conn_params = json.loads(conn.other_params)

        with sql.connect(server_hostname=conn.conn_string,
                         http_path=conn_params['http_path'],
                         access_token=conn.pwd) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                df = pd.DataFrame(cursor)
                df.columns = [x[0] for x in cursor.description]

        return df

    def test_conn(self, conn):
        try:
            conn_params = json.loads(conn.other_params)

            with sql.connect(server_hostname=conn.conn_string,
                             http_path=conn_params['http_path'],
                             access_token=conn.pwd) as connection:

                with connection.cursor() as cursor:
                    cursor.execute("SELECT 'test'")
        except Exception as e:
            return False, str(e)
        return True, ""
