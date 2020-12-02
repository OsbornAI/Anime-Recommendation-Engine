import sqlite3

class Controller:
    def __init__(self, sql_db_dir):
        self.sql_db_dir = sql_db_dir
        self.conn = sqlite3.connect(sql_db_dir)
        self.cursor = self.conn.cursor()
        
    def __call__(self, query, query_dict=False):
        if not query_dict:
            self.cursor.execute(query, query_dict)
        else:
            self.cursor.execute(query)

        self.conn.commit()

        return self.cursor.fetchall()

    # There should be custom functions here which will handle our data later on for us

    def close(self):
        self.conn.close()