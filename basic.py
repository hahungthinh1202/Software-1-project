import random
import SQL
import infection
import basic

# This module has all the miscancellus functions that are not yet or unable to categorize into other group.
# These function is not optimized and may be unnecessary.

# Recieve city_id and return a list of city_id that has connection to
def cityConnection(cityId):
    data = SQL.query_all(f"select connection from city where id = {cityId};")
    return data[0][0].split(' ')

# Recieve player id and return player's current city location id
def playerId_to_cityId(player_id):
    data = SQL.query_one(f"select city_id from player_current where player_id = {player_id};")
    return data[0]

# Add cube into a specific city
# The maximum of cube of each color is 3. if maximum is surpassed, an outbreak execute in this city,
# if not, update amount of cube in current city database.
def put_cube(city_id,virus,amount):
    data = is_outbreak(city_id, virus, amount)
    if data == 4:
        outbreak(city_id,virus)
    else:
        SQL.update(f"update city set {virus} = {amount + data} where id = {city_id};")

# Remove cube from specific city, basically update the current city database
def remove_cube(city_id,virus,amount):
    SQL.update(f"update city set {virus} = {virus} - {amount} where id = {city_id};")

# Check if city could outbreak if an amount of virus is add to that city
# Simply get the current amount of virus from database and add to the new amount
# If the result is more than three then this is out break.
# Or return the new amount of cube after added

def is_outbreak(city_id,virus,amount):
    data = SQL.query_one(f"select {virus} from city where id = {city_id};")
    data = int(data[0])
    if (amount+data)>3:
        return 4
    else:
        return data

# Return true if the vaccine for that virus is found
def is_cure(virus):
    data = SQL.query_one(f"select {virus} from game_current;")
    return bool(data[0])

# Execute the outbreak sequence of a specific city with specific virus:
# 1. Set the outbreak flag of this city to True to avoid chain outbreak (city can only outbreak one per player turn).
#    Flag will be reset after player turn
# 2. Set the maximum of three cubes in that city.
# 3. Increase the outbreak track in the game map.
# 4. For every connected city, first check if that city is already outbreak during the current turn.
#    If yes, do nothing,
#    If no, put one cube of the same color. This could also trigger another outbreak.
def outbreak(city_id,virus):
    SQL.update(f"update city set is_outbreak = True where id = {city_id};")
    SQL.update(f"update city set {virus} = {3} where id = {city_id};")
    SQL.update(f"update game_current set outbreak_track = outbreak_track + 1;")
    connected_city = cityConnection(city_id)
    for i in connected_city:
        check_outbreak = SQL.query_one(f"select is_outbreak from city where id = {i};")
        if not check_outbreak[0]:
            put_cube(i,virus,1)

# Reset the outbreak flag of everycity
def reset_outbreak_flag():
    SQL.update(f"update city set is_outbreak = 0")

# Reset the current data of every city (four virus color to zero, research center and outbreak flag to False)
def reset_city():
    for i in range(1,49):
        SQL.update(f"update city set blue = 0, violet = 0, red = 0, yellow = 0, research_center = FALSE where id = {i};")
    SQL.update(f"update city set research_center = True where id = 10;")

# Reset the current game track (Outbreak track and infection track back to zero)
def reset_game_track():
    SQL.update(f"update game_current set outbreak_track = 0, infection_track = 0, "
                   f"blue = 0, violet = 0, red = 0, yellow = 0, research_center = 1, player_turn = 1;")

# Reset the location of both player, back to Helsinki
# This function should recieve a parameter player_amount, thus not limited in only two.
def reset_player():
    SQL.update("update player_current set city_id = 10, action_point = 5 where player_id = 1;")
    SQL.update("update player_current set city_id = 10, action_point = 4 where player_id = 2;")

# Set up for a new game.
# Everything in the map (virus cube, game track and infection deck).
def set_up_map():
    reset_city()
    reset_game_track()
    reset_player()
    set_up_cube = infection.init()
    for i in set_up_cube:
        for j in range(3):
            put_cube(set_up_cube[i][j][0],set_up_cube[i][j][1],i)

# Set up for a new game.
# Reset player deck base of difficulty and amount of player
# 1. Keyword and sequence explained:
#    - Player deck is a comprised of city card and a set amount of epidemic card
#    - In the end of a turn, player will draw two player card. Thus can be either good city card or
#    bad epidemic card (which will trigger an epidemic)
#    - The difficulty, is the amount of epidemic card that will be shuffle into the player deck.
# 2. Set up sequence
#    - Delete everything from the corresponding table
#    - Random a list of number from 1-48 called list A
#    - Deal four cards for each player by remove number of list A, and insert into own table. The remain called list B.
#    - Divide list B into specific equal deck base of amount of epidemic card. then insert negative number
#      start from -1 to present epidemic card into those equal deck create list C.
#    - Insert list C into the current player card table.
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

