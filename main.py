import sqlite3
import os

connection = sqlite3.connect('library.db')
cursor = connection.cursor()

def create_tables():
  """ 
  Reads in SQL commands from files in schemas/ folder and executes them. 
  """
  schema_files = os.listdir('schemas')
  for file_name in schema_files:
    with open(f'schemas/{file_name}') as file:
      command = file.read()
      cursor.execute(command)
      
    

def main():
  create_tables()
  
if __name__ == '__main__':
  main()
