import sqlite3
from constants import DB_PATH
from utils import pretty_print

def find_item(search_term: str):
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

  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    cursor.execute("PRAGMA case_sensitive_like = false;")
    cursor.execute(query, {
        'search': '%'+search_term+'%'
      }
    )
    results = cursor.fetchall()
    pretty_print(results)
    connection.close()

    
    