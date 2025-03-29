import sqlite3
from constants import *
from utils import *

def get_personnel_list():
  with connect_to_db() as conn:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT * 
      FROM PersonnelView;
    """)
    return cursor.fetchall()
  
  
def find_personnel_id_by_member_id(member_id: int):
  with connect_to_db() as conn:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT personnelId 
      FROM Personnel
      WHERE Personnel.memberId = ?;
    """, (member_id,))
    return cursor.fetchone()
  
def register_member_as_volunteer(member_id: int):
  """
  Signs up a member to be a volunteer.
  Step 1: Check if the member is already personnel. If they are, abort.
  Step 2: Register the member as a part of personnel.
  Step 3: Display the member's Personnel ID.
  """
  conn = connect_to_db()
  conn.execute("PRAGMA foreign_keys = ON;")
  with conn:
    cursor = conn.cursor()
    
    if find_personnel_id_by_member_id(member_id) is not None:
      print(f"Error: Member with ID: {member_id} is already library personnel.")
      return
    
    cursor.execute("""
      INSERT INTO Personnel (memberId, role, dateJoined, salary) 
      VALUES (:memberId, "Volunteer", DATE(current_date, 'localtime'), NULL);
      """, {
      'memberId': member_id,
    })
    
    result = find_personnel_id_by_member_id(member_id)
    if result is not None:
      personnel_id = result[0]
      print(f"✅ Member with ID: {member_id} successfully registered as a volunteer!\nTheir Personnel ID is: {personnel_id}. ")
    else:
      print(f"Error: Failed to register member {member_id} as a volunteer.")
