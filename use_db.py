import db_functions

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
        isContinue = False
        match sInput[0]:
            case 'fnditm' | 'finditem':
                print('Foo')
            case 'brw' | 'borrowitem':
                mId = input('\nMember ID: ')
                while not mId.isdigit():
                    if mId == 'b': 
                        isContinue = True
                        break
                    mId = input('\nInvalid mId, enter again: ')
                if isContinue: continue 

                itemId = input('Item ID: ')
                while not itemId.isdigit():
                    if itemId == 'b': 
                        isContinue = True
                        break
                    itemId = input('\nInvalid itemId, enter again: ')
                if isContinue: continue 

                lId = input('Librarian ID: ')
                while not lId.isdigit():
                    if lId == 'b': 
                        isContinue = True
                        break
                    lId = input('\nInvalid lId, enter again: ')
                if isContinue: continue 

                db_functions.borrow_item(mId, itemId, lId)
            case 'rtn' | 'returnitem':
                print('Foo')
            case 'dnt' | 'donateitem':
                print('Foo')
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

