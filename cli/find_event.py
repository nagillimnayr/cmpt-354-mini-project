from db_functions import *
from constants import *


def handle_event_search(sTerm: str):
  events = search_for_event(sTerm)
  if events is None or len(events) == 0:
    print("No events found.")
    return
  
  print_table_list(events, [
    ('eventId', 'Event ID'),
    ('title', 'Title'),
    ('type', 'Type'),
    ('dateTimeStart', 'Start'),
    ('dateTimeEnd', 'End'),
    ('roomName', 'Room'),
    ('audienceType', 'Suggested Audience'),
  ])

def handle_find_event():
  while True:
    choice = input('Search by term (t) or by event ID (i)\n>').strip().lower()
    match choice:
      case 'b': break
      case 't': 
          sTerm = input('Search Term: ').strip()
          handle_event_search(sTerm)
      case 'i':
        while True:
          eId = input('Event ID: ').strip().lower()
          if eId == 'b': return
          if not eId.isdigit(): 
            print('\nInvalid event ID, enter again\n')
          else:
            find_event_by_id(int(eId))
            break
    con = input('Would you like to search for another event? (y/n)\n>').strip().lower()
    while con not in ['y', 'n']:
        con = input('Invalid entry\n>').strip().lower()
    if con == 'n': return  
