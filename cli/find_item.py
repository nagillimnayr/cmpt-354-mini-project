

from db_functions.checkout_records import borrow_item
from db_functions.items import *

def handle_item_details(item_id: int):
  item = get_item_copy_count_view(item_id)
  if item is None: 
    print("No item found.")
    return 
  
  details = "\n".join([
    f"Title: {item['title']}",
    f"Author: {item['author']}",
    f"Format: {item['format']}",
    f"Publisher: {item['publisher']}",
    f"Date Published: {item['publishDate']}",
    f"Description: {item['description']}",
    f"ID: {item['itemId']}",
    f"Total # of Copies: {item['totalCopies']}",
    f"# of Available Copies: {item['availableCopies']}",
  ])
  print(f"\n{details}\n")
  
  num_available = int(item['availableCopies'])
  if num_available > 0:
    while True:
      option = input('Would you like to check this item out? (y/n)\n>').strip().lower()
      match option:
        case 'y':
          borrow_item()
          return 
        case 'n' | 'b' | 'back': 
          return 
        case _: 
          print('Unrecognized command.')


def handle_item_id_input(msg: str):
  while True:
    print(msg)
    item_id = input(">").strip().lower()
    if item_id == 'b': 
      return None
    if item_id.isdigit():
      return int(item_id)
    else:
      print('Invalid item ID.')

def find_item():
  while True:
    choice = input('Search by title (t), author (a), or by item ID (i): ')
    match choice:
      case 'b': break
      case 't' | 'a': 
        sTerm = input('Search Term: ')
        filters = []
        if choice == 't': filters.append('title')
        if choice == 'a': filters.append('author') 
        results = search_for_items(sTerm, filters)
        if len(results) == 0: 
          print("No items found.")
        else: 
          print('\nItems found:\n')
          print_item_list(results)
          item_id = handle_item_id_input("Enter an item's ID to see more details, or (b) to go back.\n>")
          if item_id is None:
            return 
          handle_item_details(item_id)
          
            
      case 'i':
          iId = input('Item ID: ')
          if iId == 'b': break
          
          result = get_item(int(iId))
          if result is None: print("No item found.")
          else: 
            print()
            print_item(result)
            print()
      case _:
          print('Unrecognized command.')
          continue
  con = input('Would you like to search for another item? (y/n)\n').strip().lower()
  while con not in ['y', 'n']:
      con = input('Invalid entry. Would you like to search for another item? (y/n)\n').strip().lower()
  if con == 'n': return 