# Get game infomation as shown in the sql command. This function is used to get information to display on map
# and to find correct amount of cubes to be remove in treat action (one if vaccine found or up to three otherwise).
def return_game_info():
    gameData = SQL.query_one(f"select infection_track, outbreak_track, blue, violet, red, yellow, player_turn from game_current;")
    returnData ={
        'infection_track': gameData[0],
        'outbreak_track': gameData[1],
        'blue': gameData[2],
        'violet': gameData[3],
        'red': gameData[4],
        'yellow': gameData[5],
        'player_turn': gameData[6],
    }
    return returnData

# Return the virus cube amount or research center of all the cities that has some. This is used to display on map.
def return_all_city_situation():
    cityList = []
    cityData = SQL.query_all(f"select id, city_name, latitude, longitude, blue, violet, red, yellow, research_center from city;")
    for i in cityData:
        cityMember = {
            "id": i[0],
            "city_name": i[1],
            "latitude": i[2],
            "longitude": i[3],
            "blue": i[4],
            "violet": i[5],
            "red": i[6],
            "yellow": i[7],
            "research_center": i[8],
        }
        cityList.append(cityMember)
    return cityList

# Return the virus cube situation of player current location. Used to show available option for player to treat.
def return_city_situation_from_player(player_id):
    data = SQL.query_all(f"select city.id, blue, violet, red, yellow from city,player_current "
                        f"where city.id = player_current.city_id and player_id = {player_id}; ")
    return data[0]

# Return player longitude and latitude from current location. I am not sure if this function is really neccessary.
def return_player_coordinate():
    playerList = []
    playerData = SQL.query_all(f"select player_id, player_name, city_name, latitude, longitude, action_point from city, player_current "
                        f"where city.id = player_current.city_id order by player_id;")
    for i in playerData:
        returnData = {
            'player_id': i[0],
            'player_name': i[1],
            'city_name': i[2],
            'latitude': i[3],
            'longitude': i[4],
            'action_point': i[5],
        }
        playerList.append(returnData)
    return playerList

# Return city latitude and longtitude from city ID. Also, as previous function, both could be implemented in some
# other way that is more neat, this should be improved later.
def return_city_coordinate(city_id):
    data = SQL.query_all(f"select latitude, longitude from city where id = {city_id}; ")
    return data[0]

def return_current_player_info():
    player_turn = SQL.query_one(f"select player_turn from game_current;")[0]
    player_action_point = SQL.query_one(f"select action_point from player_current where player_id = {player_turn};")[0]
    print("return current player info succesfully")
    return player_turn, player_action_point

def update_player_turn(player_turn):
    player_action_point = SQL.query_one(f"select action_point from player_current where player_id = {player_turn};")[0]
    print(type(player_action_point))
    if player_action_point == 0:
        print("action point = 1")
        SQL.update(f"update player_current set action_point = 4 where player_id = {player_turn};")
        player_turn = 1 + player_turn % 2
        SQL.update(f"update game_current set player_turn = {player_turn};")
    else:
        SQL.update(f"update player_current set action_point = action_point - 1 where player_id = {player_turn};")
    print("updated player turn successfully")


# Return False if game is not yet reached end condition. Otherwise, return 'win' or 'lose.
def check_win():
    game_info = SQL.query_one(f"select outbreak_track, blue, violet, red, yellow from game_current;")
    player_deck  = SQL.query_all(f"select city_id from player_card_current limit 1;")
    basic.reset_outbreak_flag()
    if  player_deck is None or game_info[0] >7:
        return {
            'check' : ["lose","The pandemic is out of control.<n>"
                     "The disease spread faster than <n>"
                     "containment effort despite your<n>"
                     "best efforts, the outbreak<n>"
                     "overwhelmed the world.<n>"
                     "You Lose"]
        }
    elif sum(game_info[1:5]) == 4:
        return {
            'check' : ["win","Congratulations! After tireless efforts,<n>"
                     "you have successfully discovered all four vaccines<n>"
                     "and eradicated the pandemic.<n>"
                     "You Win"]
        }
    return {
            'check' : False
        }


def tutorialSetup():

    pass
