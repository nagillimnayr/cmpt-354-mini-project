import sqlite3

from constants import *
from insert_sample_data import *
from create_db import *

TABLES = [
  'Audience',
  'CheckoutRecord',
  'Event',
  'EventAttendance',
  'EventRecommendation',
  'HelpAnswer',
  'HelpQuestion',
  'Item',
  'ItemInstance',
  'Member',
  'MemberAudienceType',
  'OverdueFine',
  'Personnel',
  'SocialRoom',
]
DROP_TABLE_COMMAND = ["DROP TABLE IF EXISTS " + table + ";" for table in TABLES]

def drop_tables():
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    for cmd in DROP_TABLE_COMMAND:
      cursor.execute(cmd)

VIEWS = [
  'HelpAnswerView',
  'HelpQuestionView',
  'PersonnelInfo',
  'PersonnelView',
]   
DROP_VIEW_COMMAND = ["DROP VIEW IF EXISTS " + view + ";" for view in VIEWS]

def drop_views():
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    for cmd in DROP_VIEW_COMMAND:
      cursor.execute(cmd)


def reset_db():
  drop_tables()    
  drop_views()
  create_database()
  insert_sample_data()

if __name__ == '__main__':
  try:
    reset_db()
  except sqlite3.Error as e:
    print(e)
