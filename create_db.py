import sqlite3
import os

from constants import DB_PATH
from utils import *


def get_all_table_names():
  with connect_to_db() as conn:
    tables = conn.execute(
      """
      SELECT name 
      FROM sqlite_master 
      WHERE type='table';
      """
    ).fetchall()
    return [table['name'] for table in tables]

def get_all_view_names():
  with connect_to_db() as conn:
    views = conn.execute(
      """
      SELECT name 
      FROM sqlite_master 
      WHERE type='view';
      """
    ).fetchall()
    return [view['name'] for view in views]
  
def get_all_trigger_names():
  with connect_to_db() as conn:
    triggers = conn.execute(
      """
      SELECT name 
      FROM sqlite_master 
      WHERE type='trigger';
      """
    ).fetchall()
    return [trigger['name'] for trigger in triggers]

def drop_all_triggers():
  trigger_names = get_all_trigger_names()
  pretty_print(trigger_names)
  with connect_to_db() as conn:
    conn.execute("PRAGMA foreign_keys = OFF;")
    for trigger_name in trigger_names:
      print(f"Dropping Trigger: {trigger_name}")
      conn.execute("DROP TRIGGER IF EXISTS " + trigger_name + ";" )

def drop_all_views():
  view_names = get_all_view_names()
  pretty_print(view_names)
  with connect_to_db() as conn:
    conn.execute("PRAGMA foreign_keys = OFF;")
    for view_name in view_names:
      print(f"Dropping View: {view_name}")
      conn.execute("DROP VIEW IF EXISTS " + view_name + ";" )
      
def drop_all_tables():
  table_names = get_all_table_names()
  pretty_print(table_names)
  with connect_to_db() as conn:
    conn.execute("PRAGMA foreign_keys = OFF;")
    for table_name in table_names:
      print(f"Dropping Table: {table_name}")
      conn.execute("DROP TABLE IF EXISTS " + table_name + ";" )

def drop_all():
  drop_all_triggers()
  drop_all_views()
  drop_all_tables()

def execute_sql_in_directory(dir_name: str, conn: sqlite3.Connection = connect_to_db()):
  """
  Reads all .sql files from a directory and executes the commands within.
  """
  with conn:
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
  conn = connect_to_db()
  conn.execute("PRAGMA foreign_keys = OFF;")
  execute_sql_in_directory('sample_data', conn)


if __name__ == '__main__':
  try:
    drop_all()
    create_database()
    create_sample_data()
    
  except sqlite3.Error as e:
    print(e)
