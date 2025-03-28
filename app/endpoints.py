from app import app
from db_functions import *


@app.get('/members')
def get_all_members():
    return get_members_list()

@app.get('/items')
def get_all_items():
    return get_items_list()

@app.get('/personnel')
def get_all_personnel():
    return get_personnel_list()

@app.get('/checkouts')
def get_all_checkout_records():
    return get_all_checkout_records_list()
