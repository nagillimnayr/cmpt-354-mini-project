import sqlite3

from constants import *
from db_functions.item_instances import *
from utils import *


def get_all_checkout_records_list():
  with connect_to_db() as conn:
    return conn.execute("""
      SELECT * 
      FROM CheckoutRecord;
    """).fetchall()

def get_borrowed_items_for_member(member_id: int):
  with connect_to_db() as conn:
    return conn.execute(
      """
      SELECT * 
      FROM 
        BorrowedItemsView
      WHERE 
        memberId = ?
      ORDER BY 
        checkoutDate;
      """, (member_id,)
    ).fetchall() 

def get_overdue_items_for_member(member_id: int):
  with connect_to_db() as conn:
    return conn.execute(
      """
      SELECT 
        *,
        FLOOR(JULIANDAY(current_date, 'localtime') - JULIANDAY(dueDate, 'localtime')) AS daysLate 
      FROM 
        BorrowedItemsView
      WHERE 
        memberId = ?
        AND 
        isOverdue IS TRUE
      ORDER BY 
        checkoutDate;
      """, (member_id,)
    ).fetchall() 

def borrow_item(member_id: int, item_id: int):
  """
  Handles borrowing an item:
  1. Checks for available copies.
  2. Creates a checkout record.
  """
  try:
    with connect_to_db() as conn:
      cursor = conn.cursor()

      # Step 1: Find an available copy (not checked out)
      instance = get_available_item_instance(item_id)

      if instance is None:
        print(f"Error: No available copies for Item ID {item_id}.")
        return None

      instance_id = instance['instanceId']
      title = instance['title']

      # Step 2: Insert a new checkout record
      cursor.execute("""
        INSERT INTO CheckoutRecord (memberId, itemId, instanceId, checkoutDate, dueDate)
        VALUES (?, ?, ?, DATE(current_date, 'localtime'), DATE(current_date, 'localtime', '+14 days'));
      """, (member_id, item_id, instance_id))
      checkout_id = cursor.lastrowid  # Retrieve the newly inserted checkoutId

      cursor.execute("""
        SELECT dueDate 
        FROM CheckoutRecord
        WHERE checkoutId = ?;
      """, (checkout_id,))
      checkout_record = cursor.fetchone()
      due_date = checkout_record['dueDate']
      
      print(f'✅ Successfully checked out copy of "{title}"')
      print(f"Item ID {item_id}, Instance ID {instance_id}")
      print(f"Checkout ID {checkout_id}, Due Date {due_date}")

  except sqlite3.Error as e:
      print(f"Error: {e}")


def return_item(item_id:int, instance_id:int):
  """
  Handles returning a borrowed item:
  1. Finds the active checkout record (if exists).
  2. Updates CheckoutRecord to mark it as returned.
  3. Updates ItemInstance to make it available for borrowing.
  """
  try:
    with connect_to_db() as conn:
      cursor = conn.cursor()

      print(f"🔎 Checking if Item ID {item_id}, Instance ID {instance_id} is currently borrowed...")

      # Step 1: Find active checkout record
      cursor.execute("""
        SELECT checkoutId, dueDate 
        FROM CheckoutRecord
        WHERE instanceId = ? AND itemId = ? AND returnDate IS NULL;
      """, (instance_id, item_id))
      checkout_record = cursor.fetchone()

      if checkout_record is None:
        print(f"Error: Item ID {item_id}, Instance ID {instance_id} is NOT currently checked out.")
        return None

      checkout_id = checkout_record['checkoutId']
      due_date = checkout_record['dueDate']
      print(f"✅ Found active checkout: Checkout ID {checkout_id}, Due Date {due_date}")

      # Step 2: Mark the checkout record as returned
      cursor.execute("""
        UPDATE CheckoutRecord
        SET returnDate = DATE(current_date, 'localtime')
        WHERE checkoutId = ?;
      """, (checkout_id,))
      
      conn.commit()
      
      cursor.execute("""
        SELECT * 
        FROM CheckoutRecord
        WHERE checkoutId = ?;
      """, (checkout_id,))
      checkout_record = cursor.fetchone()
      return_date = checkout_record['returnDate']

      print(f"✅ Checkout ID {checkout_id} marked as returned on {return_date}")

      print(f"✅ Item ID {item_id}, Instance ID {instance_id} is now available for borrowing.")

      print(f"✅ Return process completed for Item ID {item_id}, Instance ID {instance_id}.")

  except sqlite3.Error as e:
    print(f"Database error: {e}")
