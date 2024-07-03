import sqlite3
import mysql.connector
from datetime import datetime

class DatabaseManager:
    def __init__(self, config):
        self.mysql_config = config['mysql']
        self.sqlite_config = config['sqlite']
        self.sqlite_conn = sqlite3.connect(self.sqlite_config['db_path'])
        self.create_sqlite_table()

    def create_sqlite_table(self):
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    directory TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    file_hash TEXT NOT NULL,
                    serial TEXT NOT NULL
                )
            ''')
            self.sqlite_conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating SQLite table: {e}")

    def insert_alert(self, directory, file_name, file_hash, serial, use_mysql=True):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            if use_mysql:
                mysql_conn = mysql.connector.connect(**self.mysql_config)
                cursor = mysql_conn.cursor()
                cursor.execute('''
                    INSERT INTO alerts (timestamp, directory, file_name, file_hash, serial)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (timestamp, directory, file_name, file_hash, serial))
                mysql_conn.commit()
                cursor.close()
                mysql_conn.close()
            else:
                raise mysql.connector.Error("No MySQL connection")
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}. Switching to SQLite.")
            try:
                cursor = self.sqlite_conn.cursor()
                cursor.execute('''
                    INSERT INTO alerts (timestamp, directory, file_name, file_hash, serial)
                    VALUES (?, ?, ?, ?, ?)
                ''', (timestamp, directory, file_name, file_hash, serial))
                self.sqlite_conn.commit()
            except sqlite3.Error as e:
                print(f"Error inserting alert into SQLite: {e}")

    def insert_directory(self, directory):
        try:
            mysql_conn = mysql.connector.connect(**self.mysql_config)
            cursor = mysql_conn.cursor()
            cursor.execute('''
                INSERT INTO directories (path)
                VALUES (%s)
            ''', (directory,))
            mysql_conn.commit()
            cursor.close()
            mysql_conn.close()
        except mysql.connector.Error as e:
            print(f"Error inserting directory into MySQL: {e}")
