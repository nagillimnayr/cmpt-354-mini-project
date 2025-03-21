import sqlite3

from ask_for_help import *
from borrow_item import *
from return_item import *
from donate_item import *
from find_event import *
from register_for_event import *
from constants import *
from find_item import *
from volunteer import *


def test_queries():
  post_question(10, "Hello, Question!")
  post_answer(5, 1, "Hello, Answer!")
  
  questions = get_questions_with_answers()
  pretty_print(questions)


if __name__ == '__main__':
  test_queries()
