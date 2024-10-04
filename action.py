import random
import basic
from os.path import curdir

import mysql.connector

from basic import remove_cube

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1202',
    database='pandemic'
)


def move_execute(player_id, city_id):
    cursor = connection.cursor()
    cursor.execute(f"update player_current set city_id = {city_id} where player_id = {player_id};")
    print("move_",player_id," to ",city_id)
    connection.commit()

def move_drive_info(player_id):
    return basic.city_connection_from_player(player_id)

def move_fly_info(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select card_id from player_own where player_id = {player_id};")
    data_raw = cursor.fetchall()
    connection.commit()
    data_out = []
    direct_city = move_drive_info(player_id)
    jet_check = move_jet_info(player_id)
    if jet_check is not False:
        direct_city.append(jet_check)
    for i in data_raw:
        if i[0] not in direct_city:
            data_out.append(i[0])
    return data_out

def move_jet_info(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select card_id from player_own, player_current "
                   f"where player_current.city_id = player_own.card_id and player_current.player_id = player_own.player_id and player_own.player_id = {player_id};")
    data = cursor.fetchone()
    if bool(data) is False:
        return [False]
    else:
        return data[0]
def move_rc_info(player_id):
    return [False]

def move_info(player_id):
    move_dict = {'drive': move_drive_info(player_id),
                 'fly': move_fly_info(player_id),
                 'jet': move_jet_info(player_id),
                 'rc': move_rc_info(player_id)
                 }
    print("you can drive/ferry to", [basic.city_id_to_name(i) for i in move_dict['drive']])
    print("Or you can discard corresponding city card to fly to", [basic.city_id_to_name(i) for i in move_dict['fly']])
    if move_dict['jet'][0]:
        print(f"Or you can discard '{basic.city_id_to_name(move_dict['jet'])}' card to fly anywhere")
    if move_dict['rc'][0]:
        print(f"Or you can move to these city that have RC:")
    print("where you want to go?")

    return move_dict

def treat_info(player_id):
    data = basic.return_city_situation_from_player(player_id)
    check_sum = sum(data[1:6])
    if check_sum == 0:
        print("No disease in this city, cannot treat!")
        return False
    else:
        print("City x situation:")
        if data[1]:
            print(f"Blue disease is at level {data[1]}")
        if data[2]:
            print(f"Violet disease is at level {data[2]}")
        if data[3]:
            print(f"Red disease is at level {data[3]} ")
        if data[4]:
            print(f"Yellow disease is at level {data[4]}")
        print("Which disease you want to treat?")
        return data



def treat_execute(player_id,virus,current_level):
    city_id = basic.city_id_from_player_id(player_id)
    if basic.is_cure(virus):
        amount = current_level
    else:
        amount = 1
    basic.remove_cube(city_id,virus,amount)
    pass

def build_rc_info(player_id):
    pass

def build_rc_execute(player_id):
    pass

def cure_info(player_id):
    pass

def cure_execute(player_id,cube_color):
    pass