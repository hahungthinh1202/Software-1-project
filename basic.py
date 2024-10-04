import random
import infection
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1202',
    database='pandemic'
)

def city_connection(city_id): #return a list of city_id that has connection to
    cursor = connection.cursor()
    cursor.execute(f"select connection from city_db where id = {city_id};")
    data = cursor.fetchall()
    return data[0][0].split(' ')

def city_id_from_player_id(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select city_id from player_current where player_id = {player_id};")
    return cursor.fetchone()[0]

def city_connection_from_player(player_id):
    return city_connection(city_id_from_player_id(player_id))

def put_cube(city_id,virus,amount):
    cursor = connection.cursor()
    data = is_outbreak(city_id, virus, amount)
    if data == 4:
        outbreak(city_id,virus)
    else:
        print(f"{virus} level at {city_id_to_name(city_id)} raised from {data} to {amount+data}", )
        cursor.execute(f"update city_current set {virus} = {amount+data} where city_id = {city_id};")
        connection.commit()

def remove_cube(city_id,virus,amount):
    cursor = connection.cursor()
    cursor.execute(f"update city_current set {virus} = {virus} - {amount} where city_id = {city_id};")
    connection.commit()


def is_outbreak(city_id,virus,amount):
    cursor = connection.cursor()
    cursor.execute(f"select {virus} from city_current where city_id = {city_id};")
    data = int(cursor.fetchone()[0])
    connection.commit()
    if (amount+data)>3:
        return 4
    else:
        return data

def is_cure(virus):
    cursor = connection.cursor()
    cursor.execute(f"select {virus} from game_current;")
    return bool(cursor.fetchone()[0])

def outbreak(city_id,virus):
    cursor = connection.cursor()
    print("Out break happen at", city_id_to_name(city_id))
    cursor.execute(f"update city_current set is_outbreak = True where city_id = {city_id};")
    cursor.execute(f"update city_current set {virus} = {3} where city_id = {city_id};")
    cursor.execute(f"update game_current set outbreak_track = outbreak_track + 1;")
    connection.commit()
    connected_city = city_connection(city_id)
    for i in connected_city:
        print(f"Disease spread into {city_id_to_name(i)}")
        cursor.execute(f"select is_outbreak from city_current where city_id = {i};")
        check_outbreak = cursor.fetchone()[0]
        connection.commit()
        if not check_outbreak:
            put_cube(i,virus,1)

def reset_outbreak_flag():
    cursor = connection.cursor()
    cursor.execute(f"update city_current set is_outbreak = 0")
    connection.commit()

def reset_city():
    cursor = connection.cursor()
    cursor.execute("delete from city_current")
    connection.commit()
    for i in range(1,49):
        cursor.execute(f"insert into city_current values ({i}, 0, 0, 0, 0, false, false);")
    cursor.execute(f"update city_current set research_center = True where city_id = 5;")
    connection.commit()

def reset_game_track():
    cursor = connection.cursor()
    cursor.execute(f"update game_current set outbreak_track = 0, infection_track = 0, "
                   f"blue = 0, violet = 0, red = 0, yellow = 0;")
    connection.commit()

def set_up_map():
    reset_city()
    reset_game_track()
    set_up_cube = infection.init()
    for i in set_up_cube:
        for j in range(3):
            put_cube(set_up_cube[i][j][0],set_up_cube[i][j][1],i)

def set_up_player_deck(difficulty,num_player):
    cursor = connection.cursor()
    cursor.execute("delete from player_own")
    cursor.execute("delete from player_card_current")
    connection.commit()
    card_list = list(range(1, 49))
    random.shuffle(card_list)
    for i in range(1,num_player+1):
        for j in range(4):
            cursor.execute(f"insert into player_own values({i},{card_list[0]});")
            card_list.pop(0)
    connection.commit()
    stack_size  = int(len(card_list)/difficulty)
    for i in range(difficulty):
        card_list.insert(random.randint(stack_size*i+i,stack_size*(i+1)+i-1),-i-1)
    for i in range(len(card_list)):
        cursor.execute(f"insert into player_card_current values({card_list[i]});")
        connection.commit()

def city_name_to_id(city_name):
    cursor = connection.cursor()
    cursor.execute(f"select id from city_db where city_name = '{city_name}';")
    data = cursor.fetchone()
    if data is None:
        print("not recognized city name")
        return False
    else:
        return data[0]

def city_id_to_name(city_id):
    cursor = connection.cursor()
    cursor.execute(f"select city_name from city_db where id = {city_id};")
    data = cursor.fetchone()
    if data is None:
        print("not recognized city_id")
        return False
    else:
        return data[0]

def return_game_info():
    cursor = connection.cursor()
    cursor.execute(f"select infection_track, outbreak_track from game_current;")
    data = cursor.fetchone()
    return data


def return_all_city_situation():
    cursor = connection.cursor()
    map_dict ={}
    cursor.execute(f"select city_id, blue, violet, red, yellow, research_center from city_current "
                   f"where  blue>0 or violet>0 or yellow>0 or red>0 or research_center>0;")
    data = cursor.fetchall()
    return data

def return_city_situation_from_player(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select city_current.city_id, blue, violet, red, yellow from city_current,player_current "
                   f"where city_current.city_id = player_current.city_id and player_id = {player_id}; ")
    data = cursor.fetchall()
    return data[0]

def return_player_coordinate():
    cursor = connection.cursor()
    cursor.execute(f"select player_id, latitude, longitude from city_db, player_current "
                   f"where id = city_id order by player_id;")
    data = cursor.fetchall()
    connection.commit()
    return data

def return_city_coordinate(city_id):
    cursor = connection.cursor()
    cursor.execute(f"select latitude, longitude from city_db where id = {city_id}; ")
    data = cursor.fetchall()
    return data[0]

def game_init(difficulty,num_player):
    set_up_map()
    set_up_player_deck(difficulty, num_player)

def check_win():
    print("check win/lose condition")

