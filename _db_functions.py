import sqlite3

from datetime import datetime, timedelta
from utils import *

from constants import DB_PATH



# Donate item
def donate_item(title:str, author:str, format:str, description:str, publish_date:datetime, publisher:str):
    """
    Handles the donation of an item to the library.
    1. Checks if the item already exists in the `Item` table.
    2. If it doesn't exist, adds it to `Item`.
    3. Adds a new instance of the item to `ItemInstance`.
    """
    try:
      conn = sqlite3.connect(DB_PATH)
      conn.execute("PRAGMA foreign_keys = ON;")
      with conn:
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
              VALUES ((SELECT COALESCE(MAX(instanceId), 0) + 1 FROM ItemInstance WHERE itemId = ?), ?, NULL);
          """, (item_id, item_id))

          print(f"✅ New copy of '{title}' added to library (Item ID {item_id})")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Find event
def search_for_event(search_term):
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
    with sqlite3.connect(DB_PATH) as conn:
      cursor = conn.cursor()
      cursor.execute("""
        SELECT E.eventId, E.title, E.type, E.dateTimeStart, E.dateTimeEnd, S.name AS location
          FROM Event E
          LEFT JOIN SocialRoom S ON E.roomId = S.roomId
          LEFT JOIN EventRecommendation ER ON E.eventId = ER.eventId
          WHERE E.eventId = ?;
        """, (event_id))
      result = cursor.fetchall()
      pretty_print(result)

  except sqlite3.Error as e:
    print(f"Database error: {e}")

# register for event
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
      conn = sqlite3.connect(DB_PATH)
      conn.execute("PRAGMA foreign_keys = ON;")
      with conn:
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

# Register librarian
def _find_personnel_id_by_member_id(member_id: int):
  with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT personnelId 
      FROM Personnel
      WHERE Personnel.memberId = ?;
    """, (member_id,))
    personnel_id = cursor.fetchone()
    return personnel_id
  
def register_member_as_volunteer(member_id: int):
  """
  Signs up a member to be a volunteer.
  Step 1: Check if the member is already personnel. If they are, abort.
  Step 2: Register the member as a part of personnel.
  Step 3: Display the member's Personnel ID.
  """
  current_date = get_current_date()
  conn = sqlite3.connect(DB_PATH)
  conn.execute("PRAGMA foreign_keys = ON;")
  with conn:
    cursor = conn.cursor()
    
    if _find_personnel_id_by_member_id(member_id) is not None:
      print(f"Error: Member with ID: {member_id} is already library personnel.")
      return
    
    cursor.execute("""
      INSERT INTO Personnel (memberId, role, dateJoined, salary) 
      VALUES (:memberId, "Volunteer", :date, NULL);
      """, {
      'memberId': member_id,
      'date': current_date,
    })
    conn.commit()
    
    result = _find_personnel_id_by_member_id(member_id)
    if result is not None:
      personnel_id = result[0]
      print(f"✅ Member with ID: {member_id} successfully registered as a volunteer!\nTheir Personnel ID is: {personnel_id}. ")
    else:
      print(f"Error: Failed to register member {member_id} as a volunteer.")

# Questions
def get_answers_to_question(question_id: int) -> list[dict]:
  answers = []
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = dict_row_factory
  with conn:
    answers = conn.execute("""
      SELECT * 
      FROM HelpAnswerView
      WHERE questionId = ?
      ORDER BY datePublished ASC;  
    """, (question_id,)).fetchall()
  conn.close()
  return answers
  
def get_questions() -> list[dict]:
  questions = []
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = dict_row_factory
  with conn:
    questions = conn.execute("""
      SELECT * 
      FROM HelpQuestionView
      ORDER BY datePublished ASC;                
    """).fetchall()
  conn.close()
  return questions
  
def get_questions_with_answers():
  questions = get_questions()
  questions_with_answers = []
  for question in questions:
    question_id = question['questionId']
    question_with_answers = dict(question)
    question_with_answers['answers'] = get_answers_to_question(question_id)
    questions_with_answers.append(question_with_answers)
  return questions_with_answers

def post_question(member_id: int, question: str):
  current_date = get_current_date()
  try:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    with conn:
      conn.execute("""
        INSERT INTO HelpQuestion (
          memberId, 
          question, 
          datePublished
        ) VALUES (:member_id, :question, :date_published);
        
      """, {
        'member_id': member_id,
        'question': question,
        'date_published': current_date
      })
  except sqlite3.Error as e:
    print(f"Database error: {e}")
  else:
    print(f"✅ Uploaded question: {question}")
    
def post_answer(question_id:int, personnel_id: int, answer: str):
  current_date = get_current_date()
  try:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    with conn:
      conn.execute("""
        INSERT INTO HelpAnswer (
          questionId,
          personnelId, 
          answer, 
          datePublished
        ) VALUES (:question_id, :personnel_id, :answer, :date_published);
        
      """, {
        'question_id': question_id,
        'personnel_id': personnel_id,
        'answer': answer,
        'date_published': current_date
      })
  except sqlite3.Error as e:
    print(f"Database error: {e}")
  else:
    print(f"✅ Uploaded answer: {answer}")
