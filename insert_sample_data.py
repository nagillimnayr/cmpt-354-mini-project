import sqlite3
import os

connection = sqlite3.connect('library.db')
cursor = connection.cursor()


def insert_sample_data():
  """ 
  Reads in SQL INSERT commands from files and executes them. 
  Commands need to be executed in a specific order.
  """
  dir = 'sample_data'
  file_names = os.listdir(dir)
  for file_name in file_names:
    with open(f'{dir}/{file_name}') as file:
      command = file.read()
      cursor.execute(command)
      
  updates = [
    """
    UPDATE ItemInstance
    SET currentCheckoutId = 3 
    WHERE instanceId = 5;
    """,
    """
    UPDATE ItemInstance
    SET currentCheckoutId = 4 
    WHERE instanceId = 7;
    """,
    """
    UPDATE ItemInstance
    SET currentCheckoutId = 5 
    WHERE instanceId = 9;
    """,
    """
    UPDATE ItemInstance
    SET currentCheckoutId = 6 
    WHERE instanceId = 11;
    """,
    """
    UPDATE ItemInstance
    SET currentCheckoutId = 7 
    WHERE instanceId = 13;
    """,
    """
    UPDATE ItemInstance
    SET currentCheckoutId = 8 
    WHERE instanceId = 15;
    """,
  ]
  
  for update in updates:
    cursor.execute(update)

def main():
  insert_sample_data()
  
  
if __name__ == '__main__':
  main()
