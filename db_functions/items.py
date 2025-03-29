import sqlite3
from constants import *
from utils import *

def get_items_list():
  with connect_to_db() as conn:
    return conn.execute(
      """
      SELECT * 
      FROM Item 
      ORDER BY 
        format ASC,
        title ASC;
      """
    ).fetchall()

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

def print_item(item: dict):
  print(format_item(item))

def print_items_list(items: list[dict]):
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

  with connect_to_db() as conn:
    cursor = conn.cursor()
    return cursor.execute(
      "PRAGMA case_sensitive_like = false;"
    ).execute(
      query, 
      {
      'search': '%'+search_term+'%'
      }
    ).fetchall()

def find_item_by_id(item_id: int):
  query = """
    SELECT * 
    FROM Item
    WHERE Item.itemId = ?;
  """
  with connect_to_db() as conn:
    return conn.execute(query, (item_id,)).fetchone()


def donate_item(title:str, author:str, format:str, description:str, publish_date: str, publisher:str):
  """
  Handles the donation of an item to the library.
  1. Checks if the item already exists in the `Item` table.
  2. If it doesn't exist, adds it to `Item`.
  3. Adds a new instance of the item to `ItemInstance`.
  """
  try:
    with connect_to_db() as conn:
      cursor = conn.cursor()

      print(f"🔎 Checking if '{title}' by {author} already exists in the library...")

      # Step 1: Check if the item already exists
      cursor.execute(
        """
        SELECT itemId FROM Item 
        WHERE title = ? AND author = ?;
        """, 
        (title, author)
      )
      result = cursor.fetchone()

      if result:
        item_id = result[0]
        print(f"✅ Item already exists - Item ID {item_id}")
      else:
        # Step 2: Insert new item into Item table
        cursor.execute(
          """
          INSERT INTO Item (title, author, format, description, publishDate, publisher)
          VALUES (?, ?, ?, ?, ?, ?);
          """, 
          (title, author, format, description, publish_date, publisher)
        )
        item_id = cursor.lastrowid
        print(f"✅ New item added to library - Item ID {item_id}")

      # Step 3: Add a new instance to ItemInstance
      cursor.execute(
        """
        INSERT INTO ItemInstance (instanceId, itemId, currentCheckoutId)
        VALUES ((SELECT COALESCE(MAX(instanceId), 0) + 1 FROM ItemInstance WHERE itemId = ?), ?, NULL);
        """, 
        (item_id, item_id)
      )

      print(f"✅ New copy of '{title}' added to library (Item ID {item_id})")

  except sqlite3.Error as e:
    print(f"Database error: {e}")
