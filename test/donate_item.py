import sqlite3

from constants import DB_PATH

def donate_item(db_path, title, author, format, description, publish_date, publisher):
    """
    Handles the donation of an item to the library.
    1. Checks if the item already exists in the `Item` table.
    2. If it doesn't exist, adds it to `Item`.
    3. Adds a new instance of the item to `ItemInstance`.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            print(f"🔎 Checking if '{title}' by {author} already exists in the library...")

            # Step 1: Check if the item already exists
            cursor.execute("""
                SELECT itemId FROM Item 
                WHERE title = ? AND author = ?;
            """, (title, author))
            result = cursor.fetchone()

            if result:
                item_id = result[0]
                print(f"✅ Item already exists - Item ID {item_id}")
            else:
                # Step 2: Insert new item into Item table
                cursor.execute("""
                    INSERT INTO Item (title, author, format, description, publishDate, publisher)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (title, author, format, description, publish_date, publisher))
                item_id = cursor.lastrowid
                print(f"✅ New item added to library - Item ID {item_id}")

            # Step 3: Add a new instance to ItemInstance
            cursor.execute("""
                INSERT INTO ItemInstance (instanceId, itemId, currentCheckoutId)
                VALUES ((SELECT COALESCE(MAX(instanceId), 0) + 1 FROM ItemInstance), ?, NULL);
            """, (item_id,))

            print(f"✅ New copy of '{title}' added to library (Item ID {item_id})")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
