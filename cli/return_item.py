from db_functions import *
from constants import *
from cli.account import *

def handle_return_item(mId: int):
  borrowed_items = get_borrowed_items_for_member(mId)
  num_borrowed = len(borrowed_items)
  if num_borrowed == 0:
    print("You currently have no borrowed items.\n")
    return
  
  print(f"You currently have {num_borrowed} borrowed items:")
  print_borrowed_items(borrowed_items)
  
  while True:
    print("Enter checkout ID of item to return:")
    cId = input('>')
    if cId == 'b': return 
    while not cId.isdigit():
      print('\nInvalid checkout ID')
      continue

    return_item(int(cId))

    con = input('Would you like to return another item? (y/n)\n>').strip().lower()
    while con not in ['y', 'n']:
      con = input('Invalid entry\n>').strip().lower()
    if con == 'n': return 
