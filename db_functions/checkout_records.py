import sqlite3
from constants import *
from utils import *

def get_all_checkout_records_list():
  with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = dict_row_factory
    cursor = conn.cursor()
    cursor.execute("""
      SELECT * 
      FROM CheckoutRecord;
    """)
    return cursor.fetchall()
  
  