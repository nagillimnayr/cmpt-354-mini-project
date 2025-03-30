import sqlite3
from constants import *
from utils import *

def get_personnel_list():
  with connect_to_db() as conn:
    return conn.execute(
      """
      SELECT * 
      FROM PersonnelView;
      """
    ).fetchall()
  
def get_personnel_ids():
  with connect_to_db() as conn:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT personnelId, memberId
      FROM personnel;
    """)
    return cursor.fetchall()
  
def find_personnel_id_by_member_id(member_id: int):
  with connect_to_db() as conn:
    result = conn.execute(
      """
      SELECT personnelId 
      FROM Personnel
      WHERE Personnel.memberId = ?;
      """, 
      (member_id,)
    ).fetchone()
    return result['personnelId'] if result is not None else None
  
def register_member_as_volunteer(member_id: int):
  """
  Signs up a member to be a volunteer.
  Step 1: Check if the member is already personnel. If they are, abort.
  Step 2: Register the member as a part of personnel.
  Step 3: Display the member's Personnel ID.
  """
  with connect_to_db() as conn:
    cursor = conn.cursor()
    
    if find_personnel_id_by_member_id(member_id) is not None:
      print(f"Error: Member with ID: {member_id} is already library personnel.")
      return
    
    cursor.execute(
      """
      INSERT INTO Personnel (memberId, role, dateJoined, salary) 
      VALUES (:memberId, "Volunteer", DATE(current_date, 'localtime'), NULL);
      """, 
      { 
       'memberId': member_id,
      }
    )
    
    personnel_id = cursor.lastrowid
    print(f'personnelId: {personnel_id}')
    if personnel_id is not None:
      print(f"✅ Member with ID: {member_id} successfully registered as a volunteer!\nTheir Personnel ID is: {personnel_id}. ")
    else:
      print(f"Error: Failed to register member {member_id} as a volunteer.")
