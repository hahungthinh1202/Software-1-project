import random
import SQL
import infection

def city_connection(city_id): #return a list of city_id that has connection to
    data = SQL.query_all(f"select connection from city_db where id = {city_id};")
    return data[0][0].split(' ')

def playerId_to_cityId(player_id):
    data = SQL.query_one(f"select city_id from player_current where player_id = {player_id};")
    return data[0]

def put_cube(city_id,virus,amount):
    data = is_outbreak(city_id, virus, amount)
    if data == 4:
        outbreak(city_id,virus)
    else:
        print(f"{virus} level at {cityId_to_cityName(city_id)} raised from {data} to {amount + data}", )
        SQL.update(f"update city_current set {virus} = {amount+data} where city_id = {city_id};")

def remove_cube(city_id,virus,amount):
    SQL.update(f"update city_current set {virus} = {virus} - {amount} where city_id = {city_id};")


def is_outbreak(city_id,virus,amount):
    data = SQL.query_one(f"select {virus} from city_current where city_id = {city_id};")
    data = int(data[0])
    if (amount+data)>3:
        return 4
    else:
        return data

def is_cure(virus):
    data = SQL.query_one(f"select {virus} from game_current;")
    return bool(data[0])

def outbreak(city_id,virus):
    print("Out break happen at", cityId_to_cityName(city_id))
    SQL.update(f"update city_current set is_outbreak = True where city_id = {city_id};")
    SQL.update(f"update city_current set {virus} = {3} where city_id = {city_id};")
    SQL.update(f"update game_current set outbreak_track = outbreak_track + 1;")
    connected_city = city_connection(city_id)
    for i in connected_city:
        print(f"Disease spread into {cityId_to_cityName(i)}")
        check_outbreak = SQL.query_one(f"select is_outbreak from city_current where city_id = {i};")
        if not check_outbreak[0]:
            put_cube(i,virus,1)

def reset_outbreak_flag():
    SQL.update(f"update city_current set is_outbreak = 0")


def reset_city():
    SQL.update("delete from city_current")
    for i in range(1,49):
        SQL.update(f"insert into city_current values ({i}, 0, 0, 0, 0, false, false);")
    SQL.update(f"update city_current set research_center = True where city_id = 5;")


def reset_game_track():
    SQL.update(f"update game_current set outbreak_track = 0, infection_track = 0, "
                   f"blue = 0, violet = 0, red = 0, yellow = 0, research_center = 1;")


def set_up_map():
    reset_city()
    reset_game_track()
    set_up_cube = infection.init()
    for i in set_up_cube:
        for j in range(3):
            put_cube(set_up_cube[i][j][0],set_up_cube[i][j][1],i)

def set_up_player_deck(difficulty,num_player):

    SQL.update("delete from player_own")
    SQL.update("delete from player_card_current")
    card_list = list(range(1, 49))
    random.shuffle(card_list)
    for i in range(1,num_player+1):
        for j in range(4):
            SQL.update(f"insert into player_own values({i},{card_list[0]});")
            card_list.pop(0)
    stack_size  = int(len(card_list)/difficulty)
    for i in range(difficulty):
        card_list.insert(random.randint(stack_size*i+i,stack_size*(i+1)+i-1),-i-1)
    for i in range(len(card_list)):
        SQL.update(f"insert into player_card_current values({card_list[i]});")


def cityName_to_cityId(city_name):
    data = SQL.query_one(f"select id from city_db where city_name = '{city_name}';")
    if data is None:
        return False
    else:
        return data[0]

def cityId_to_cityName(city_id):
    data = SQL.query_one(f"select city_name from city_db where id = '{city_id}';")
    if data is None:
        print("not recognized city_id")
        return False
    else:
        return data[0]

def return_game_info():
    data = SQL.query_one(f"select infection_track, outbreak_track, blue, violet, red, yellow from game_current;")
    return data


def return_all_city_situation():
    data = SQL.query_all(f"select city_id, blue, violet, red, yellow, research_center from city_current "
                        f"where  blue>0 or violet>0 or yellow>0 or red>0 or research_center>0;")
    return data

def return_city_situation_from_player(player_id):
    data = SQL.query_all(f"select city_current.city_id, blue, violet, red, yellow from city_current,player_current "
                        f"where city_current.city_id = player_current.city_id and player_id = {player_id}; ")
    return data[0]

def return_player_coordinate():
    data = SQL.query_all(f"select player_id, latitude, longitude from city_db, player_current "
                        f"where id = city_id order by player_id;")
    return data

def return_city_coordinate(city_id):
    data = SQL.query_all(f"select latitude, longitude from city_db where id = {city_id}; ")
    return data[0]

def game_init(difficulty,num_player):
    set_up_map()
    set_up_player_deck(difficulty, num_player)

def check_win():
    outbreaK_amount = SQL.query_one(f"select outbreak_track from game_current;")[0]
    player_deck  = SQL.query_all(f"select city_id from player_card_current limit 1;")
    basic.reset_outbreak_flag()
    if  player_deck is None or outbreaK_amount >7:
        return True
    return False



