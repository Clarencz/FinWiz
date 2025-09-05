import sqlite3
import pandas as pd
import os

class DBManager:
    def __init__(self, db_path="new_session.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def save_dataframe(self, df, table_name, if_exists="replace"):
        """Save a pandas DataFrame to the database."""
        self.connect()
        df.to_sql(table_name, self.conn, if_exists=if_exists, index=False)

    def load_dataframe(self, table_name):
        """Load a pandas DataFrame from the database."""
        self.connect()
        try:
            return pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
        except pd.errors.DatabaseError:
            return None

    def execute_query(self, query):
        """Execute a raw SQL query."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        return cursor.fetchall()

    def list_tables(self):
        """List all tables in the database."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type=\'table\';")
        return [table[0] for table in cursor.fetchall()]

    def __del__(self):
        self.close()



