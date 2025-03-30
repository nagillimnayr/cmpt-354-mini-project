import json
import sqlite3
from datetime import date, datetime

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
  conn.execute("PRAGMA foreign_keys = ON;")
  return conn

def pretty_print(obj):
  if isinstance(obj, str):
    print(obj)
  else:
    formatted_string = json.dumps(obj, indent=4, sort_keys=False)
    print(formatted_string)

def convert_date(val: bytes):
  return val.decode()

sqlite3.register_converter("date", convert_date)


def print_table_list(objs: list[dict], column_labels: list[tuple[str, str]]):
  """
  Prints a table.
  The `column_labels` must contain tuples associating the keys of the dicts to 
  print with their corresponding column label.
  Example: [('key', 'Column Label')] 
  """
  max_lengths = {
    key: len(value) for key, value in column_labels
  }
  
  for obj in objs:
    for key, value in obj.items():
      max_lengths[key] = max(max_lengths[key], len(str(value)))
  
  col_sep =  ' | '
    
  header = col_sep + col_sep.join([
    f"{value:<{max_lengths[key]}}"
    for key, value in column_labels
  ]) + col_sep
  line = '-' * len(header)
  print(line)
  print(header)
  print(line)
  
  for obj in objs:
    row = col_sep + col_sep.join(
      [f"{str(obj[key]):<{max_lengths[key]}}" for key, _ in column_labels]
    ) + col_sep
    print(row)
    
  print(line)
