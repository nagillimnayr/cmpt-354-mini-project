import sqlite3
from constants import *
from utils import *

def get_members_list():
  with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = dict_row_factory
    cursor = conn.cursor()
    cursor.execute("""
      SELECT * 
      FROM Member; 
    """)
    
    return cursor.fetchall()


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
      
  for member_str in [format(member) for member in members]:
    print(member_str, end='\n\n')
