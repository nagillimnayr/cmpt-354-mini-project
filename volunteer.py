

import sqlite3
from constants import DB_PATH
from utils import get_current_date


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
    
    
  
  
  
  