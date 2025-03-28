import sqlite3
from constants import *
from utils import *

def format_item(item: dict) -> str:
  """
  Formats an item into a string for printing.
  """
  return "\n".join([
    f"Title: {item.get('title')}",
    f"Author: {item.get('author')}",
    f"Format: {item.get('format')}",
    f"Publisher: {item.get('publisher')}",
    f"Date Published: {item.get('publishDate')}",
    f"ID: {item.get('itemId')}",
    f"Description: {item.get('description')}",
  ])

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
    
    for item_str in [format_item(item) for item in items]:
      print(item_str, end='\n\n')
