import sqlite3
from datetime import datetime, timedelta

from constants import *
from db_functions.item_instances import select_item_instance
from utils import *


def get_all_checkout_records_list():
  with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = dict_row_factory
    cursor = conn.cursor()
    cursor.execute("""
      SELECT * 
      FROM CheckoutRecord;
    """)
    return cursor.fetchall()
  

def borrow_item(member_id: int, item_id: int):
  """
  Handles borrowing an item:
  1. Checks for available copies.
  2. Creates a checkout record.
  3. Updates ItemInstance to mark the item as checked out.
  """
  try:
    conn = connect()
    conn.execute("PRAGMA foreign_keys = ON;")
    with conn:
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

      if not result:
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

      instance = select_item_instance(conn, item_id, instance_id)
      
      assert instance['currentCheckoutId'] == checkout_id

      print(f"✅ Step 3: Item ID {item_id}, Instance ID {instance_id} marked as checked out.")

      print(f"✅ Borrow process completed for Item ID {item_id}, Instance ID {instance_id}.")

  except sqlite3.Error as e:
      print(f"Database error: {e}")
