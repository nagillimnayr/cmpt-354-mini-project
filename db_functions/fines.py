import sqlite3
from constants import *
from utils import *

def get_all_fines_list():
  with connect_to_db() as conn:
    cursor = conn.cursor()
    cursor.execute(
      """
      SELECT * 
      FROM OverdueFine; 
      """
    )
    return cursor.fetchall()
  

def get_outstanding_fines_for_member(member_id: int):
  with connect_to_db() as conn:
    cursor = conn.cursor()
    cursor.execute(
      """
      SELECT * 
      FROM OutstandingFinesView
      WHERE OutstandingFinesView.memberId = ?; 
      """, (member_id,)
    )
    return cursor.fetchall()
  
