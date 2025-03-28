import sqlite3
import os

from constants import DB_PATH


TABLES = [
  'Audience',
  'CheckoutRecord',
  'Event',
  'EventAttendance',
  'EventRecommendation',
  'HelpAnswer',
  'HelpQuestion',
  'Item',
  'ItemInstance',
  'Member',
  'MemberAudienceType',
  'OverdueFine',
  'Personnel',
  'SocialRoom',
]
DROP_TABLE_COMMANDS = ["DROP TABLE IF EXISTS " + table + ";" for table in TABLES]

def drop_tables():
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    for cmd in DROP_TABLE_COMMANDS:
      cursor.execute(cmd)

VIEWS = [
  'HelpAnswerView',
  'HelpQuestionView',
  'PersonnelInfo',
  'PersonnelView',
]   
DROP_VIEW_COMMANDS = ["DROP VIEW IF EXISTS " + view + ";" for view in VIEWS]

def drop_views():
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    for cmd in DROP_VIEW_COMMANDS:
      cursor.execute(cmd)

def drop_all():
  drop_tables()    
  # drop_views()
  

def execute_sql_in_directory(dir_name: str):
  """
  Reads all .sql files from a directory and executes the commands within.
  """
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    files = os.listdir(dir_name)
    for file_name in files:
      with open(f'{dir_name}/{file_name}') as file:
        command = file.read()
        cursor.execute(command)


def create_tables():
  """ 
  Reads in SQL commands from files in schemas folder and executes them. 
  """
  execute_sql_in_directory('schemas')
    
    
def create_views():
    execute_sql_in_directory('views')


def create_triggers():
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    """
    We can't use subqueries inside `CHECK` or `ASSERTION` statements, so we must
    use a `TRIGGER` to impose constraint on number of `OverdueFine`s for a single
    `CheckoutRecord`.
    """
    cursor.execute("""
      CREATE TRIGGER IF NOT EXISTS max_overdue_fines_per_checkout 
      BEFORE INSERT ON OverdueFine 
      WHEN (
          SELECT COUNT(*)
          FROM OverdueFine AS O
          WHERE O.checkoutId = NEW.checkoutId
        ) >= 10
      BEGIN
          SELECT 
          RAISE (ABORT, 'Maximum number of fines reached for this Checkout');
      END;
      """
    )
    
    """
    Trigger to prevent checking out an `ItemInstance` that is already
    checked out.
    """
    cursor.execute("""
      CREATE TRIGGER IF NOT EXISTS prevent_checkout_of_checked_out_item_instance 
      BEFORE INSERT ON CheckoutRecord
      WHEN (
        SELECT currentCheckoutId 
        FROM ItemInstance
        WHERE 
          itemId = NEW.itemId 
          AND
          instanceId = NEW.instanceId
      ) IS NOT NULL
      BEGIN 
        SELECT 
        RAISE (ABORT, 'ItemInstance is already checked out');
      END;
    """)
    
    """ 
    Trigger to set `currentCheckoutId` for `ItemInstance` when a new 
    `CheckoutRecord` is inserted.
    """
    cursor.execute("""
      CREATE TRIGGER IF NOT EXISTS set_current_checkout_id 
      AFTER INSERT ON CheckoutRecord
      WHEN (
        SELECT currentCheckoutId 
        FROM ItemInstance
        WHERE 
          itemId = NEW.itemId 
          AND
          instanceId = NEW.instanceId
      ) IS NULL
      BEGIN 
        UPDATE ItemInstance
        SET currentCheckoutId = NEW.checkoutId
        WHERE 
          itemId = NEW.itemId 
          AND
          instanceId = NEW.instanceId;
      END;
    """)
    
    """
    Trigger to set `ItemInstance`'s `currentCheckoutRecord` to `NULL` when an 
    item is returned. 
    """
    cursor.execute("""
      CREATE TRIGGER IF NOT EXISTS nullify_current_checkout_id 
      AFTER UPDATE ON CheckoutRecord
      WHEN 
        NEW.returnDate IS NOT NULL
      BEGIN 
        UPDATE ItemInstance
        SET currentCheckoutId = NULL
        WHERE 
          itemId = NEW.itemId 
          AND
          instanceId = NEW.instanceId;
      END;
    """)

def create_database():
  create_tables()
  create_views()
  create_triggers()

def insert_sample_data():
  """ 
  Reads in SQL INSERT commands from files and executes them. 
  Commands need to be executed in a specific order.
  """
  
  with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()
    dir = 'sample_data'
    file_names = os.listdir(dir)
    for file_name in file_names:
      with open(f'{dir}/{file_name}') as file:
        command = file.read()
        cursor.execute(command)
        
    # updates = [
    #   """
    #   UPDATE ItemInstance
    #   SET currentCheckoutId = 3 
    #   WHERE instanceId = 5;
    #   """,
    #   """
    #   UPDATE ItemInstance
    #   SET currentCheckoutId = 4 
    #   WHERE instanceId = 7;
    #   """,
    #   """
    #   UPDATE ItemInstance
    #   SET currentCheckoutId = 5 
    #   WHERE instanceId = 9;
    #   """,
    #   """
    #   UPDATE ItemInstance
    #   SET currentCheckoutId = 6 
    #   WHERE instanceId = 11;
    #   """,
    #   """
    #   UPDATE ItemInstance
    #   SET currentCheckoutId = 7 
    #   WHERE instanceId = 13;
    #   """,
    #   """
    #   UPDATE ItemInstance
    #   SET currentCheckoutId = 8 
    #   WHERE instanceId = 15;
    #   """,
    # ]
    
    # for update in updates:
    #   cursor.execute(update)
      

if __name__ == '__main__':
  try:
    drop_all()
    create_database()
    insert_sample_data()
  except sqlite3.Error as e:
    print(e)
