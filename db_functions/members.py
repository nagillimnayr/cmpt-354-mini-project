import sqlite3
from constants import *
from utils import *

def get_members_list():
  with connect_to_db() as conn:
    return conn.execute(
      """
      SELECT * 
      FROM Member; 
      """
    ).fetchall()

def get_member_ids():
    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
          SELECT memberId
          FROM Member;
        """)

        rows = cursor.fetchall()
        return [row[0] for row in rows]

def format_member(member: dict):
  """
  Formats a member into a string for printing.
  """
  
  return '\n'.join([
    f"Name: {member.get('firstName')} {member.get('lastName')}",
    f"ID: {member.get('memberId')}",
    f"Date of Birth: {member.get('dateOfBirth')}",
    f"Phone Number: {member.get('phoneNumber')}",
  ])

def print_members_list():
  """
  Prints a list of all members.
  """
  members = get_members_list()
  if len(members) == 0:
    print("No members found.")
    return
      
  for member_str in [format_member(member) for member in members]:
    print(member_str, end='\n\n')
