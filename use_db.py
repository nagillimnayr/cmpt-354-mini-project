from datetime import datetime

from db_functions import *

MID = -1
PID = -1

print ('Hello, are you a member (m) or personnel (p)?')
uInput = input('> ').lower()
while not uInput in ['m', 'p']: uInput = input('Invalid entry (m or p) \n> ').lower()
match uInput:
    case 'm':
        mId = input('Enter member Id\n> ')
        while not mId.isdigit(): mId = input('Invalid memberId, enter again\n> ')
        mId = int(mId)

        members = get_members_list()
        mIds = [m['memberId'] for m in members]
        while mId not in mIds:
            mId = input('Member Id not found, enter again\n> ')
        MID = mId
        mName = [m for m in members if m['memberId'] == mId]
        mName = mName[0]['firstName'] + ' ' + mName[0]['lastName']
        print('\nHello,', mName)
    case 'p':
        pId = input('Enter personnel Id\n> ')
        while not pId.isdigit(): pId = input('Invalid personnelId, enter again\n> ')
        pId = int(pId)

        personnel = get_personnel_ids()
        pIds = [p['personnelId'] for p in personnel] 
        while pId not in pIds:
            pId = input('Personnel Id not found, enter again\n> ')
        PID = pId
        pMemId = [p['memberId'] for p in personnel if p['personnelId'] == pId]
        MID = pMemId[0]
        pName = get_member_name_by_id(int(pMemId[0]))
        pName = pName['firstName'] + ' ' + pName['lastName']
        print('\nHello,', pName)
        
print('How can I assist you? (type help for a list of commands)')

while uInput not in ['q', 'quit', 'kill']:
    uInput = input('\nEnter input\n> ').strip().lower()
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
            'Ask Librarian:        -qst     -question')

    match sInput[0]:
        case 'fnditm' | 'finditem':
                while True:
                    choice = input('Search by term (t) or by item Id (i): ')
                    match choice:
                        case 'b': break
                        case 't': 
                            sTerm = input('Search Term: ')
                            if sTerm == 'b': break
                            filters = [
                                'title',
                                'author',
                            ]
                            results = search_for_items(sTerm, filters)
                            if len(results) == 0: print("No items found.")
                            else: 
                              print('\nItems found:\n')
                              print_item_list_view(results)
                        case 'i':
                            iId = input('Item Id: ')
                            if iId == 'b': break
                            
                            result = find_item_by_id(int(iId))
                            if result is None: print("No item found.")
                            else: print_item(result)
                            
                    con = input('Would you like to search for another item? (y/n)\n>').strip().lower()
                    while con not in ['y', 'n']:
                        con = input('Invalid entry\n>').strip().lower()
                    if con == 'n': break 
        case 'brw' | 'borrowitem':
                while True:
                    mId = MID
                    iId = input('Item Id: ')
                    if iId == 'b': break 
                    while not iId.isdigit(): itemId = input('\nInvalid itemId, enter again: ')

                    borrow_item(int(mId), int(iId))

                    con = input('Would you like to borrow another item? (y/n)\n>').strip().lower()
                    while con not in ['y', 'n']:
                        con = input('Invalid entry\n>').strip().lower()
                    if con == 'n': break 
        case 'rtn' | 'returnitem':
                while True:
                    itemId = input('Item Id: ')
                    if itemId == 'b': break 
                    while not itemId.isdigit(): itemId = input('\nInvalid itemId, enter again: ')

                    instanceId = input('Instance Id: ')
                    if instanceId == 'b': break 
                    while not instanceId.isdigit(): instanceId = input('\nInvalid itemId, enter again: ')

                    return_item(int(itemId), int(instanceId))

                    con = input('Would you like to return another item? (y/n)\n>').strip().lower()
                    while choice not in ['y', 'n']:
                        choice = input('Invalid entry\n>').strip().lower()
                    if con == 'n': break 
        case 'dnt' | 'donateitem':
                while True:
                    title = input('Title\n>')
                    if title == 'b': break
                    while len(title) == 0: title = input('Invalid title\n>')

                    author = input('Author\n>')
                    if author == 'b': break
                    while len(author) == 0: author = input('Invalid author\n>')

                    format = input('Format\n>')
                    if format == 'b': break
                    while len(format) == 0: format = input('Invalid format\n>')

                    description = input('Description\n>')
                    if description == 'b': break
                    while len(description) == 0: description = input('Invalid description\n>')
                        
                    publishDate = input('Publish Date (YYYY-MM-DD)\n>')
                    if publishDate == 'b': break
                    while len(publishDate) == 0: publishDate = input('Invalid publish date\n>')
                    isValid = False
                    while not isValid:
                        try:
                            datetime.strptime(publishDate, '%Y-%m-%d')
                            break
                        except ValueError:
                            publishDate = input('Invalid publish date\n>')

                    publisher = input('Publisher\n>')
                    if publisher == 'b': break
                    while len(publisher) == 0: publisher = input('Invalid publisher\n>') 

                    donate_item(title, author, format, description, publishDate, publisher)

                    con = input('Would you like to donate another item? (y/n)\n>').strip().lower()
                    while con not in ['y', 'n']:
                        con = input('Invalid entry\n>').strip().lower()
                    if con == 'n': break  
        case 'fndevt' | 'findevent':
                while True:
                    choice = input('Search by term (t) or by item Id (i)\n>').strip().lower()
                    match choice:
                        case 'b': break
                        case 't': 
                            sTerm = input('Search Term: ').strip()
                            if sTerm == 'b': break

                            search_for_event(sTerm)
                        case 'i':
                            eId = input('Event Id: ').strip().lower()
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
                    eId = input('Event Id: ').strip()
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
                            qId = input('Question Id: ')
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

                            qId = input('Question Id: ')
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
