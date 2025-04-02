from db_functions import *
from constants import *

def print_account_details(mId: int):
  borrowed_items = get_borrowed_items_for_member(mId)
  num_borrowed = len(borrowed_items)

  for item in borrowed_items:
    item['isOverdue'] = bool(item['isOverdue']) 
  
  if num_borrowed > 0:
    if num_borrowed == 1:
      print(f"You currently have {num_borrowed} borrowed item:")
    else:
      print(f"You currently have {num_borrowed} borrowed items:")
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
    overdue_items = get_overdue_items_for_member(mId)
    num_overdue = len(overdue_items)
    if num_overdue > 0:
      if num_overdue == 1:
        print(f"1 of your borrowed items is overdue:")
      else:
        print(f"{num_overdue} of your borrowed items is overdue:")
      print_table_list(overdue_items, [
        ('itemId', 'Item ID'),
        ('checkoutId', 'Checkout ID'),
        ('title', 'Title'),
        ('author', 'Author'),
        ('format', 'Format'),
        ('checkoutDate', 'Checkout Date'),
        ('dueDate', 'Due Date'),
        ('daysLate', 'Days Late'),
      ])
  else: 
    print("You currently have no borrowed items.\n")

  account_balance = get_members_outstanding_fines_balance(mId)
  print(f"You have ${account_balance:.2f} owing in outstanding fines.")
  fines = get_outstanding_fines_for_member(mId)
  if len(fines) > 0:
    print_table_list(fines, [
      ('fineId', 'Fine ID'),
      ('checkoutId', 'Checkout ID'),
      ('dueDate', 'Due Date'),
      ('returnDate', 'Return Date'),
      ('fineTotal', 'Fine Total'),
      ('amountPaid', 'Amount Paid'),
      ('balance', 'Balance Owing'),
    ])
  else: print()
    
  