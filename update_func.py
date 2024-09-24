import random

import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1202',
    database='pandemic'
)

def update_player_location(player_id, new_location_id):
    cursor = connection.cursor()
    cursor.execute(f"update player_info set city_id = {new_location_id} where player_id = {player_id}")
    connection.commit()

def get_city_connection(city_id): #return a list of city_id that has connection to
    cursor = connection.cursor()
    cursor.execute(f"select connection from city_db where id = {city_id};")
    data = cursor.fetchall()
    return data[0][0].split(' ')

def get_city_connection_from_player(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select city_id from player_info where player_id = {player_id};")
    cursor.execute(f"select connection from city_db where id = {cursor.fetchone()[0]};")
    return cursor.fetchone()[0].split(' ')

def reset_infection_deck():
    cursor = connection.cursor()
    order = list(range(1,49))
    random.shuffle(order)
    for i in order:
        cursor.execute(f"insert into infection_deck values ({i});")
        connection.commit()

def set_up_infection_deck():
    three_cube = select_infection_deck_top_three()
    two_cube = select_infection_deck_top_three()
    one_cube = select_infection_deck_top_three()
    return {'3_cube': three_cube,'2_cube': two_cube,'1_cube': one_cube }

def discard_infection_card(card_id):
    cursor = connection.cursor()
    cursor.execute(f"insert into infection_discard values ({card_id});")
    connection.commit()

def select_infection_deck_bottom():
    cursor = connection.cursor()
    cursor.execute(f"select * from infection_deck;")
    data = cursor.fetchall()
    return data[-1][0]

def select_infection_deck_top_three():
    cursor = connection.cursor()
    cursor.execute(f"select * from infection_deck limit 3;")
    data = cursor.fetchall()
    data_out = []
    for i in data:
        data_out.append(i[0])
        cursor.execute(f"delete from infection_deck where city_id = {i[0]};")
        connection.commit()
        discard_infection_card(i[0])
    return data_out