from app import app
from db_functions.items import get_items_list
from db_functions.members import get_members_list
from db_functions.personnel import get_personnel_list



@app.get('/members')
def get_all_members():
    return get_members_list()

@app.get('/items')
def get_all_items():
    return get_items_list()



@app.get('/personnel')
def get_all_personnel():
    return get_personnel_list()
