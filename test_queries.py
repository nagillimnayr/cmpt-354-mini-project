import sqlite3

from db_functions import *

def test_queries():
  # print_items_list()
  #  list_all_members()
  borrow_item(member_id=9, item_id=6)
  # return_item(item_id=6, instance_id=2)


if __name__ == '__main__':
  try:
    test_queries()
  except sqlite3.Error as e:
        print(f"Database error: {e}")
