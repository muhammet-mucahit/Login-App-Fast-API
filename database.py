import psycopg2
from user import User

conn = psycopg2.connect(
    database = "<YOUR DATABASE NAME>",
    user     = "<YOUR DATABASE USER>",
    password = "<YOUR DATABASE PASSWORD>",
    host     = "<YOUR DATABASE HOST>",
    port     = "<YOUR DATABASE PORT>"
)

class Database:
    def __init__(self):
        self._conn = conn
        self._cursor = self._conn.cursor()

    def init(self):
        query = """
        CREATE TABLE users(
            id VARCHAR(255) PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL
        );

        CREATE TABLE resources(
            keyword VARCHAR(255) PRIMARY KEY
        );

        CREATE TABLE users_resources(
            user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
            keyword VARCHAR(255) REFERENCES resources(keyword) ON DELETE CASCADE
        );
        """
        self.cursor.execute(query)
        self.commit()

    def reset(self):
        query = """
        DROP TABLE users_resources;
        DROP TABLE resources;
        DROP TABLE users;
        """
        self.cursor.execute(query)
        self.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def getUser(self, user_id: int):
        query = "SELECT * FROM users WHERE id = '{}'".format(user_id)
        self.cursor.execute(query)
        user = self.fetchone()
        return user

    def getUsers(self):
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        users = self.fetchall()
        return users

    def saveUser(self, user: User):
        query = "INSERT INTO users(id, email) VALUES ('{}', '{}')".format(
            user.id, user.email)
        self.cursor.execute(query)
        self.commit()
    
    def deleteUser(self, user_id: str):
        query = "DELETE FROM users WHERE id='{}';".format(user_id)
        self.cursor.execute(query)
        self.commit()

    def getResourcesOfUser(self, user_id):
        query = "SELECT * FROM resources WHERE keyword IN (SELECT keyword FROM users_resources WHERE user_id='{}');".format(
            user_id)
        self.cursor.execute(query)
        resources = self.fetchall()
        return resources

    def addResourcesToUser(self, user_id, keyword):
        query = "INSERT INTO resources VALUES('{}');".format(keyword)
        self.cursor.execute(query)
        self.commit()
        query = "INSERT INTO users_resources VALUES('{}', '{}');".format(
            user_id, keyword)
        self.cursor.execute(query)
        self.commit()

import sys

if __name__ == "__main__":
    database = Database()
    arg = sys.argv[1]
    if arg == '-construct':
        database.init()
    elif arg == '-reset':
        database.reset()
    else:
        print("Wrong input, Call just with -reset or -construct")