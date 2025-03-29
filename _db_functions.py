import sqlite3

from utils import *

from constants import DB_PATH


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
