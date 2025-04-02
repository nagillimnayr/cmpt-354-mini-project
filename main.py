from datetime import datetime

from cli.qa_forum import handle_qa_forum
from db_functions import *
from cli import *
from constants import *

MID = -1
PID = -1

def main():
    mId, pId = handle_login()
    print('How can I assist you? (type help for a list of commands)')
    while True:
        uInput = input('\nEnter input:\n> ').strip().lower()
        if len(uInput) == 0: continue
        sInput = uInput.split()

        if uInput in QUIT_COMMANDS:
            break
        
        # Check for input in help keywords
        if sInput[0] in ['h', 'help']:
            if len(sInput) > 1:
                match sInput[1]:
                    case 'fnditm' | 'finditem':
                        print('Description: search for item either by keyword(s) or itemId')
                    case 'brw' | 'borrowitem':
                        print('Description: checkout item from the library')
                    case 'rtn' | 'returnitem':
                        print('Description: return a previously checked out item to the library')
                    case 'dnt' | 'donateitem':
                        print('Description: donate an item to the library`s collection')
                    case 'fndevt' | 'findevent':
                        print('Description: search for an event by title, type, date, or recommended audience')
                    case 'reg' | 'register':
                        print('Description: register to attend a specific event by eventId')
                    case 'vlt' | 'volunteer':
                        print('Description: volunteer to become a librarian')
                    case 'qst' | 'questions':
                        print('Description: see question board/post a question')
                    case _:
                        print('Unrecognized Command')
            else:
                print('For more information on a specific COMMAND, type help COMMAND-NAME\n'
                'Find Item:            -fnditm, -finditem\n'
                'Borrow Item:          -brw,    -borrowitem\n'
                'Return Item:          -rtn,    -returnitem\n'
                'Donate Item:          -dnt,    -donate\n'
                'Find Event:           -fndevt  -findevent\n'
                'Register Event:       -reg     -register\n'
                'Volunteer:            -vlt     -volunteer\n'
                'Ask Librarian:        -qst     -question')
            continue
        
        match sInput[0]:
            case 'fnditm' | 'finditem':
                handle_find_item(member_id=mId)
            case 'brw' | 'borrowitem':
                    while True:
                        mId = MID
                        iId = input('Item ID: ')
                        if iId == 'b': break 
                        while not iId.isdigit(): itemId = input('\nInvalid itemId, enter again: ')

                        borrow_item(int(mId), int(iId))

                        con = input('Would you like to borrow another item? (y/n)\n>').strip().lower()
                        while con not in ['y', 'n']:
                            con = input('Invalid entry\n>').strip().lower()
                        if con == 'n': break 
            case 'rtn' | 'returnitem':
                    while True:
                        itemId = input('Item ID: ')
                        if itemId == 'b': break 
                        while not itemId.isdigit(): itemId = input('\nInvalid itemId, enter again: ')

                        instanceId = input('Instance ID: ')
                        if instanceId == 'b': break 
                        while not instanceId.isdigit(): instanceId = input('\nInvalid itemId, enter again: ')

                        return_item(int(itemId), int(instanceId))

                        con = input('Would you like to return another item? (y/n)\n>').strip().lower()
                        while choice not in ['y', 'n']:
                            choice = input('Invalid entry\n>').strip().lower()
                        if con == 'n': break 
            case 'dnt' | 'donateitem':
                    while True:
                        title = input('Title:\n>')
                        if title == 'b': break
                        while len(title) == 0: title = input('Invalid title\n>')

                        author = input('Author:\n>')
                        if author == 'b': break
                        while len(author) == 0: author = input('Invalid author\n>')

                        format = input('Format:\n>')
                        if format == 'b': break
                        while len(format) == 0: format = input('Invalid format\n>')

                        description = input('Description:\n>')
                        if description == 'b': break
                        while len(description) == 0: description = input('Invalid description\n>')
                            
                        publishDate = input('Publish Date (YYYY-MM-DD):\n>')
                        if publishDate == 'b': break
                        while len(publishDate) == 0: publishDate = input('Invalid publish date\n>')
                        isValid = False
                        while not isValid:
                            try:
                                datetime.strptime(publishDate, '%Y-%m-%d')
                                break
                            except ValueError:
                                publishDate = input('Invalid publish date\n>')

                        publisher = input('Publisher:\n>')
                        if publisher == 'b': break
                        while len(publisher) == 0: publisher = input('Invalid publisher\n>') 

                        donate_item(title, author, format, description, publishDate, publisher)

                        con = input('Would you like to donate another item? (y/n)\n>').strip().lower()
                        while con not in ['y', 'n']:
                            con = input('Invalid entry\n>').strip().lower()
                        if con == 'n': break  
            case 'fndevt' | 'findevent':
                    while True:
                        choice = input('Search by term (t) or by item ID (i)\n>').strip().lower()
                        match choice:
                            case 'b': break
                            case 't': 
                                sTerm = input('Search Term: ').strip()
                                if sTerm == 'b': break

                                search_for_event(sTerm)
                            case 'i':
                                eId = input('Event ID: ').strip().lower()
                                if eId == 'b': break
                                while not eId.isdigit(): eId = input('\nInvalid eventId, enter again\n>').strip()

                                find_event_by_id(int(eId))
                        con = input('Would you like to search for another event? (y/n)\n>').strip().lower()
                        while con not in ['y', 'n']:
                            con = input('Invalid entry\n>').strip().lower()
                        if con == 'n': break  
            case 'reg' | 'register':
                    while True:
                        choice = input('Would you like to see a list of all events? (y/n)\n>').strip().lower()
                        while choice not in ['y', 'n']:
                            choice = input('Invalid entry\n>').strip().lower()
                        if choice == 'y':
                            display_events()
                        
                        eId = input('Event ID: ').strip()
                        if eId == 'b': break
                        while not eId.isdigit(): eId = input('\nInvalid eventId, enter again: ').strip()
                        register_for_event(int(mId), int(eId))

                        con = input('Would you like to register for another event? (y/n)\n>').strip().lower()
                        while con not in ['y', 'n']:
                            con = input('Invalid entry\n>').strip().lower()
                        if con == 'n': break  
            case 'vlt' | 'volunteer':
                    mId = MID
                    register_member_as_volunteer(int(mId))
            case 'qst' | 'questions':
                handle_qa_forum(mId, pId)
            case _:
                print('Unrecognized command. Type `help` for a list of commands.')


    print('Exiting...')

if __name__ == '__main__':
    main()
