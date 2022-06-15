import sqlite3
import textwrap
class CheckInstance(object):
    """
    CheckRegistry implements an instance of a (running) check
    """
    
    def __init__(self, check):
        self.check = check

    def run(self):
        check = self.check

        # TODO: Just drafting the very first prototype

        print("---------------------------------------------------------------------------")
        print("Running check: ", check.check_id)
        conn = sqlite3.connect("consumerdb.db")

        with conn:
            cursor = conn.cursor()

            sql = textwrap.dedent(check.check_sql)
            print("Running the following SQL query: ", sql)
            cursor.execute(check.check_sql)

            
            print("Check results are the following: ")
            names = list(map(lambda x: x[0], cursor.description))
            print(names)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
