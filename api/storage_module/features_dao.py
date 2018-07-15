#!/usr/bin/python3
from storage_module.psqldb import PsqlDB
from storage_module.app_exceptions import DatabaseError, MissingParameterError


# The PostGIS Data Access Object handles all interactions with the feature table.
class FeatureDao:

    #constructor
    def __init__(self):
        self.db = PsqlDB()

    def getServerParams(self):
        return self.db.getServerParams()

    def getTableColumns(self, table):
        """
        Prepare the query statement and get result as a list of table attributes.
        Parameter table: The table name for read the columns
        Return the string of column names joined by a comma between the names
        """

        sql = "SELECT * FROM {} LIMIT 1".format( table )
        self.__basicExecute(sql)
        colnames = [desc[0] for desc in self.db.cur.description]
        s = ","
        return s.join( colnames )

    def __basicExecute(self, sql):
        """
        Execute a basic SQL statement.
        
        Parameter sql: The string that represents the query statement

        """

        try:
            self.db.execQuery(sql)
        except Exception as error:
            self.db.rollback()
            raise DatabaseError('Database error:', error)