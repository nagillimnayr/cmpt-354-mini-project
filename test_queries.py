import sqlite3

from db_functions import *


def test_queries():
  # post_question(10, "Hello, Question!")
  # post_answer(5, 1, "Hello, Answer!")
  
  # questions = get_questions_with_answers()
  # pretty_print(questions)
  try:
    with sqlite3.connect('library.db') as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT instanceId, itemId FROM ItemInstance WHERE currentCheckoutId IS NULL; ")
      result = cursor.fetchall()
      print(result)
  except sqlite3.Error as e:
        print(f"Database error: {e}")


if __name__ == '__main__':
  test_queries()
