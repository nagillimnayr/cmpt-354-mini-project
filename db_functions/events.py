import sqlite3
from constants import *
from utils import *

def search_for_event(search_term):
  """
  Searches for events in the library based on:
  - Title (search_term)
  - Event Type
  - Date
  - Recommended Audience
  """
  try:
    with connect_to_db() as conn:
      cursor = conn.cursor()

      print("🔎 Searching for events...")

      filters = [
        'title',
        'type',
        'dateTimeStart',
        'description'
      ]
      where_clause = " OR ".join([ "E." + filter + " LIKE :search" for filter in filters])
      where_clause += " OR ER.audienceType LIKE :search"

      query = """
        SELECT E.eventId, E.title, E.type, E.dateTimeStart, E.dateTimeEnd, S.name, ER.audienceType AS location
        FROM Event E
        LEFT JOIN SocialRoom S ON E.roomId = S.roomId
        LEFT JOIN EventRecommendation ER ON E.eventId = ER.eventId
        WHERE """ + where_clause + ';'
      # Execute query
      cursor.execute("PRAGMA case_sensitive_like = false;")
      cursor.execute(query, {
          'search': '%'+search_term+'%'
        }
      )
      results = cursor.fetchall()
      pretty_print(results)

  except sqlite3.Error as e:
    print(f"Database error: {e}")

def find_event_by_id(event_id: int):
  try:
    with connect_to_db() as conn:
      cursor = conn.cursor()
      cursor.execute(
        """
          SELECT E.eventId, E.title, E.type, E.dateTimeStart, E.dateTimeEnd, S.name AS location
          FROM Event E
          LEFT JOIN SocialRoom S ON E.roomId = S.roomId
          LEFT JOIN EventRecommendation ER ON E.eventId = ER.eventId
          WHERE E.eventId = ?;
        """, 
        (event_id,)
      )
      result = cursor.fetchall()
      pretty_print(result)

  except sqlite3.Error as e:
    print(f"Database error: {e}")


def register_for_event(member_id:int, event_id:int):
  """
  Registers a library member for an event.
  1. Checks if the event exists.
  2. Checks if the member exists.
  3. Checks if the member is already registered.
  4. (Optional) Checks if event capacity is full.
  5. Registers the member for the event.
  """
  try:
    with connect_to_db() as conn:
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
      cursor.execute(
        """
        SELECT S.capacity, COUNT(EA.memberId)
        FROM EventAttendance EA
        JOIN Event E ON EA.eventId = E.eventId
        JOIN SocialRoom S ON E.roomId = S.roomId
        WHERE E.eventId = ?
        GROUP BY S.capacity;
        """, 
        (event_id,)
      )
      capacity_check = cursor.fetchone()

      if capacity_check:
        room_capacity, current_attendees = capacity_check
        if current_attendees >= room_capacity:
          print(f"Error: Event ID {event_id} has reached full capacity ({room_capacity} attendees).")
          return None

      # Step 5: Register the member for the event
      cursor.execute(
        """
        INSERT INTO EventAttendance (eventId, memberId)
        VALUES (?, ?);
        """, 
        (event_id, member_id)
      )

      print(f"✅ Registration successful: Member ID {member_id} is now registered for Event ID {event_id}.")

  except sqlite3.Error as e:
      print(f"Database error: {e}")
