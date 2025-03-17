import sqlite3
import os

connection = sqlite3.connect('library.db')
cursor = connection.cursor()

def create_tables():
  """ 
  Reads in SQL commands from files in schemas/ folder and executes them. 
  """
  dir = 'schemas'
  schema_files = os.listdir(dir)
  for file_name in schema_files:
    with open(f'{dir}/{file_name}') as file:
      command = file.read()
      cursor.execute(command)
  
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
  
  connection.commit()

def main():
  create_tables()
  
if __name__ == '__main__':
  main()
