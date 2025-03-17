import sqlite3
from datetime import datetime, timedelta

def borrow_item(db_path, member_id, item_id, librarian_id):
    """
    Goal, borrow an item from the library.
    Steps:
      1. Find an available copy of the item.
      2. Create a new checkout record.
      3. Update ItemInstance to reflect checkout.
    """
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Step 1: Find an available item instance
        cursor.execute("""
            SELECT instanceId FROM ItemInstance
            WHERE itemId = ? AND currentCheckoutId IS NULL
            LIMIT 1;
        """, (item_id,))
        result = cursor.fetchone()
        print(result)

        if not result:
            print("No available copies for this item.")
            return

        instance_id = result[0]

        # Step 2: Insert new checkout record
        checkout_date = datetime.now().strftime("%Y-%m-%d")  # Get current date
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO CheckoutRecord (memberId, itemId, instanceId, librarianId, checkoutDate, dueDate, returnDate)
            VALUES (?, ?, ?, ?, ?, ?, NULL);
        """, (member_id, item_id, instance_id, librarian_id, checkout_date, due_date))

        # Step 3: Get the last inserted checkoutId
        checkout_id = cursor.lastrowid

        # Step 4: Update ItemInstance to mark the item as checked out
        cursor.execute("""
            UPDATE ItemInstance
            SET currentCheckoutId = ?
            WHERE instanceId = ?;
        """, (checkout_id, instance_id))

        # Commit transaction
        conn.commit()
        print(f"✅ Item {item_id} (Instance {instance_id}) successfully borrowed by Member {member_id}. Due on {due_date}.")
    
    except sqlite3.Error as e:
        conn.rollback()  # Rollback changes if error occurs
        print(f"Database error: {e}")

    finally:
        conn.close()  # Close connection

