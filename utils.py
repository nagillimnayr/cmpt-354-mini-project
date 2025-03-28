from datetime import datetime
import json
import sqlite3

from constants import * 

def dict_row_factory(cursor, row):
  """
  https://docs.python.org/3/library/sqlite3.html#sqlite3-howto-row-factory
  """
  fields = [column[0] for column in cursor.description]
  return {key: value for key, value in zip(fields, row)}

def connect() -> sqlite3.Connection:
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = dict_row_factory
  return conn

def pretty_print(obj):
  if isinstance(obj, str):
    print(obj)
  else:
    formatted_string = json.dumps(obj, indent=4, sort_keys=False)
    print(formatted_string)

def get_current_date():
  return datetime.now().strftime("%Y-%m-%d")
