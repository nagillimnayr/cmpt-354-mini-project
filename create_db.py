import sqlite3
import os

from constants import DB_PATH


TABLES = [
  'Audience',
  'CheckoutRecord',
  'Event',
  'EventAttendance',
  'EventRecommendation',
  'HelpAnswer',
  'HelpQuestion',
  'Item',
  'ItemInstance',
  'Member',
  'MemberAudienceType',
  'OverdueFine',
  'Personnel',
  'SocialRoom',
]
DROP_TABLE_COMMANDS = ["DROP TABLE IF EXISTS " + table + ";" for table in TABLES]

def drop_tables():
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    for cmd in DROP_TABLE_COMMANDS:
      cursor.execute(cmd)

VIEWS = [
  'HelpAnswerView',
  'HelpQuestionView',
  'PersonnelInfo',
  'PersonnelView',
]   
DROP_VIEW_COMMANDS = ["DROP VIEW IF EXISTS " + view + ";" for view in VIEWS]

def drop_views():
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    for cmd in DROP_VIEW_COMMANDS:
      cursor.execute(cmd)

def drop_all():
  drop_tables()    
  drop_views()
  

def execute_sql_in_directory(dir_name: str):
  """
  Reads all .sql files from a directory and executes the commands within.
  """
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    files = os.listdir(dir_name)
    for file_name in files:
      with open(f'{dir_name}/{file_name}') as file:
        command = file.read()
        cursor.execute(command)


def create_tables():
  """ 
  Reads in SQL commands from files in schemas folder and executes them. 
  """
  execute_sql_in_directory('schemas')
    
    
def create_views():
  execute_sql_in_directory('views')


def create_triggers():
  execute_sql_in_directory('triggers')


def create_database():
  create_tables()
  create_views()
  create_triggers()

def insert_sample_data():
  """ 
  Reads in SQL INSERT commands from files and executes them. 
  Commands need to be executed in a specific order.
  """
  with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    dir = 'sample_data'
    file_names = os.listdir(dir)
    for file_name in file_names:
      with open(f'{dir}/{file_name}') as file:
        command = file.read()
        cursor.execute(command)
  

if __name__ == '__main__':
  try:
    drop_all()
    create_database()
    insert_sample_data()
      
      
    
  except sqlite3.Error as e:
    print(e)
