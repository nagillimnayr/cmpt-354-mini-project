import sqlite3

from borrow_item import borrow_item
from return_item import return_item
from constants import DB_PATH


def test_queries():
    
  #borrow_item(member_id=3, item_id=5, librarian_id=2)
  return_item(item_id=5, instance_id=6)

  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    cursor.execute("""
      SELECT * FROM CheckoutRecord
      WHERE memberId = 3;  
      """
    )
    result = cursor.fetchall()
    print('\n')
    print(result)
    cursor.execute("""
      SELECT currentCheckoutId FROM ItemInstance
      WHERE itemId = 5;
      """
    )
    result = cursor.fetchall()
    print(result)

if __name__ == '__main__':
  test_queries()
