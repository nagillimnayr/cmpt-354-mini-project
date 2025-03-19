import sqlite3

from constants import DB_PATH

def register_for_event(member_id, event_id):
    """
    Registers a library member for an event.
    1. Checks if the event exists.
    2. Checks if the member exists.
    3. Checks if the member is already registered.
    4. (Optional) Checks if event capacity is full.
    5. Registers the member for the event.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            print(f"🔎 Checking if Event ID {event_id} exists...")

            # Step 1: Verify event exists
            cursor.execute("SELECT eventId, roomId FROM Event WHERE eventId = ?;", (event_id,))
            event = cursor.fetchone()
            if not event:
                print(f"Error: Event ID {event_id} does not exist.")
                return None

            room_id = event[1]
            print(f"✅ Event ID {event_id} found, located in Room {room_id}.")

            print(f"🔎 Checking if Member ID {member_id} exists...")

            # Step 2: Verify member exists
            cursor.execute("SELECT memberId FROM Member WHERE memberId = ?;", (member_id,))
            if not cursor.fetchone():
                print(f"Error: Member ID {member_id} does not exist.")
                return None

            print(f"✅ Member ID {member_id} found.")

            print(f"🔎 Checking if Member ID {member_id} is already registered for Event ID {event_id}...")

            # Step 3: Check if already registered
            cursor.execute("SELECT * FROM EventAttendance WHERE memberId = ? AND eventId = ?;", (member_id, event_id))
            if cursor.fetchone():
                print(f"Error: Member ID {member_id} is already registered for Event ID {event_id}.")
                return None

            print(f"✅ Member is not yet registered. Proceeding with registration.")

            # Step 4: (Optional) Check if event room capacity is full
            cursor.execute("""
                SELECT S.capacity, COUNT(EA.memberId)
                FROM EventAttendance EA
                JOIN Event E ON EA.eventId = E.eventId
                JOIN SocialRoom S ON E.roomId = S.roomId
                WHERE E.eventId = ?
                GROUP BY S.capacity;
            """, (event_id,))
            capacity_check = cursor.fetchone()

            if capacity_check:
                room_capacity, current_attendees = capacity_check
                if current_attendees >= room_capacity:
                    print(f"Error: Event ID {event_id} has reached full capacity ({room_capacity} attendees).")
                    return None

            # Step 5: Register the member for the event
            cursor.execute("""
                INSERT INTO EventAttendance (eventId, memberId)
                VALUES (?, ?);
            """, (event_id, member_id))

            print(f"✅ Registration successful: Member ID {member_id} is now registered for Event ID {event_id}.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")