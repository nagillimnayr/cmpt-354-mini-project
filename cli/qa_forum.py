from db_functions import *
from constants import *


def print_question_with_answers(qwa):
  print("\n".join([
    f"Question ID: {qwa['questionId']}",
    f"Member ID: {qwa['memberId']}",
    f"Member: {qwa['firstName']} {qwa['lastName']}",
    f"Date Posted: {qwa['datePublished']}",
    f"Question: {qwa['question']}",
    # f": {qwa['']}"
  ]))
  answers = []
  for ans in qwa['answers']:
    answers.append('\n'.join([(" " * 4) + line for line in [
      f"Answer ID: {ans['answerId']}",
      f"Personnel ID: {ans['personnelId']}",
      f"Personnel: {ans['firstName']} {ans['lastName']}",
      f"Role: {ans['role']}",
      f"Date Posted: {ans['datePublished']}",
      f"Answer: {ans['answer']}",
      # f": {ans['']}",
    ]]))

  if len(answers) > 0:
    print('\n\n'.join(answers))
  print()

def handle_qa_forum(mId: int, pId: int | None):
  qa_forum_menu_options = [
    '(qa) See all questions & answers',
    '(sq) See answers to a specific question',
    '(pq) Post a question',
  ]
  if pId is not None:
    qa_forum_menu_options.append('(aq) Answer question')
  qa_forum_menu = '\n'.join(qa_forum_menu_options) 
  qa_forum_menu_header = '\n' + '\n'.join([
    '---------------------------------------------------------',
    '----------------------- Q&A Forum -----------------------',
    '---------------------------------------------------------',
  ])  
  while True:
    print(qa_forum_menu_header)
    print(qa_forum_menu)

    choice = input('\nEnter choice: ')
    match choice:
        case 'b': return
        case 'qa':
            questions_and_answers = get_questions_with_answers()
            for qwa in questions_and_answers:
              print_question_with_answers(qwa)
            # pretty_print(questions_and_answers)
        case 'sq':
            qId = input('Question ID: ')
            if (qId == 'b'): return
            while not qId.isdigit(): qId = input('Invalid questionId, enter again: ')

            answers = get_answers_to_question(int(qId))  
            pretty_print(answers)      
        case 'pq':
            question = input("Question to post: ")
            if (question == 'b'): return
            while len(question) == 0: question = input("Blank question, enter again: ")

            post_question(mId, question)
        case 'aq':
            if pId is None: 
                print('Error, only library personnel can answer questions.')
                break

            qId = input('Question ID: ')
            if (qId == 'b'): return
            while not qId.isdigit(): qId = input('Invalid questionId, enter again: ')
            
            answer = input("Answer to post: ")
            if (answer == 'b'): return
            while len(answer) == 0: answer = input("Blank answer, enter again: ")

            post_answer(int(qId), int(pId), answer)
        
        case _:
            print('Unrecognized command.')
            continue
        
    con = input('Would you like to interact with the forum again? (y/n)\n>').strip().lower()
    while con not in ['y', 'n']:
        con = input('Invalid entry\n>').strip().lower()
    if con == 'n': return   
