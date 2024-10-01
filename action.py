import random
import basic
from os.path import curdir

import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1202',
    database='pandemic'
)


def move_execute(player_id, city_id):
    cursor = connection.cursor()
    cursor.execute(f"update player_current set city_id = {city_id} where player_id = {player_id};")
    print("move_",city_id,player_id)
    connection.commit()

def move_drive_info(player_id):
    return basic.get_city_connection_from_player(player_id)

def move_direct_info(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select card_id from player_own where player_id = {player_id};")
    data_raw = cursor.fetchall()
    connection.commit()
    data_out = []
    for i in data_raw:
        data_out.append(i[0])
    return data_out

def move_charter_info(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select card_id from player_own, player_current "
                   f"where player_current.city_id = player_own.card_id and player_current.player_id = player_own.player_id and player_own.player_id = {player_id};")
    return bool(cursor.fetchone())

def move_info(player_id):
    pass

def treat_info(player_id):
    pass

def treat_execute(player_id,cube_color):
    pass

def build_RC_info(player_id):
    pass

def build_RC_execute(player_id):
    pass

def cure_info(player_id):
    pass

def cure_execute(player_id,cube_color):
    pass