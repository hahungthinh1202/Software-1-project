import basic
import SQL
import player
from basic import cityId_to_cityName


# Return city id list that player can drive/ferry into (neighbor city of current player location)
def move_drive_info(player_id):
    return basic.city_connection(basic.playerId_to_cityId(player_id))

# Return city id list that player can discard corresponding card to fly directly into.
# Return [False] if player does not have any card
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

#Return city id card that player can discard to fly anywhere
#Return [False] if player does not meet the requirement (player's location is the same as 1 of his/her city card)
def move_jet_info(player_id):
    data = SQL.query_one(f"select card_id from player_own, player_current "
                         f"where player_current.city_id = player_own.card_id and player_current.player_id = player_own.player_id and player_own.player_id = {player_id};")
    if bool(data) is False:
        return False
    else:
        return data[0]

#Return list of city id that player can fly directly
#Return [False] if there is only 1 research center in the map or player are not stay at one.
def move_rc_info(player_id):
    check_rc_amount = SQL.query_one(f"select research_center from game_current")
    check_location = SQL.query_one(f"select city_current.city_id from city_current, player_current "
                                   f"where player_id = {player_id} and player_current.city_id = city_current.city_id and research_center = 1;")
    if int(check_rc_amount[0])>1 and check_location is not None:
        data = SQL.query_all(f"select city_id from city_current where research_center = 1;")
        data = [i[0] for i in data]
        data.remove(basic.playerId_to_cityId(player_id))
        return data
    else:
        return [False]

def move_check(player_id):
    move_dict = {'drive': move_drive_info(player_id),
                 'fly': move_fly_info(player_id),
                 'jet': move_jet_info(player_id),
                 'rc': move_rc_info(player_id)
                 }
    return move_dict

def move_detail_print(move_dict):
    print("you can drive/ferry to", [basic.cityId_to_cityName(i) for i in move_dict['drive']])
    if move_dict['fly']:
        print("Or you can discard corresponding city card to fly to",
              [basic.cityId_to_cityName(i) for i in move_dict['fly']])
    if move_dict['jet']:
        print(f"Or you can discard '{basic.cityId_to_cityName(move_dict['jet'])}' card to fly anywhere")
    if move_dict['rc'][0]:
        print(f"Or you can fly directly to these city", [basic.cityId_to_cityName(i) for i in move_dict['rc']],
              "that have a research center:")

def move_execute(player_id, city_id,move_dict):
    if city_id in move_dict['drive'] + move_dict['fly'] + move_dict['rc']:
        SQL.update(f"update player_current set city_id = {city_id} where player_id = {player_id};")
        if city_id in move_dict['fly']:
            player.discard(player_id, city_id)
        return True
    elif move_dict['jet']:
        move_execute(player_id, city_id)
        player.discard(player_id, move_dict['jet'])
        return True
    else:
        print(f"You can not move to {basic.cityId_to_cityName(city_id)}")
        return False

def treat_check(player_id):
    data = basic.return_city_situation_from_player(player_id)
    treat_dict = {
        'blue': data[1],
        'violet': data[2],
        'red': data[3],
        'yellow': data[4]
    }
    pop_list = []
    for i in treat_dict:
        if treat_dict[i] == 0:
            pop_list.append(i)
    for i in pop_list:
        treat_dict.pop(i)
    treat_dict['city']= cityId_to_cityName(data[0])
    if treat_dict == {}:
        return [False]
    else:
        return treat_dict

def treat_detail_print(treat_dict):
    print(f"Or you can treat the disease at {treat_dict['city']}:")
    for i in treat_dict:
        if i != 'city':
            print(f"  - {i} disease is at level {treat_dict[i]}")

def treat_execute(player_id,virus,treat_dict):
    if treat_dict == {}:
        print(f"No disease at your current city, treat is not needed!")
        return False
    elif virus not in treat_dict:
        print(f"No {virus} disease at your current city, treat is not needed!")
        return False
    else:
        city_id = basic.playerId_to_cityId(player_id)
        if basic.is_cure(virus):
            amount = treat_dict[virus]
        else:
            amount = 1
        basic.remove_cube(city_id,virus,amount)
        return True


def build_check(player_id):
    city_card = move_jet_info(player_id)
    if city_card:
        city_check = SQL.query_one(f"select research_center from city_current where city_id = {city_card};")
        if city_check[0] == 0:
            return city_card
        else:
            return False
    else:
        return False

def build_detail_print(build_dict):
    print(f"Or you can remove {cityId_to_cityName(build_dict)} card to build a research center here!")


def build_execute(player_id):
    if build_check(player_id) is False:
        print("You cannot build!")
        return False
    else:
        city_id = basic.playerId_to_cityId(player_id)
        print(f"Build research center at {basic.cityId_to_cityName(player_id)}")
        SQL.update(f"update city_current set research_center = 1 "
                   f"where city_id = {city_id};")
        SQL.update(f"update game_current set research_center = research_center + 1 ")
        player.discard(player_id,city_id)
        return True


def cure_check(player_id):
    cure_data = {'blue': [],
                 'violet': [],
                 'red': [],
                 'yellow': [],
                 'cure': []
                 }

    data = SQL.query_all(f"select virus,id from player_own, city_db where player_id = {1} and card_id = id order by virus;")
    for i in data:
        cure_data[i[0]].append(i[1])
    for i in cure_data:
        if len(cure_data[i]) >= 4:
            cure_data['cure'].append(i)
    if cure_data['cure'] == []:
        return False
    else:
        return cure_data

def cure_print (cure_dict):
    for i in cure_dict['cure']:
        print(f"Or you can discard 4 {i} card to find the vaccine of the {i} disease")

def cure_execute(player_id,cure_dict, cube_color):
    if cube_color not in cure_dict:
        print(f"you are unable to treat {cube_color} disease")
    else:
        SQL.update(f"update game_current set {cube_color} = 1;")
        for i in range(4):
            player.discard(player_id,cure_dict[cube_color][0])
            cure_dict[cube_color].pop(0)