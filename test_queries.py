from borrow_item import borrow_item

db_path = 'library.db'

def test_queries():
  borrow_item(db_path, 1, 1, 1)
  borrow_item(db_path, 1, 1, 1)
  borrow_item(db_path, 1, 1, 1)

  
if __name__ == '__main__':
  test_queries()
