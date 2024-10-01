import random
import infection
from os.path import curdir

import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1202',
    database='pandemic'
)

def get_city_connection(city_id): #return a list of city_id that has connection to
    cursor = connection.cursor()
    cursor.execute(f"select connection from city_db where id = {city_id};")
    data = cursor.fetchall()
    return data[0][0].split(' ')

def get_city_connection_from_player(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select city_id from player_current where player_id = {player_id};")
    return get_city_connection(cursor.fetchone()[0])

def put_cube(city_id,virus,amount):
    cursor = connection.cursor()
    data = is_outbreak(city_id, virus, amount)
    print(data)
    if data == 4:
        print("out_break")
        outbreak(city_id,virus)
    else:
        cursor.execute(f"update city_current set {virus} = {amount+data} where city_id = {city_id};")
        connection.commit()

def is_outbreak(city_id,virus,amount):
    cursor = connection.cursor()
    cursor.execute(f"select {virus} from city_current where city_id = {city_id};")
    data = int(cursor.fetchone()[0])
    print(data)
    connection.commit()
    if (amount+data)>3:
        return 4
    else:
        return data

def outbreak(city_id,virus):
    cursor = connection.cursor()
    cursor.execute(f"update city_current set is_outbreak = True where city_id = {city_id};")
    cursor.execute(f"update city_current set {virus} = {3} where city_id = {city_id};")
    connection.commit()
    connected_city = get_city_connection(city_id)
    for i in connected_city:
        cursor.execute(f"select is_outbreak from city_current where city_id = {i};")
        check_outbreak = cursor.fetchone()[0]
        connection.commit()
        if not check_outbreak:
            print("put_cube",i)
            put_cube(i,virus,1)

def reset_outbreak_flag():
    cursor = connection.cursor()
    cursor.execute(f"update city_current set is_outbreak = False where is_outbreak = True;")
    connection.commit()

def reset_city():
    cursor = connection.cursor()
    cursor.execute("delete from city_current")
    connection.commit()
    for i in range(1,49):
        cursor.execute(f"insert into city_current values ({i}, 0, 0, 0, 0, false, false);")
    cursor.execute(f"update city_current set research_center = True where city_id = 5;")
    connection.commit()

def set_up_map():
    infection.reset_discard()
    set_up_cube = infection.set_up_begin_deck()
    reset_city()
    for i in set_up_cube:
        for j in range(3):
            put_cube(set_up_cube[i][j][0],set_up_cube[i][j][1],i)

def set_up_player_deck(difficulty,num_player):
    cursor = connection.cursor()
    card_list = list(range(1, 49))
    random.shuffle(card_list)
    for i in range(1,num_player+1):
        for j in range(4):
            cursor.execute(f"insert into player_own values({i},{card_list[0]});")
            card_list.pop(0)
    connection.commit()
    stack_size  = int(len(card_list)/difficulty)
    for i in range(difficulty):
        card_list.insert(random.randint(stack_size*i+i,stack_size*(i+1)+i-1),-1)
    for i in range(len(card_list)):
        cursor.execute(f"insert into player_card_current values({i+1},{card_list[i]});")
        connection.commit()

def draw_card(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select player_card_current.city_id, player_card_current.id from player_card_current, game_current "
                   f"where player_card_current.id = game_current.current_player_card;")
    data = cursor.fetchone()
    city = data[0]
    current_player_card = int(data[1])
    print(current_player_card)
    if int(city)<0 :
        epidemic()
    else:
        cursor.execute(f"insert into player_own values({player_id},{city});")
        cursor.execute(f"update game_current set current_player_card={current_player_card+1};")
    connection.commit()

def epidemic():
    pass




def get_map_data():
    cursor = connection.cursor()
    map_dict ={}
    cursor.execute(f"select latitude, longitude,blue,red,yellow,black, research_center from city_current, city_db "
                   f"where city_id = id and blue>0 or black>0 or yellow>0 or red>0 or research_center>0;")
    data = cursor.fetchall()
    return data

def return_player_location(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select latitude, longitude from city_db, player_current "
                   f"where id = city_id and player_id = {player_id};")
    data = cursor.fetchone()
    connection.commit()
    return data

