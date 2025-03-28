import sqlite3

from db_functions import *
from _db_functions import *

def test_queries():
  # print_items_list()
  #  list_all_members()
  return_item(6, 1)


if __name__ == '__main__':
  try:
    test_queries()
  except sqlite3.Error as e:
        print(f"Database error: {e}")
