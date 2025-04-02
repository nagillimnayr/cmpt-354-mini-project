from db_functions import *
from constants import *

def handle_login() -> tuple[int, int | None]:
  mId = -1
  pId = None
  name = ''
  print ('Hello, are you a member (m) or personnel (p)?')
  uInput = input('> ').strip().lower()
  while not uInput in ['m', 'p']: uInput = input('Invalid entry (m or p) \n> ').strip().lower()
  match uInput:
    case 'm':
      while True:
        mId = input('Enter Member ID:\n> ')
        if mId in QUIT_COMMANDS:
          print('Exiting...')
          exit(0)
        if not mId.isdigit(): 
          print('Invalid Member ID, enter again\n')
          continue
        mId = int(mId)

        member = get_member(mId)
        if member is None:
          print(f'Member with ID: {mId} not found, please enter again\n')
          continue
      
        name = member['firstName'] + ' ' + member['lastName']
        break
    case 'p':
      while True:
        pId = input('Enter Personnel ID\n> ')
        if pId in QUIT_COMMANDS:
          print('Exiting...')
          exit(0)
        if not pId.isdigit(): 
          print('Invalid Personnel ID, enter again\n')
          continue
        pId = int(pId)
    
        personnel = get_personnel(pId)
        if personnel is None:
          print(f'Personnel with ID: {pId} not found, please enter again\n')
          continue
        mId = int(personnel['memberId'])
        name = personnel['firstName'] + ' ' + personnel['lastName']
        break
  print('\nHello,', name)
  
  borrowed_items = get_borrowed_items_for_member(mId)
  overdue_items = [item for item in borrowed_items if item['isOverdue']]
  num_borrowed = len(borrowed_items)
  num_overdue = len(overdue_items)
  
  print(f"You currently have {num_borrowed} borrowed items, {num_overdue} of which are overdue:")
  
  for item in borrowed_items:
    item['isOverdue'] = bool(item['isOverdue']) 
  
  if num_borrowed > 0:
    print_table_list(borrowed_items, [
      ('itemId', 'Item ID'),
      ('checkoutId', 'Checkout ID'),
      ('title', 'Title'),
      ('author', 'Author'),
      ('format', 'Format'),
      ('checkoutDate', 'Checkout Date'),
      ('dueDate', 'Due Date'),
      ('isOverdue', 'Is Overdue?'),
    ])
  
  return mId, pId
