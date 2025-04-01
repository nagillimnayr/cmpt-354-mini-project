from datetime import datetime

from db_functions import *
from cli import *

MID = -1
PID = -1

QUIT_COMMANDS = ['q', 'quit', 'exit', 'kill']

print ('Hello, are you a member (m) or personnel (p)?')
uInput = input('> ').strip().lower()
while not uInput in ['m', 'p']: uInput = input('Invalid entry (m or p) \n> ').strip().lower()
match uInput:
    case 'm':
        while True:
            mId = input('Enter Member ID:\n> ')
            if mId in QUIT_COMMANDS:
                print('Exiting...')
                exit(0)
            if not mId.isdigit(): 
                print('Invalid Member ID, enter again\n')
                continue
            mId = int(mId)

            member = get_member(mId)
            if member is None:
                print(f'Member with ID: {mId} not found, please enter again\n')
                continue

            MID = mId
            name = member['firstName'] + ' ' + member['lastName']
            print('\nHello,', name)
            break;
    case 'p':
        is_valid = False
        while True:
            pId = input('Enter Personnel ID\n> ')
            if pId in QUIT_COMMANDS:
                print('Exiting...')
                exit(0)
            if not pId.isdigit(): 
                print('Invalid Personnel ID, enter again\n')
                continue
            pId = int(pId)
        
            personnel = get_personnel(pId)
            if personnel is None:
                print(f'Personnel with ID: {pId} not found, please enter again\n')
                continue
            PID = personnel['personnelId']
            MID = personnel['memberId']
            name = personnel['firstName'] + ' ' + personnel['lastName']
            print('\nHello,', name)
            break
        
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
            handle_find_item(member_id=MID)
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
                    
                    mId = MID
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
                while True:
                    print(
                        'see all questions & answers (qa),\n'
                        'see answers to specific question (sq),\n'
                        'post question (pq)\n'
                        'answer question (aq)\n')

                    choice = input('Enter choice: ')
                    match choice:
                        case 'q': break
                        case 'qa':
                            questionsAndAnswers = get_questions_with_answers()
                            labels = [
                                ('questionId', 'QID'),
                                ('memberId', 'MID'),
                                ('question', 'Question'),
                                ('datePublished', 'Date'),
                                ('firstName', 'First Name'),
                                ('lastName', 'Last Name'),
                                ('answers', 'Answers')
                            ]
                            pretty_print(questionsAndAnswers)
                        case 'sq':
                            qId = input('Question ID: ')
                            if (qId == 'b'): break
                            while not qId.isdigit(): qId = input('Invalid questionId, enter again: ')

                            answers = get_answers_to_question(int(qId))  
                            pretty_print(answers)      
                        case 'pst':
                            mId = MID
                            question = input("Question to post: ")
                            if (question == 'b'): break
                            while len(question) == 0: question = input("Blank question, enter again: ")

                            post_question(int(mId), question)
                        case 'aq':
                            if PID == -1: 
                                print('Error, only library personnel can answer questions')
                                break

                            qId = input('Question ID: ')
                            if (qId == 'b'): break
                            while not qId.isdigit(): qId = input('Invalid questionId, enter again: ')
                            
                            pId = PID

                            answer = input("Answer to post: ")
                            if (answer == 'b'): break
                            while len(answer) == 0: answer = input("Blank answer, enter again: ")

                            post_answer(int(qId), int(pId), answer)

                    con = input('Would you like to interact with the forum again? (y/n)\n>').strip().lower()
                    while con not in ['y', 'n']:
                        con = input('Invalid entry\n>').strip().lower()
                    if con == 'n': break    
        case _:
            print('Unrecognized command. Type `help` for a list of commands.')


print('Exiting...')
