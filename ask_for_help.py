

import sqlite3

from constants import DB_PATH
from utils import dict_row_factory



def get_answers_to_question(question_id: int) -> list[dict]:
  answers = []
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = dict_row_factory
  with conn:
    answers = conn.execute("""
      SELECT * 
      FROM HelpAnswerView
      WHERE questionId = ?; 
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
      FROM HelpQuestionView;                
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
