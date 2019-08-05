import sqlite3, contextlib
from urllib.request import pathname2url

import os

class SpeckleCache():

    initialized = False

    def __init__(self, filepath=None):
        if filepath is None:
            self.db_path = os.path.join(os.getenv('LOCALAPPDATA'), os.path.join('SpeckleSettings', 'SpeckleCache.db'))
        else:
            self.db_path = filepath

        self.log(self.db_path)

        self.db_uri = 'file:{}?mode=rw'.format(pathname2url(self.db_path))

        if self.try_connect():
            self.initialized = True

    def log(self, msg):
        print('SpeckleCache: {}'.format(msg))   

    def create_database(self):
        try:
            conn = sqlite3.connect(self.db_path)
        except:
            self.log("Could not create database.")
            return None

        self.log("Creating database...")

        with conn:
            c = conn.cursor()
            try:
                c.execute('''CREATE TABLE Account
                             ([AccountId] integer NOT NULL PRIMARY KEY AUTOINCREMENT,[ServerName] varchar, [RestApi] varchar, [Email] varchar, [Token] varchar, [IsDefault] integer,
                             UNIQUE(RestApi,Email))''')
                c.execute('''CREATE TABLE CachedObject
                             ([CombinedHash] varchar NOT NULL PRIMARY KEY,[RestApi] varchar, [DatabaseId] varchar, [Hash] varchar, [AddedOn] bigint, [Bytes] blob)''')
                c.execute('''CREATE TABLE CachedStream
                             ([CombinedHash] varchar NOT NULL PRIMARY KEY,[RestApi] varchar, [StreamId] varchar, [AddedOn] bigint, [UpdatedOn] bigint, [Bytes] blob)''')
                c.execute('''CREATE TABLE SentObject
                             ([RestApi] varchar, [DatabaseId] varchar, [Hash] varchar)''')
                conn.commit()
                self.log("Created database.")
                return c.lastrowid           
            except sqlite3.OperationalError:
                self.log("Tables already exist.")
                return None

    def try_connect(self):
        try:
            conn = sqlite3.connect(self.db_uri, uri=True)
            return conn
        except sqlite3.OperationalError:
            self.log("Database does not exist.")            
            return None

    def account_exists(self, host, email):
        conn = self.try_connect()
        if conn == None:
            self.log("Failed to access database.")
            return False

        with conn:
            c = conn.cursor()
            try:
                c.execute(""" SELECT * FROM Account WHERE RestApi = ? AND Email = ?""", (host, email,))
                #c.execute(""" SELECT * FROM Account WHERE Email=?""", (email,))
                rows = c.fetchall()
                if len(rows) > 0:
                    return True
                return False

            except sqlite3.IntegrityError as e:
                raise

    def write_account(self, host, host_name, email, apitoken):
        # Sanitize
        host = host.strip("/")
        host = host.strip("\\")
        email = email.strip()

        conn = self.try_connect()
        if conn == None:
            raise Exception("Failed to connect to database.")

        with conn:
            c = conn.cursor()
            try:
                c.execute(""" INSERT INTO Account(AccountId,ServerName,RestApi,Email,Token,IsDefault)
                         VALUES(NULL,?,?,?,?,0) """, (host_name, host, email, apitoken))
                conn.commit()
            except sqlite3.IntegrityError as e:
                self.log("Account already exists in database.")

    def delete_account(self, host, email):
        # Sanitize
        host = host.strip("/")
        host = host.strip("\\")
        email = email.strip()

        conn = self.try_connect()
        if conn == None:
            raise Exception("Failed to connect to database.")

        with conn:
            c = conn.cursor()
            try:
                c.execute(""" DELETE FROM Account WHERE RestApi = ? AND Email = ?""", (host, email,))
                conn.commit()
            except sqlite3.IntegrityError as e:
                self.log("Account already exists in database.")

    def get_all_accounts(self):

        conn = self.try_connect()
        if conn == None:
            raise Exception("Failed to connect to database.")

        with conn:
            c = conn.cursor()
            try:
                c.execute(""" SELECT * FROM Account""")
                rows = c.fetchall()
                return rows

            except sqlite3.IntegrityError as e:
                raise

    def get_account(self, host, email):
        conn = self.try_connect()
        if conn == None:
            self.log("Failed to access database.")
            return False

        with conn:
            c = conn.cursor()
            try:
                c.execute(""" SELECT * FROM Account WHERE RestApi = ? AND Email = ?""", (host, email,))
                #c.execute(""" SELECT * FROM Account WHERE Email=?""", (email,))
                rows = c.fetchall()
                if len(rows) > 0:
                    return rows[0]
                return None

            except sqlite3.IntegrityError as e:
                raise


if __name__ == "__main__":
    db = SpeckleCache()

    db.create_database()

    res = db.write_account("https://hestia.speckle.works/api/v1", "Hestia Speckle", "tom.svilans@gmail.com", "abcd")
    res = db.write_account("https://hestia.speckle.works/api/v99", "Wam Balam", "tom.svilans@hotmail.com", "abcd")

    res = db.account_exists("https://hestia.speckle.works/api/v1", "tom.svilans@gmail.com")
    print("Account exists: {}".format(res))

    res = db.get_account("https://hestia.speckle.works/api/v1", "tom.svilans@gmail.com")
    res = db.get_all_accounts()
    print(res)

    res = db.delete_account("https://hestia.speckle.works/api/v99", "tom.svilans@hotmail.com")
