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
    ('dateTimeStart', 'Start Time'),
    ('dateTimeEnd', 'End Time'),
    ('roomName', 'Room'),
    ('audienceType', 'Suggested Audience'),
  ])
  
def print_event_details(eId: int):
  event = find_event_by_id(int(eId))
  if event is None: 
    print("No event found.")
    return 
  
  print('\n' + "\n".join([
    f"Event ID: {event['eventId']}",
    f"Title: {event['title']}",
    f"Type: {event['type']}",
    f"Start Time: {event['dateTimeStart']}",
    f"End Time: {event['dateTimeEnd']}",
    f"Room ID: {event['roomId']}",
    f"Room Name: {event['roomName']}",
    f"Description: {event['description']}",
  ]) + '\n')

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
            print_event_details(int(eId))
    con = input('Would you like to search for another event? (y/n)\n>').strip().lower()
    while con not in ['y', 'n']:
        con = input('Invalid entry\n>').strip().lower()
    if con == 'n': return  
