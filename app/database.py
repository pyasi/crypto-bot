import psycopg2
import urllib.parse as urlparse
import os


class Database:
    def __init__(self, table_name):
        self.table_name = table_name
        self.connect()

    def __del__(self):
        self.cursor().close()
        self.connection.close()

    def connect(self):
        try:
            if os.environ.get('DATABASE_URL'):
                url = urlparse.urlparse(os.environ['DATABASE_URL'])
                database_name = url.path[1:]
                user = url.username
                password = url.password
                host = url.hostname
                port = url.port
                database_name = 'crypto_portfolio'
                self.connection = psycopg2.connect(database=database_name,
                                                   user=user,
                                                   password=password,
                                                   host=host,
                                                   port=port)
            else:
                database_name = 'crypto_portfolio'
                self.connection = psycopg2.connect(database=database_name)

        except psycopg2.OperationalError:
            pg_connection = psycopg2.connect(database="postgres")
            pg_connection.set_isolation_level(0)
            pg_connection.cursor().execute("CREATE DATABASE " + database_name)
            pg_connection.cursor().close()
            pg_connection.close()
            self.connection = psycopg2.connect(database=database_name)
            self.connection.set_isolation_level(1)

        try:
            cursor = self.cursor()
            cursor.execute("select 1 from " + self.table_name)
            cursor.fetchone()
            print("connected to " + self.table_name)
        except psycopg2.DatabaseError as de:
            print("could not find table " + self.table_name + ", creating now")
            self.connection.commit()
            self.create_table()

    def create_table(self):
        try:
            print("creating table " + self.table_name)
            self.cursor().execute("CREATE TABLE " + self.table_name + ""
                                  " ( "
                                  "    id serial PRIMARY KEY,"
                                  "    username varchar, "
                                  "    coin varchar, "
                                  "    ticker varchar, "
                                  "    amount real"
                                  ");")
            self.connection.commit()
        except psycopg2.Error as e:
            print("Could not create table, error: " + e.pgerror)
            exit(1)

    def cursor(self):
        return self.connection.cursor()

    def ensure_connected(self):
        try:
            self.connection.isolation_level
        except ConnectionError as oe:
            self.connect()

    def enter_coin(self, values):
        """
        Called when a user uses the /portfolio slash command. Decides whether
        to update an existing row or create a new one

        :param values: Values to enter into DB
        """
        self.ensure_connected()
        cursor = self.cursor()
        cursor.execute(
            "SELECT exists(SELECT ticker FROM {} where username = '{}' and ticker = '{}');".
            format(self.table_name, values['username'], values['ticker']))
        if cursor.fetchone()[0]:
            self.update_coin(values)
        else:
            self.add_coin(values)

    def add_coin(self, values):
        """
        Creates a row in the DB with the given values

        :param values: Values with coin details
        """
        self.ensure_connected()
        add_row = (
            "INSERT INTO {}(username, coin, ticker, amount) VALUES('{}', '{}', '{}', {});".
            format(self.table_name, values['username'], values['coin'],
                   values['ticker'], values['amount']))
        self.cursor().execute(add_row, values)
        self.connection.commit()

    def update_coin(self, values):
        """
        Updates an existing row in the DB with the given values

        :param values: Values with coin details
        """
        self.ensure_connected()

        update_row = (
            "UPDATE {} set amount = {} where ticker = '{}' and username = '{}'".
            format(self.table_name, values['amount'], values['ticker'],
                   values['username']))
        self.cursor().execute(update_row)
        self.connection.commit()

    def delete_coin(self, values):
        """
        Deletes a coin from the DB for a user

        :param values: Values with coin details
        """
        self.ensure_connected()

        delete_row = (
            "DELETE from {} WHERE ticker = '{}' and username = '{}'".
            format(self.table_name, values['ticker'], values['username']))
        self.cursor().execute(delete_row)
        self.connection.commit()

    def get_user_portfolio(self, user_id):
        """
        Gets the user's portfolio from the DB

        :return: All user's rows
        """
        self.ensure_connected()
        cursor = self.cursor()
        cursor.execute(
            "SELECT coin, ticker, amount FROM {} where username = '{}';".
            format(self.table_name, user_id))
        return cursor.fetchall()
