

import sqlite3

from constants import DB_PATH
from utils import dict_row_factory, pretty_print


def list_questions():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = dict_row_factory
  with conn:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT * 
      FROM HelpQuestionView;                
    """)
    questions = cursor.fetchall()
    pretty_print(questions)
  conn.close()

def list_answers_to_question(question_id: int):
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = dict_row_factory
  with conn:
    answers = conn.execute("""
      SELECT * 
      FROM HelpAnswerView
      WHERE questionId = ?; 
    """, (question_id,)).fetchall()
    pretty_print(answers)
  conn.close()
  