import basic
import SQL
import player


# This module include all the function that run the player action
# There are four action move/treat/cure/build
# Each action is derived into three small function step
# 1. Action check (_check). Generally return a dictionary of needed info if action is available, return false otherwise.
# 2. Action print (_print). Simply accept the dictionary from previous function and print out.
# 3. Action execute (_execute). Execute the action, update database needed.

# Move action. There are some (_info) function, use to gather information of different move type.
# Return city id list that player can drive/ferry into (neighbor city of current player location)
def move_drive_info(player_id):
    return basic.cityConnection(basic.playerId_to_cityId(player_id))

# Return city id list that player can discard corresponding card to fly directly into.
# Return [False] if player does not have any card.
def move_fly_info(player_id):
    data_raw = SQL.query_all(f"select card_id from player_own where player_id = {player_id};")
    if data_raw is not None:
        data_out = []
        direct_city = move_drive_info(player_id)
        jet_check = move_jet_info(player_id)
        if jet_check is not False:
            direct_city.append(jet_check)
        for i in data_raw:
            if i[0] not in direct_city:
                data_out.append(i[0])
        return data_out
    else:
        return [False]

# Return city id card that player can discard to fly anywhere
# Return [False] if player does not meet the requirement (player's location is the same as 1 of his/her city card)
def move_jet_info(player_id):
    data = SQL.query_one(f"select card_id from player_own, player_current "
                         f"where player_current.city_id = player_own.card_id and player_current.player_id = player_own.player_id and player_own.player_id = {player_id};")
    if bool(data) is False:
        return False
    else:
        return data[0]

# Return list of city id that player can fly directly
# Return [False] if there is only 1 research center in the map or player are not stay at one.
def move_rc_info(player_id):
    check_rc_amount = SQL.query_one(f"select research_center from game_current")
    check_location = SQL.query_one(f"select city.id from city, player_current "
                                   f"where player_id = {player_id} and player_current.city_id = city.id and research_center = 1;")
    if int(check_rc_amount[0])>1 and check_location is not None:
        data = SQL.query_all(f"select id from city where research_center = 1;")
        data = [i[0] for i in data]
        data.remove(basic.playerId_to_cityId(player_id))
        return data
    else:
        return [False]

# Return the dictionary of available city id that for each move type, player can move into.
def move_check(player_id):
    move_dict = {'drive': move_drive_info(player_id),
                 'fly': move_fly_info(player_id),
                 'jet': move_jet_info(player_id),
                 'rc': move_rc_info(player_id)
                 }
    return move_dict

def move_check_info(player_id):

    data = move_drive_info(player_id)
    driveData = []
    for member in data:
        driveData.append(
            {
                'id': member,
                'location': basic.return_city_coordinate(member)
            })

    data = move_fly_info(player_id)
    flyData = []
    if data:
        for member in data:
            flyData.append(
                {
                    'id': member,
                    'location': basic.return_city_coordinate(member)
                })

    data = move_rc_info(player_id)
    rcData = []
    if data[0]:
        for member in data:
            rcData.append(
                {
                    'id': member,
                    'location': basic.return_city_coordinate(member)
                })
    else: rcData = False

    move_dict ={
        'drive': driveData,
        'fly': flyData,
        'jet': move_jet_info(player_id),
        'rc': rcData
    }

    return move_dict

def player_own_info(player_id):
    data = SQL.query_all(f"select card_id from player_own where player_id = {player_id}")
    return_data = []
    for i in data:
        city = SQL.query_one(f"select city_name, virus from city where id = {i[0]}; ")
        return_data.append({
            "id" : i[0],
            "name": city[0],
            "color": city[1]
        })
    return return_data

# Execute move, update the player location, discard suitable card if player use fly move or jet move
# Return True if move is done successfully or False if player cannot make the move.
def move_execute(player_id, city_id,move_dict):
    if city_id in move_dict['drive'] + move_dict['fly'] + move_dict['rc']:
        SQL.update(f"update player_current set city_id = {city_id} where player_id = {player_id};")
        if city_id in move_dict['fly']:
            player.discard(player_id, city_id)
        return True
    elif move_dict['jet']:
        SQL.update(f"update player_current set city_id = {city_id} where player_id = {player_id};")
        player.discard(player_id, move_dict['jet'])
        return True

# Return the dictionary of available virus color and its amount if higher than zero, in the current player location.
# If city does not have any virus, the dictionary will be empty {}, and thus return False. Otherwise, return the dictionary.
def treat_check(player_id):
    data = basic.return_city_situation_from_player(player_id)
    treatList = [data[1],data[2],data[3],data[4]]
    return treatList



def treat_execute(player_id,virus,treatList):
    virusName = ['blue','violet','red','yellow']
    if sum(treatList) == 0:
        print(f"No disease at your current city, treat is not needed!")
        return False
    elif treatList[virus] == 0:
        print(f"No {virus} disease at your current city, treat is not needed!")
        return False
    else:
        city_id = basic.playerId_to_cityId(player_id)
        if basic.is_cure(virusName[virus]):
            amount = treatList[virus]
        else:
            amount = 1
        basic.remove_cube(city_id, virusName[virus], amount)
        return True


def build_check(player_id):
    city_card = move_jet_info(player_id)
    if city_card:
        city_check = SQL.query_one(f"select research_center from city where id = {city_card};")
        if city_check[0] == 0:
            return city_card
        else:
            return False
    else:
        return False

def build_execute(player_id):
    if build_check(player_id) is False:
        return False
    else:
        city_id = basic.playerId_to_cityId(player_id)
        SQL.update(f"update city set research_center = 1 "
                   f"where id = {city_id};")
        SQL.update(f"update game_current set research_center = research_center + 1 ")
        player.discard(player_id, city_id)
        return True


def cure_check(player_id):
    cure_data = {'blue': [],
                 'violet': [],
                 'red': [],
                 'yellow': [],
                 'cure': []
                 }
    card_check = SQL.query_all(f"select virus,id from player_own, city "
                               f"where player_id = {player_id} and card_id = city.id order by virus;")
    rc_check = SQL.query_one(f"select research_center from city, player_current "
                                    f"where player_id = {player_id} and city.id  = player_current.city_id;")

    for i in card_check:
        cure_data[i[0]].append(i[1])
    for i in cure_data:
        if len(cure_data[i]) >= 4:
            cure_data['cure'].append(i)

    if cure_data['cure'] and rc_check[0] == 1:
        return cure_data
    else:
        return False


def cure_execute(player_id,cure_dict, virus):
    if virus not in cure_dict['cure']:
        print(f"you are unable to treat {virus} disease")
        return False
    else:
        SQL.update(f"update game_current set {virus} = 1;")
        for i in range(4):
            player.discard(player_id, cure_dict[virus][0])
            cure_dict[virus].pop(0)
        return True