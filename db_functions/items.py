import sqlite3
from constants import *
from utils import *

def get_items_list():
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
    
    return cursor.fetchall()

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

def print_items_list():
  """
  Prints all items.
  """
  items = get_items_list()
  
  if len(items) == 0:
    print("No items found.")
    return
  
  for item_str in [format_item(item) for item in items]:
    print(item_str, end='\n\n')


def search_for_item(search_term: str):
  """
  Searches for an Item based on the provided search term. 
  Will compare the search term with the `title`, `author`, `description`, 
  and `publisher` attributes.
  """
  
  filters = [
    'title',
    'author',
    'description',
    'publisher',
  ]
  where_clause = " OR ".join([ "Item." + filter + " LIKE :search" for filter in filters])
  query = """
    SELECT DISTINCT * 
    FROM Item
    WHERE """ + where_clause + ";"

  with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute("PRAGMA case_sensitive_like = false;")
    cursor.execute(query, {
        'search': '%'+search_term+'%'
      }
    )
    return cursor.fetchall()

def find_item_by_id(item_id: int):
  query = """
    SELECT * 
    FROM Item
    WHERE Item.itemId = ?;
  """
  with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute(query, (item_id,))
    return cursor.fetchone()
