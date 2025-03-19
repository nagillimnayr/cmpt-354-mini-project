

import sqlite3
from constants import DB_PATH
from utils import get_current_date


def _find_librarian_id_by_member_id(member_id: int):
  with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT librarianId 
      FROM Librarian
      WHERE Librarian.memberId = ?;
    """, (member_id,))
    librarian_id = cursor.fetchone()
    return librarian_id

def register_member_as_volunteer(member_id: int):
  """
  Signs up a member to be a volunteer librarian.
  Step 1: Check if the member is already a librarian. If they are, abort.
  Step 2: Register the member as a librarian.
  Step 3: Display the member's librarian ID.
  """
  current_date = get_current_date()
  with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    
    if _find_librarian_id_by_member_id(member_id) is not None:
      print(f"Error: Member with ID: {member_id} is already a Librarian.")
      return
    
    cursor.execute("""
      INSERT INTO Librarian (memberId, isVolunteer, dateJoined) 
      VALUES (:memberId, TRUE, :date);
      """, {
      'memberId': member_id,
      'date': current_date,
    })
    conn.commit()
    
    result = _find_librarian_id_by_member_id(member_id)
    if result is not None:
      librarian_id = result[0]
      print(f"✅ Member with ID: {member_id} successfully registered as a volunteer!\nTheir Librarian ID is: {librarian_id}. ")
    else:
      print(f"Error: Failed to register member {member_id} as a volunteer.")
    
    
  
  
  
  