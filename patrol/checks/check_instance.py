import logging
import textwrap
import pandas as pd

from patrol import checks
from patrol.connectors.connector_factory import ConnectorFactory


log = logging.getLogger(__name__)

class CheckInstance(object):
    """
    CheckRegistry implements an instance of a (running) check
    """

    def __init__(self, check):
        self.check = check

    def run(self):
        check = self.check

        # TODO: Just drafting the very first prototype
        # Code below needs to be rewritten
        
        log.info("===>")
        log.info("Running check: %s", check.check_id)

        connector_name = check.connection.connector_name
        log.info("Attempting to plug in the following connector: %s", connector_name)
        connector = ConnectorFactory().get_connector(connector_name)
        
        query = textwrap.dedent(check.check_sql)
        log.info("The following query will be executed: %s", query)
        df = connector.get_pandas_df(check.check_sql, check.connection)

        log.info("Check result is the following (first 10 rows): \n %s", 
                df.head(10).to_string(index=False))
