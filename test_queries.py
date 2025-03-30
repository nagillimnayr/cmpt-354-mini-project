import sqlite3

from db_functions import *

def test_queries():

  items = get_item_list_view()
  print_item_list_view(items)


if __name__ == '__main__':
  try:
    test_queries()
  except sqlite3.Error as e:
        print(f"Database error: {e}")
