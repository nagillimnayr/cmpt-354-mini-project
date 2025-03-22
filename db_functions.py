import sqlite3

from datetime import datetime, timedelta
from utils import *

from constants import DB_PATH

# Search item
def search_for_item(search_term: str):
  """
  Searches for an Item based on the provided search term. 
  Will compare the search term with the `title`, `author`, `description`, 
  and `publisher` attributes.
  """
  
  filters = [
    'title',
    'author',
    'description',
    'publisher',
  ]
  where_clause = " OR ".join([ "Item." + filter + " LIKE :search" for filter in filters])
  query = """
    SELECT DISTINCT * 
    FROM Item
    WHERE """ + where_clause + ";"

  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    cursor.execute("PRAGMA case_sensitive_like = false;")
    cursor.execute(query, {
        'search': '%'+search_term+'%'
      }
    )
    results = cursor.fetchall()
    pretty_print(results)
  
  return results

def find_item_by_id(item_id: int):
  query = """
    SELECT * 
    FROM Item
    WHERE Item.itemId = ?;
  """
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    cursor.execute(query, (item_id,))
    result = cursor.fetchone()
    pretty_print(result)
  return result

# Borrow item
def borrow_item(member_id:int, item_id:int, personnel_id:int):
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

# Return item
def return_item(item_id:int, instance_id:int):
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
            today = get_current_date()
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

# Donate item
def donate_item(title:str, author:str, format:str, description:str, publish_date:datetime, publisher:str):
    """
    Handles the donation of an item to the library.
    1. Checks if the item already exists in the `Item` table.
    2. If it doesn't exist, adds it to `Item`.
    3. Adds a new instance of the item to `ItemInstance`.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
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

# Find event
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
  with sqlite3.connect(DB_PATH) as conn:
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
