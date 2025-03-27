import sqlite3
from constants import *
from utils import *

def format_item(item: dict) -> str:
  """
  Formats an item for printing.
  """
  return f"""
  Title: {item['title']}
  Author: {item['author']}
  Format: {item['format']}
  Publisher: {item['publisher']}
  Date Published: {item['publishDate']}
  ID: {item['itemId']}
  Description: {item['description']}
  """
  

def list_all_items():
  """
  Prints all items, sorted by format, then title.
  """
  with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = dict_row_factory
    cursor = conn.cursor()
    cursor.execute("""
      SELECT * 
      FROM Item 
      ORDER BY 
        format ASC,
        title ASC;
    """)
    
    items = cursor.fetchall()
    
    if len(items) == 0:
      print("No items found.")
      return
    
    for item in items:
      item_str = format_item(item)
      print(item_str)
