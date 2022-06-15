import logging
import sqlite3
import textwrap

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

        log.info("---------------------------------------------------------------------------")
        log.info("Running check: %s", check.check_id)
        conn = sqlite3.connect("consumerdb.db")

        with conn:
            cursor = conn.cursor()

            sql = textwrap.dedent(check.check_sql)
            log.info("Running the following SQL query: %s", sql)
            cursor.execute(check.check_sql)
            
            log.info("Check results are the following: ")
            names = list(map(lambda x: x[0], cursor.description))
            log.info(names)
            rows = cursor.fetchall()
            for row in rows:
                log.info(row)
