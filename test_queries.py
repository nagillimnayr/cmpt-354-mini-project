import sqlite3

from ask_for_help import list_answers_to_question, list_questions
from borrow_item import *
from reset import drop_views
from return_item import *
from donate_item import *
from find_event import *
from register_for_event import *
from constants import *
from find_item import *
from volunteer import *


def test_queries():
  # find_item_by_id(6)
  # register_member_as_volunteer(11)
  # list_questions()
  list_answers_to_question(2)
  # drop_views()


if __name__ == '__main__':
  test_queries()
