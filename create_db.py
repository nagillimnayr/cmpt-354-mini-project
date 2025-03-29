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
  conn = connect_to_db()
  with conn:
    cursor = conn.cursor()
    files = os.listdir(dir_name)
    for file_name in files:
      path = f'{dir_name}/{file_name}'
      with open(path) as file:
        print(f"Attempting to Execute {path}")
        command = file.read()
        cursor.execute(command)
        print(f"Successfully Executed {path}")


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


def insert_sample_data():
  """ 
  # Reads in SQL INSERT commands from files and executes them. 
  """
  print("--------------------- Inserting Data ---------------------")
  execute_sql_in_directory('sample_data/insert')

def update_sample_data():
  """
  This sample data is added to the database via UPDATE rather than INSERT
  so that we can take advantage of our triggers to handle automating 
  certain tasks.
  """
  print("--------------------- Updating Data ---------------------")
  execute_sql_in_directory('sample_data/update')

def create_sample_data():
  insert_sample_data()
  update_sample_data()

if __name__ == '__main__':
  try:
    drop_all_tables()
    create_database()
    create_sample_data()
    
  except sqlite3.Error as e:
    print(e)
