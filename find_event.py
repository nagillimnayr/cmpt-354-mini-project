import sqlite3

from constants import DB_PATH

def find_event(search_term=None, event_type=None, date=None, audience=None):
    """
    Searches for events in the library based on:
    - Title (search_term)
    - Event Type
    - Date
    - Recommended Audience
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            print("🔎 Searching for events...")

            # Base SQL query
            query = """
                SELECT E.eventId, E.title, E.type, E.dateTimeStart, E.dateTimeEnd, S.name AS location
                FROM Event E
                LEFT JOIN SocialRoom S ON E.roomId = S.roomId
                LEFT JOIN EventRecommendation ER ON E.eventId = ER.eventId
                WHERE 1=1
            """
            params = []

            # Apply filters based on user input
            if search_term:
                query += " AND E.title LIKE ?"
                params.append(f"%{search_term}%")
            if event_type:
                query += " AND E.type = ?"
                params.append(event_type)
            if date:
                query += " AND DATE(E.dateTimeStart) = ?"
                params.append(date)
            if audience:
                query += " AND ER.audienceTypeFK = ?"
                params.append(audience)

            # Execute query
            cursor.execute(query, params)
            results = cursor.fetchall()

            if results:
                print("✅ Found events:")
                for row in results:
                    print(f"{row[1]} ({row[2]}) - {row[3]} to {row[4]} at {row[5]}")
            else:
                print("No events found matching the criteria.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")