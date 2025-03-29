import sqlite3
from datetime import datetime, timedelta

from constants import *
from db_functions.item_instances import select_item_instance
from utils import *


def get_all_checkout_records_list():
  with connect_to_db() as conn:
    return conn.execute("""
      SELECT * 
      FROM CheckoutRecord;
    """).fetchall()
  

def borrow_item(member_id: int, item_id: int):
  """
  Handles borrowing an item:
  1. Checks for available copies.
  2. Creates a checkout record.
  3. Updates ItemInstance to mark the item as checked out.
  """
  try:
    with connect_to_db() as conn:
      cursor = conn.cursor()

      print(f"🔎 Checking for available copies of Item ID {item_id}...")

      # Step 1: Find an available copy (not checked out)
      cursor.execute("""
        SELECT instanceId 
        FROM ItemInstance
        WHERE 
          itemId = ? AND currentCheckoutId IS NULL
        LIMIT 1;
      """, (item_id,))
      result: dict = cursor.fetchone()

      if result is None:
        print(f"Error: No available copies for Item ID {item_id}.")
        return None

      instance_id = result['instanceId']
      print(f"✅ Step 1: Found available copy - Instance ID {instance_id}")

      # Step 2: Insert a new checkout record

      cursor.execute("""
        INSERT INTO CheckoutRecord (memberId, itemId, instanceId, checkoutDate, dueDate, returnDate)
        VALUES (?, ?, ?, date('now'), date('now', '+14 days'), NULL);
      """, (member_id, item_id, instance_id))
      checkout_id = cursor.lastrowid  # Retrieve the newly inserted checkoutId

      cursor.execute("""
        SELECT dueDate 
        FROM CheckoutRecord
        WHERE checkoutId = ?;
      """, (checkout_id,))
      checkout_record = cursor.fetchone()
      due_date = checkout_record['dueDate']
      
      print(f"✅ Step 2: Created checkout record - Checkout ID {checkout_id}, Due Date {due_date}")

      instance = select_item_instance(item_id, instance_id)
      
      assert instance['currentCheckoutId'] == checkout_id

      print(f"✅ Step 3: Item ID {item_id}, Instance ID {instance_id} marked as checked out.")

      print(f"✅ Borrow process completed for Item ID {item_id}, Instance ID {instance_id}.")

  except sqlite3.Error as e:
      print(f"Database error: {e}")


def return_item(item_id:int, instance_id:int):
  """
  Handles returning a borrowed item:
  1. Finds the active checkout record (if exists).
  2. Updates CheckoutRecord to mark it as returned.
  3. Updates ItemInstance to make it available for borrowing.
  4. (Optional) Applies a fine if the item is overdue.
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
        SET returnDate = date('now')
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

      # Step 4: (Optional) Apply overdue fine if the item is returned late
      cursor.execute("""
        INSERT INTO OverdueFine (checkoutId, fineTotal, amountPaid, dateIssued)
        SELECT ?, 
                (JULIANDAY(?) - JULIANDAY(dueDate)) * 0.50, 
                0, ?
        FROM CheckoutRecord
        WHERE checkoutId = ? AND ? > dueDate;
      """, (checkout_id, return_date, return_date, checkout_id, return_date))

      print("✅ Overdue fine checked (if applicable).")
      print(f"✅ Return process completed for Item ID {item_id}, Instance ID {instance_id}.")

  except sqlite3.Error as e:
    print(f"Database error: {e}")
