import sqlite3

from constants import *
from insert_sample_data import *
from main import *

TABLES = [
  'Audience',
  'CheckoutRecord',
  'Event',
  'EventAttendance',
  'EventRecommendation',
  'Item',
  'ItemInstance',
  'Librarian',
  'Member',
  'MemberAudienceType',
  'OverdueFine',
  'SocialRoom',
]
DROP_TABLE_COMMAND = ["DROP TABLE IF EXISTS " + table + ";" for table in TABLES]

def reset_db():
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    for cmd in DROP_TABLE_COMMAND:
      cursor.execute(cmd)
    
  create_tables()
  insert_sample_data()

if __name__ == '__main__':
  try:
    reset_db()
  except sqlite3.Error as e:
    print(e)
