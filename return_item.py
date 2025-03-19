import sqlite3
from datetime import datetime

from constants import DB_PATH

def return_item(item_id, instance_id):
    """
    Handles returning a borrowed item:
    1. Finds the active checkout record (if exists).
    2. Updates CheckoutRecord to mark it as returned.
    3. Updates ItemInstance to make it available for borrowing.
    4. (Optional) Applies a fine if the item is overdue.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            print(f"🔎 Checking if Item ID {item_id}, Instance ID {instance_id} is currently borrowed...")

            # Step 1: Find active checkout record
            cursor.execute("""
                SELECT checkoutId, dueDate FROM CheckoutRecord
                WHERE instanceId = ? AND itemId = ? AND returnDate IS NULL;
            """, (instance_id, item_id))
            result = cursor.fetchone()

            if not result:
                print(f"Error: Item ID {item_id}, Instance ID {instance_id} is NOT currently checked out.")
                return None

            checkout_id, due_date = result
            print(f"✅ Found active checkout: Checkout ID {checkout_id}, Due Date {due_date}")

            # Step 2: Mark the checkout record as returned
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("""
                UPDATE CheckoutRecord
                SET returnDate = ?
                WHERE checkoutId = ?;
            """, (today, checkout_id))

            print(f"✅ Checkout ID {checkout_id} marked as returned on {today}")

            # Step 3: Update ItemInstance to make it available
            cursor.execute("""
                UPDATE ItemInstance
                SET currentCheckoutId = NULL
                WHERE instanceId = ? AND itemId = ?;
            """, (instance_id, item_id))

            print(f"✅ Item ID {item_id}, Instance ID {instance_id} is now available for borrowing.")

            # Step 4: (Optional) Apply overdue fine if the item is returned late
            cursor.execute("""
                INSERT INTO OverdueFine (checkoutId, fineTotal, amountPaid, dateIssued)
                SELECT ?, 
                       (JULIANDAY(?) - JULIANDAY(dueDate)) * 0.50, 
                       0, ?
                FROM CheckoutRecord
                WHERE checkoutId = ? AND ? > dueDate;
            """, (checkout_id, today, today, checkout_id, today))

            print("✅ Overdue fine checked (if applicable).")
            print(f"✅ Return process completed for Item ID {item_id}, Instance ID {instance_id}.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

