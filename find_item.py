import sqlite3
from constants import DB_PATH
from utils import pretty_print


def search_item_by_title(search_term: str):
  """
  
  """
  results = []
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    # cursor.execute("PRAGMA case_sensitive_like = false;")
    cursor.execute("""
      SELECT * 
      FROM Item
      WHERE Item.title LIKE ?
      ;         
      """,
      ('%'+search_term+'%',)
    )
    results = cursor.fetchall()
  return results

def search_item_by_author(search_term: str):
  """
  
  """
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    
    

def search_item_by_description(search_term: str):
  """
  
  """
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    
    
def search_item_by_publisher(search_term: str):
  """
  
  """
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    

def find_item(search_term: str):
  """
  
  """
  results = search_item_by_title(search_term)
  pretty_print(results)

    
    