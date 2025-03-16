import sqlite3
import os

connection = sqlite3.connect('library.db')
cursor = connection.cursor()

def insert_sample_data():
  """ 
  Reads in SQL INSERT commands from files and executes them. 
  """
  files = os.listdir()
  for file_name in files:
    with open(f'schemas/{file_name}') as file:
      command = file.read()
      cursor.execute(command)

def main():
  insert_sample_data()
  
  
if __name__ == '__main__':
  main()
