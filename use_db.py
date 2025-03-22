import db_functions
from datetime import datetime

KEYWORDS = ['fnditm', 'finditem', 'brw', 'borrowitem', 'rtn', 'returnitem', 'dnt', 'donate', 'fndevt', 'findevent', 'reg', 'register', 'vlt', 'volunteer', 'ask', 'askhelp']

uInput = ''

print('Hello, how can I assist you? (type help for a list of commands)')

while uInput not in ['q', 'quit', 'kill']:
    uInput = input('\nEnter Input: ').strip().lower()

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
                case 'ask' | 'askhelp':
                    print('Description: ask a librarian for help')
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
                print('Foo')
            case 'brw' | 'borrowitem':
                mId = input('\nMember Id: ')
                if mId == 'b': continue 
                while not mId.isdigit(): mId = input('\nInvalid memberId, enter again: ')

                iId = input('Item Id: ')
                if iId == 'b': continue 
                while not iId.isdigit(): itemId = input('\nInvalid itemId, enter again: ')

                lId = input('Librarian Id: ')
                if lId == 'b': continue 
                while not lId.isdigit(): lId = input('\nInvalid librarianId, enter again: ')

                db_functions.borrow_item(mId, iId, lId)
            case 'rtn' | 'returnitem':
                itemId = input('Item Id: ')
                if itemId == 'b': continue 
                while not itemId.isdigit(): itemId = input('\nInvalid itemId, enter again: ')

                instanceId = input('Instance Id: ')
                if instanceId == 'b': continue 
                while not instanceId.isdigit(): instanceId = input('\nInvalid itemId, enter again: ')

                db_functions.return_item(itemId, instanceId)
            case 'dnt' | 'donateitem':
                title = input('Title: ')
                if title == 'b': continue
                while len(title) == 0: title = input('Invalid title: ')

                author = input('Author: ')
                if author == 'b': continue
                while len(author) == 0: author = input('Invalid author: ')

                format = input('Format: ')
                if format == 'b': continue
                while len(format) == 0: format = input('Invalid format: ')

                description = input('Description: ')
                if description == 'b': continue
                while len(description) == 0: description = input('Invalid description: ')
                    
                publishDate = input('Publish Date (YYYY-MM-DD): ')
                if publishDate == 'b': continue
                while len(publishDate) == 0: publishDate = input('Invalid publish date: ')
                isValid = False
                while not isValid:
                    try:
                        datetime.strptime(publishDate, '%Y-%m-%d')
                        break
                    except ValueError:
                        publishDate = input('Invalid publish date: ')

                publisher = input('Publisher: ')
                if publisher == 'b': continue
                while len(publisher) == 0: publisher = input('Invalid publisher: ') 

                db_functions.donate_item(title, author, format, description, publishDate, publisher)
            case 'fndevt' | 'findevent':
                print('Foo')
            case 'reg' | 'register':
                print('Foo')
            case 'vlt' | 'volunteer':
                print('Foo')
            case 'ask' | 'askhelp':
                print('Foo')
            case _:
                print('base case')

print('Exiting...')

