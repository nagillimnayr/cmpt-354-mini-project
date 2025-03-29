import sqlite3
from constants import *
from utils import *


def get_answers_to_question(question_id: int) -> list[dict]:
  with connect_to_db() as conn:
    return conn.execute("""
      SELECT * 
      FROM HelpAnswerView
      WHERE questionId = ?
      ORDER BY datePublished ASC;  
    """, (question_id,)).fetchall()
  
def get_questions() -> list[dict]:
  with connect_to_db() as conn:
    return conn.execute("""
      SELECT * 
      FROM HelpQuestionView
      ORDER BY datePublished ASC;                
    """).fetchall()
  
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
  try:
    with connect_to_db() as conn:
      conn.execute("""
        INSERT INTO HelpQuestion (
          memberId, 
          question, 
          datePublished
        ) VALUES (:member_id, :question, DATE(current_date, 'localtime'));
      """, {
        'member_id': member_id,
        'question': question,
      })
  except sqlite3.Error as e:
    print(f"Database error: {e}")
  else:
    print(f"✅ Uploaded question: {question}")
    
def post_answer(question_id:int, personnel_id: int, answer: str):
  try:
    with connect_to_db() as conn:
      conn.execute("""
        INSERT INTO HelpAnswer (
          questionId,
          personnelId, 
          answer, 
          datePublished
        ) VALUES (:question_id, :personnel_id, :answer, DATE(current_date, 'localtime'));
      """, {
        'question_id': question_id,
        'personnel_id': personnel_id,
        'answer': answer,
      })
  except sqlite3.Error as e:
    print(f"Database error: {e}")
  else:
    print(f"✅ Uploaded answer: {answer}")
