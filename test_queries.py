import sqlite3

from db_functions import *

def test_queries():

  items = get_item_list()
  print_item_list(items)


if __name__ == '__main__':
  try:
    test_queries()
  except sqlite3.Error as e:
        print(f"Database error: {e}")
