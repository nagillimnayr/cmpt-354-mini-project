import sqlite3
from constants import *
from utils import *

def get_item_instances_list():
  with connect_to_db() as conn:
    cursor = conn.cursor()
    cursor.execute("""
      SELECT * 
      FROM ItemInstance
      ORDER BY itemId, instanceId;
    """)
    return cursor.fetchall()


def select_item_instance(item_id: int, instance_id: int):
  with connect_to_db() as conn:
    return conn.execute("""
      SELECT * 
      FROM ItemInstance
      WHERE
        itemId = :item_id
        AND
        instanceId = :instance_id;       
    """, {
      'item_id': item_id,
      'instance_id': instance_id,
    }).fetchone()
