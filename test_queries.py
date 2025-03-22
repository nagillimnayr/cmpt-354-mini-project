import sqlite3

from db_functions import *


def test_queries():
  post_question(10, "Hello, Question!")
  post_answer(5, 1, "Hello, Answer!")
  
  questions = get_questions_with_answers()
  pretty_print(questions)


if __name__ == '__main__':
  test_queries()
