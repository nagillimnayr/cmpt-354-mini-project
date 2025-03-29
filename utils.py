from datetime import datetime, date
import json
import sqlite3

from constants import * 

def dict_row_factory(cursor, row):
  """
  https://docs.python.org/3/library/sqlite3.html#sqlite3-howto-row-factory
  """
  fields = [column[0] for column in cursor.description]
  return {key: value for key, value in zip(fields, row)}

def connect_to_db() -> sqlite3.Connection:
  conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
  conn.row_factory = dict_row_factory
  return conn

def pretty_print(obj):
  if isinstance(obj, str):
    print(obj)
  else:
    formatted_string = json.dumps(obj, indent=4, sort_keys=False)
    print(formatted_string)

def convert_date(val):
    """Convert ISO 8601 date to datetime.date object."""
    return date.fromisoformat(val.decode())

sqlite3.register_converter("date", convert_date)
