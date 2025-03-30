from app import app
from db_functions import *


@app.get('/members')
def get_all_members():
    return get_members_list()

@app.get('/items')
def get_all_items():
    return get_items()

@app.get('/instances')
def get_all_item_instances():
    return get_item_instances_list()

@app.get('/personnel')
def get_all_personnel():
    return get_personnel_list()

@app.get('/checkouts')
def get_all_checkout_records():
    return get_all_checkout_records_list()

@app.get('/fines')
def get_all_fines():
    return get_all_fines_list()

@app.get('/fines/outstanding')
def get_all_outstanding_fines():
    return get_all_outstanding_fines_list()
