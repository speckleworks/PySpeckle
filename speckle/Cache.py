import sqlite3, contextlib
from urllib.request import pathname2url

import os, platform

"""Speckle Cache documentation

The SpeckleCache class is used to manage user profiles and cached 
objects and streams.

Example:
    Instantiate a cache and retrieve existing user accounts::

        from speckle import SpeckleCache

        cache = SpeckleCache()

        accounts = cache.get_all_accounts()

        # Check if user profile exists
        email = "foo@bar.com"
        host = "foo.bar.com"
        res = cache.account_exists(host, email)


"""
class SpeckleCache():
    """Class for speckle cache.

    """
    initialized = False

    def __init__(self, filepath=None, create=False):
        """Initialize cache object

        This creates a SpeckleCache object using either the default database 
        location (%LOCALAPPDATA%/SpeckleSettings/SpeckleCache.db) or a user-
        specified database file.

        
        Keyword Arguments:
            filepath {str} -- Optional database filepath (default: {None})
        """        
        if filepath is None:

            """
            Get platform-dependent default SpeckleSettings directory
            """
            settings_dir = ""
            if platform.system() == "Windows":
                settings_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'SpeckleSettings')
            elif platform.system() == "Darwin":
                settings_dir = os.path.join(os.getenv('HOME'), 'SpeckleSettings')
            elif platform.system() == "Linux":
                settings_dir = os.path.join(os.getenv('HOME'), 'SpeckleSettings')

            self.db_path = os.path.join(settings_dir, 'SpeckleCache.db')
        else:
            self.db_path = filepath

        self.log(self.db_path)

        self.db_uri = 'file:{}?mode=rw'.format(pathname2url(self.db_path))

        if create:
            self.create_database(db_path)

        #if self.try_connect():
        #    self.initialized = True

    def log(self, msg):
        """Log message

        Utility function to display debug or progress messages.
        
        Arguments:
            msg {str} -- Message to display
        """            
        print('SpeckleCache: {}'.format(msg))   

    def create_database(self):
        """Create a database

        Creates a .db database at the location specified by self.db_path.
        
        """        
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
                return conn          
            except sqlite3.OperationalError:
                self.log("Tables already exist.")
                return None

    def try_connect(self):
        """Tries to connect to the database

        Attempts to connect with the database specified by self.db_path.
        Returns either a connection to the database or None.

        Returns:
            Connection -- Connection to database or None          
        
        """    
        try:
            conn = sqlite3.connect(self.db_uri, uri=True)
            return conn
        except sqlite3.OperationalError:
            self.log("Database does not exist.")            
            return None

    def account_exists(self, host, email):
        """Checks if user profile exists

        Checks the database to see if user profile exists.
        
        Arguments:
            host {str} -- Speckle server
            email {str} -- User email address

        Returns:
            Account exists -- True if account is in database, otherwise False              
        """

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
        """Write a user profile to database

        Writes a user profile to the database specified by self.db_path.
        
        Arguments:
            host {str} -- Speckle server
            email {str} -- User email address
            host_name {str} -- Name of Speckle server
            apitoken {str} -- API token for server authorization
        """

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
        """Deletes user profile from database

        Deletes a user profile from the database specified by self.db_path.
        
        Arguments:
            host {str} -- Speckle server
            email {str} -- User email address
        """

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

    def delete_all(self, table="CachedObject"):
        """Deletes all objects from table in database

        Deletes all objects from specified table in the database specified by self.db_path.
        
        Keyword Arguments:
            table {str} -- Table in database to delete all entries from {default: {"CachedObject"}}
        """

        conn = self.try_connect()
        if conn == None:
            raise Exception("Failed to connect to database.")

        with conn:
            c = conn.cursor()
            try:
                c.execute(" DELETE FROM " + table)
                conn.commit()
            except sqlite3.IntegrityError as e:
                self.log("Failed to clear table{}.".format(table))

    def get_all_accounts(self):
        """Get all accounts in database

        Gets all user profiles from the database specified by self.db_path.

        Returns:
            Accounts -- A list of tuples containing user profile data        

        """

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
        """Gets user profile from database

        Gets a user profile from the database specified by self.db_path.
        
        Arguments:
            host {str} -- Speckle server
            email {str} -- User email address

        Returns:
            Account -- A tuple containing user profile data
        """        
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
