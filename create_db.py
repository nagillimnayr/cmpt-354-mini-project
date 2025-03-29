import sqlite3
import os

from constants import DB_PATH
from utils import *


def get_all_table_names():
  with connect_to_db() as conn:
    cursor = conn.cursor()
    cursor.execute(
      """
      SELECT name 
      FROM sqlite_master 
      WHERE type='table';
      """
    )
    tables = cursor.fetchall()
    return [table['name'] for table in tables]


def drop_all_tables():
  table_names = get_all_table_names()
  with connect_to_db() as conn:
    cursor = conn.cursor()
    for table_name in table_names:
      print(f"Dropping Table: {table_name}")
      cursor.execute("DROP TABLE IF EXISTS " + table_name + ";" )


def execute_sql_in_directory(dir_name: str):
  """
  Reads all .sql files from a directory and executes the commands within.
  """
  with connect_to_db() as conn:
    cursor = conn.cursor()
    files = os.listdir(dir_name)
    for file_name in files:
      path = f'{dir_name}/{file_name}'
      with open(path) as file:
        print(f"Attempting to Execute {path}")
        command = file.read()
        cursor.executescript(command)
        print(f"Successfully Executed {path}")
  print()


def create_tables():
  print("---------------------- Creating Tables ----------------------")
  execute_sql_in_directory('schemas')
    
    
def create_views():
  print("----------------------- Creating Views ----------------------")
  execute_sql_in_directory('views')


def create_triggers():
  print("--------------------- Creating Triggers ---------------------")
  execute_sql_in_directory('triggers')


def create_database():
  create_tables()
  create_views()
  create_triggers()


def create_sample_data():
  print("--------------------- Creating Data ---------------------")
  execute_sql_in_directory('sample_data')


if __name__ == '__main__':
  try:
    drop_all_tables()
    create_database()
    create_sample_data()
    
  except sqlite3.Error as e:
    print(e)
