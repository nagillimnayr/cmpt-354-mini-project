import sqlite3
from constants import *
from utils import *

def get_personnel_list():
  with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = dict_row_factory
    cursor = conn.cursor()
    cursor.execute("""
      SELECT * 
      FROM PersonnelView;
    """)
    
    return cursor.fetchall()
  
  