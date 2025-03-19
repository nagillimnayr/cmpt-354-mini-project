import sqlite3
from datetime import datetime, timedelta

from constants import DB_PATH

def borrow_item(member_id, item_id, personnel_id):
    """
    Handles borrowing an item:
    1. Checks for available copies.
    2. Creates a checkout record.
    3. Updates ItemInstance to mark the item as checked out.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            print(f"🔎 Checking for available copies of Item ID {item_id}...")

            # Step 1: Find an available copy (not checked out)
            cursor.execute("""
                SELECT instanceId FROM ItemInstance
                WHERE itemId = ? AND currentCheckoutId IS NULL
                LIMIT 1;
            """, (item_id,))
            result = cursor.fetchone()

            if not result:
                print(f"Error: No available copies for Item ID {item_id}.")
                return None

            instance_id = result[0]
            print(f"✅ Step 1: Found available copy - Instance ID {instance_id}")

            # Step 2: Insert a new checkout record
            checkout_date = datetime.now().strftime("%Y-%m-%d")
            due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

            cursor.execute("""
                INSERT INTO CheckoutRecord (memberId, itemId, instanceId, personnelId, checkoutDate, dueDate, returnDate)
                VALUES (?, ?, ?, ?, ?, ?, NULL);
            """, (member_id, item_id, instance_id, personnel_id, checkout_date, due_date))

            checkout_id = cursor.lastrowid  # Retrieve the newly inserted checkoutId
            print(f"✅ Step 2: Created checkout record - Checkout ID {checkout_id}, Due Date {due_date}")

            # Step 3: Update ItemInstance to mark it as checked out
            cursor.execute("""
                UPDATE ItemInstance
                SET currentCheckoutId = ?
                WHERE instanceId = ? AND itemId = ?;
            """, (checkout_id, instance_id, item_id))

            print(f"✅ Step 3: Item ID {item_id}, Instance ID {instance_id} marked as checked out.")

            print(f"✅ Borrow process completed for Item ID {item_id}, Instance ID {instance_id}.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
