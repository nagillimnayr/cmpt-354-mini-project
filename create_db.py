import sqlite3
import os

from constants import DB_PATH

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
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    """
    We can't use subqueries inside `CHECK` or `ASSERTION` statements, so we must
    use a `TRIGGER` to impose constraint on number of `OverdueFine`s for a single
    `CheckoutRecord`.
    """
    cursor.execute("""
      CREATE TRIGGER IF NOT EXISTS max_overdue_fines_per_checkout 
      BEFORE INSERT ON OverdueFine 
      WHEN (
          SELECT COUNT(*)
          FROM OverdueFine AS O
          WHERE O.checkoutId = NEW.checkoutId
        ) >= 10
      BEGIN
          SELECT 
          RAISE (ABORT, 'Maximum number of fines reached for this Checkout');
      END;
      """
    )

def create_database():
  create_tables()
  create_views()
  create_triggers()


if __name__ == '__main__':
  try:
    create_database()
  except sqlite3.Error as e:
    print(e)
