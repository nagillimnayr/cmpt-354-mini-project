import sqlite3

from borrow_item import borrow_item

def main():
  db_path = 'library.db'
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  
  cursor.execute("""
    SELECT * FROM ItemInstance;  
    """
  )
  result = cursor.fetchall()
  print(result)

  cursor.execute("""
    SELECT * FROM CheckoutRecord
    WHERE memberId = 3;  
    """
  )
  result = cursor.fetchall()
  print(result)

  borrow_item(db_path, member_id=3, item_id=5, librarian_id=2)

  
if __name__ == '__main__':
  main()
