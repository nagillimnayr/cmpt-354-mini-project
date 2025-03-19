import sqlite3

from borrow_item import *
from return_item import *
from donate_item import *
from find_event import *
from register_for_event import *
from constants import *
from find_item import *

# def test_queries():
    
#   borrow_item(member_id=3, item_id=5, librarian_id=2)

#   with sqlite3.connect(DB_PATH) as connection:
#     cursor = connection.cursor()
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


def test_queries():
  find_item("Dune")


if __name__ == '__main__':
  test_queries()
