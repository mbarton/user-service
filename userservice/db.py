import sqlite3

class EntryAlreadyExists(Exception):
    pass

class DB:
    def __init__(self, db_file, bcrypt):
        self.db = sqlite3.connect(db_file)
        self.bcrypt = bcrypt

    def read_all(self, sql, args):
        cursor = self.db.cursor()
        cursor.execute(sql, args)
        return cursor.fetchall()

    def write(self, sql, args):
        try:
            cursor = self.db.cursor()
            
            cursor.execute(sql, args)
            ret = cursor.fetchall()
            
            self.db.commit()
            return ret
        except sqlite3.IntegrityError:
            raise EntryAlreadyExists

    # Seperate method to signal intention and allow for different exception handling
    # if required
    def execute(self, sql, args):
        return self.write(sql, args)

    def unsafe_execute_block(self, sql_block):
        self.db.cursor().executescript(sql_block)
        self.db.commit()

    def secure_hash(self, data):
        return self.bcrypt.generate_password_hash(data)

    def secure_hash_verify(self, data, expected):
        return self.bcrypt.check_password_hash(data, expected)

    def close(self):
        self.db.close()