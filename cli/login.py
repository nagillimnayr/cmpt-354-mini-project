from db_functions import *
from constants import *

def handle_login() -> tuple[int, int | None]:
  mId = -1
  pId = None
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
        print('\nHello,', name)
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
        print('\nHello,', name)
        break
  return mId, pId
