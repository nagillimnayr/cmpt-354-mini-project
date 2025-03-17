import sqlite3


def main():
  connection = sqlite3.connect('library.db')
  cursor = connection.cursor()
  
  cursor.execute("""
    SELECT * FROM ItemInstance;  
    """
  )
  result = cursor.fetchall()
  print(result)

  
if __name__ == '__main__':
  main()
