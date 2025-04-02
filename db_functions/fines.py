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
  
def get_all_outstanding_fines_list():
  with connect_to_db() as conn:
    cursor = conn.cursor()
    cursor.execute(
      """
      SELECT * 
      FROM OutstandingFinesView; 
      """
    )
    return cursor.fetchall()

def get_outstanding_fines_for_member(member_id: int):
  with connect_to_db() as conn:
    return conn.execute(
      """
      SELECT * 
      FROM OutstandingFinesView
      WHERE memberId = ?; 
      """, (member_id,)
    ).fetchall()

def get_members_outstanding_fines_balance(member_id: int):
  with connect_to_db() as conn:
    result: dict = conn.execute(
      """
      SELECT 
        SUM(balance) AS balance
      FROM OutstandingFinesView
      WHERE memberId = ?; 
      """, (member_id,)
    ).fetchone()
    if result is None: return 0.0
    balance = result.get('balance', 0.0)
    if balance is None:
      balance = 0.0
    return balance
