import sqlite3

from borrow_item import borrow_item
from return_item import return_item
from donate_item import donate_item
from find_event import find_event
from register_for_event import register_for_event
from constants import DB_PATH


def test_queries():
    
  #borrow_item(member_id=3, item_id=5, librarian_id=2)
  #return_item(item_id=5, instance_id=6)
  # donate_item(DB_PATH, 
  #   title="The Pragmatic Programmer", 
  #   author="Andy Hunt, Dave Thomas", 
  #   format="Hardcover", 
  #   description="A guide to programming best practices.", 
  #   publish_date="1999-10-30", 
  #   publisher="Addison-Wesley")
  # find_event(search_term="Book Club")
  register_for_event(member_id=3, event_id=5)


  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    # cursor.execute("""
    #   SELECT * FROM CheckoutRecord
    #   WHERE memberId = 3;  
    #   """
    # )
    # result = cursor.fetchall()
    # print('\n')
    # print(result)
    # cursor.execute("""
    #   SELECT currentCheckoutId FROM ItemInstance
    #   WHERE itemId = 5;
    #   """
    # )
    # result = cursor.fetchall()
    # print(result)
    # cursor.execute("""
    #   SELECT * FROM ItemInstance
    #   WHERE itemId = 16; 
    # """)
    # result = cursor.fetchall()
    # print(result)


if __name__ == '__main__':
  test_queries()
