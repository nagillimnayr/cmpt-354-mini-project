import sqlite3

from borrow_item import borrow_item
from constants import DB_PATH


def test_queries():
    
  borrow_item(member_id=3, item_id=5, librarian_id=2)

  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    cursor.execute("""
      SELECT * FROM CheckoutRecord
      WHERE memberId = 3;  
      """
    )
    result = cursor.fetchall()
    print(result)

if __name__ == '__main__':
  test_queries()
