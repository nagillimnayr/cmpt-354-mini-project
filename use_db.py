from datetime import datetime

from db_functions import *

KEYWORDS = ['fnditm', 'finditem', 'brw', 'borrowitem', 'rtn', 'returnitem', 'dnt', 'donate', 'fndevt', 'findevent', 'reg', 'register', 'vlt', 'volunteer', 'qst', 'questions']



print ('Hello, are you a member (m) or librarian (l)?')
uInput = input('> ')
while not uInput in ['m', 'l']:
    uInput = input('Invalid entry (m or l) \n> ')
match uInput:
    case 'm':
        mId = input('Enter member Id\n> ')
        mIds = get_member_ids()
        print(mIds)
        while not mId in mIds:
            if not mId.isdigit(): mId = input('Invalid memberId, enter again\n> ')
            mId = input('Member Id not found, enter again\n> ')
        
        

print('How can I assist you? (type help for a list of commands)')

while uInput not in ['q', 'quit', 'kill']:
    
    uInput = input('> ').strip().lower()

    if len(uInput) == 0: continue

    sInput = uInput.split()

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
            'Ask Librarian:        -ask     -askhelp')
    
    # Check for input in db keywords
    if sInput[0] in KEYWORDS:
        match sInput[0]:
            case 'fnditm' | 'finditem':
                while True:
                    choice = input('Search by term (t) or by item Id (i): ')
                    match choice:
                        case 'b': break
                        case 't': 
                            sTerm = input('Search Term: ')
                            if sTerm == 'b': break

                            results = search_for_item(sTerm)
                            if len(results) == 0: print("No items found.")
                            else: 
                              print('\nItems found:\n')
                              print_items_list(results)
                        case 'i':
                            iId = input('Item Id: ')
                            if iId == 'b': break
                            
                            result = find_item_by_id(int(iId))
                            if result is None: print("No item found.")
                            else: print_item(result)
                            
                    con = input('Would you like to search for another item? (y/n): ').strip().lower()
                    if con == 'n': break
                    elif not con == 'y': con = input('Invalid entry (y/n): ').strip().lower()
            case 'brw' | 'borrowitem':
                while True:
                    mId = input('\nMember Id: ')
                    if mId == 'b': break 
                    while not mId.isdigit(): mId = input('\nInvalid memberId, enter again: ')

                    iId = input('Item Id: ')
                    if iId == 'b': break 
                    while not iId.isdigit(): itemId = input('\nInvalid itemId, enter again: ')

                    borrow_item(int(mId), int(iId))

                    con = input('Would you like to borrow another item? (y/n): ').strip().lower()
                    if con == 'n': break 
                    elif not con == 'y': con = input('Invalid entry (y/n): ').strip().lower()
            case 'rtn' | 'returnitem':
                while True:
                    itemId = input('Item Id: ')
                    if itemId == 'b': break 
                    while not itemId.isdigit(): itemId = input('\nInvalid itemId, enter again: ')

                    instanceId = input('Instance Id: ')
                    if instanceId == 'b': break 
                    while not instanceId.isdigit(): instanceId = input('\nInvalid itemId, enter again: ')

                    return_item(int(itemId), int(instanceId))

                    con = input('Would you like to return another item? (y/n): ').strip().lower()
                    if con == 'n': break 
                    elif not con == 'y': con = input('Invalid entry (y/n): ').strip().lower()
            case 'dnt' | 'donateitem':
                while True:
                    title = input('Title: ')
                    if title == 'b': break
                    while len(title) == 0: title = input('Invalid title: ')

                    author = input('Author: ')
                    if author == 'b': break
                    while len(author) == 0: author = input('Invalid author: ')

                    format = input('Format: ')
                    if format == 'b': break
                    while len(format) == 0: format = input('Invalid format: ')

                    description = input('Description: ')
                    if description == 'b': break
                    while len(description) == 0: description = input('Invalid description: ')
                        
                    publishDate = input('Publish Date (YYYY-MM-DD): ')
                    if publishDate == 'b': break
                    while len(publishDate) == 0: publishDate = input('Invalid publish date: ')
                    isValid = False
                    while not isValid:
                        try:
                            datetime.strptime(publishDate, '%Y-%m-%d')
                            break
                        except ValueError:
                            publishDate = input('Invalid publish date: ')

                    publisher = input('Publisher: ')
                    if publisher == 'b': break
                    while len(publisher) == 0: publisher = input('Invalid publisher: ') 

                    donate_item(title, author, format, description, publishDate, publisher)

                    con = input('Would you like to donate another item? (y/n): ').strip().lower()
                    if con == 'n': break 
                    elif not con == 'y': con = input('Invalid entry (y/n): ').strip().lower()
            case 'fndevt' | 'findevent':
                while True:
                    choice = input('Search by term (t) or by item Id (i): ')
                    match choice:
                        case 'b': break
                        case 't': 
                            sTerm = input('Search Term: ')
                            if sTerm == 'b': break

                            search_for_event(sTerm)
                        case 'i':
                            eId = input('Event Id: ')
                            if eId == 'b': break
                            
                            find_event_by_id(int(eId))
                    con = input('Would you like to search for another event? (y/n): ').strip().lower()
                    if con == 'n': break 
                    elif not con == 'y': con = input('Invalid entry (y/n): ').strip().lower()  
            case 'reg' | 'register':
                while True:
                    mId = input('Member Id: ')
                    if mId == 'b': break 
                    while not mId.isdigit(): mId = input('\nInvalid memberId, enter again: ')

                    eId = input('Event Id: ')
                    if eId == 'b': break
                    while not eId.isdigit(): eId = input('\nInvalid eventId, enter again: ')

                    register_for_event(int(mId), int(eId))

                    con = input('Would you like to search for another event? (y/n): ').strip().lower()
                    if con == 'n': break 
                    elif not con == 'y': con = input('Invalid entry (y/n): ').strip().lower()
            case 'vlt' | 'volunteer':
                while True:
                    mId = input('Member Id: ')
                    if mId == 'b': break
                    while not mId.isdigit(): mId = input('\nInvalid memberId, enter again: ')

                    register_member_as_volunteer(int(mId))

                    con = input('Would you like to register another member? (y/n): ').strip().lower()
                    if con == 'n': break 
                    elif not con == 'y': con = input('Invalid entry (y/n): ').strip().lower()
            case 'qst' | 'questions':
                while True:
                    print('See questions (q),\n'
                    'see all questions & answers (qa),\n'
                    'see answers to specific question (sq),\n'
                    'post question (p)\n'
                    'answer question (aq)\n')

                    choice = input('Enter choice: ')
                    match choice:
                        case 'q':
                            questions = get_questions()
                        case 'qa':
                            questionsAndAnswers = get_questions_with_answers()
                        case 'sq':
                            qId = input('Question Id: ')
                            if (qId == 'b'): break
                            while not qId.isdigit(): qId = input('Invalid questionId, enter again: ')

                            answers = get_answers_to_question(qId)        
                        case 'p':
                            mId = input('Member Id: ')
                            if (mId == 'b'): break
                            while not mId.isdigit(): mId = input('Invalid memberId, enter again: ')

                            question = input("Question to post: ")
                            if (question == 'b'): break
                            while len(question) == 0: question = input("Blank question, enter again: ")

                            post_question(mId, question)
                        case 'aq':
                            qId = input('Question Id: ')
                            if (qId == 'b'): break
                            while not qId.isdigit(): qId = input('Invalid questionId, enter again: ')

                            pId = input('Personnel Id: ')
                            if (pId == 'b'): break
                            while not pId.isdigit(): pId = input('Invalid personnelId, enter again: ')

                            answer = input("Answer to post: ")
                            if (answer == 'b'): break
                            while len(answer) == 0: answer = input("Blank answer, enter again: ")

                            post_answer(qId, pId, answer)
            case _:
                print('base case')

print('Exiting...')
