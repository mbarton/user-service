import sqlite3

class DB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file)

    def execute_block(self, sql_block):
        self.db.cursor().executescript(sql_block)
        self.db.commit()

    def close(self):
        self.db.close()