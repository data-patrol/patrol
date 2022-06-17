import os
import logging
import uuid
from time import strftime
import textwrap
import pandas as pd

from patrol import checks
from patrol.connectors.connector_factory import ConnectorFactory
from patrol.conf import conf

log = logging.getLogger(__name__)

class CheckInstance(object):
    """
    CheckRegistry implements an instance of a (running) check
    """

    def __init__(self, check):
        self.check = check
        self.guid = uuid.uuid4()

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

        # Save report to Excel file
        report_dir = '{}/{}'.format(conf.get('core', 'REPORTS_FOLDER'), strftime('%Y-%m-%d'))
        report_file = '/{}__{}__{}.xlsx'.format(check.check_id, strftime('%H%M%S'), self.guid)
        report_file = report_dir + report_file

        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        
        log.info("Saving detailed report to Excel file: %s", report_file)

        # Configure proper column width in Excel depending on actual values
        writer = pd.ExcelWriter(report_file) 
        df.to_excel(writer, sheet_name='Report', index=False)  # may consider na_rep='NaN'

        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['Report'].set_column(col_idx, col_idx, column_length)
        writer.save()
