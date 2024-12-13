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
def moveDriveInfo(player_id):
    return basic.cityConnection(basic.playerId_to_cityId(player_id))

# Return city id list that player can discard corresponding card to fly directly into.
# Return [False] if player does not have any card.
def moveFlyInfo(player_id):
    dataRaw = SQL.queryAll(f"select card_id from player_own where player_id = {player_id};")
    if dataRaw is not None:
        dataOut = []
        directCity = moveDriveInfo(player_id)
        jetCheck = moveJetInfo(player_id)
        if jetCheck is not False:
            directCity.append(jetCheck)
        for i in dataRaw:
            if i[0] not in directCity:
                dataOut.append(i[0])
        return dataOut
    else:
        return [False]

# Return city id card that player can discard to fly anywhere
# Return [False] if player does not meet the requirement (player's location is the same as 1 of his/her city card)
def moveJetInfo(player_id):
    data = SQL.queryOne(f"select card_id from player_own, player_current "
                         f"where player_current.city_id = player_own.card_id and player_current.player_id = player_own.player_id and player_own.player_id = {player_id};")
    if bool(data) is False:
        return False
    else:
        return data[0]

# Return list of city id that player can fly directly
# Return [False] if there is only 1 research center in the map or player are not stay at one.
def moveRcInfo(player_id):
    checkRcAmount = SQL.queryOne(f"select research_center from game_current")
    checkLocation = SQL.queryOne(f"select city.id from city, player_current "
                                   f"where player_id = {player_id} and player_current.city_id = city.id and research_center = 1;")
    if int(checkRcAmount[0])>1 and checkLocation is not None:
        data = SQL.queryAll(f"select id from city where research_center = 1;")
        data = [i[0] for i in data]
        data.remove(basic.playerId_to_cityId(player_id))
        return data
    else:
        return [False]

# Return the dictionary of available city id that for each move type, player can move into.
def moveCheck(player_id):
    move_dict = {'drive': moveDriveInfo(player_id),
                 'fly': moveFlyInfo(player_id),
                 'jet': moveJetInfo(player_id),
                 'rc': moveRcInfo(player_id)
                 }
    return move_dict

def move_check_info(player_id):

    data = moveDriveInfo(player_id)
    driveData = []
    for member in data:
        driveData.append(
            {
                'id': member,
                'location': basic.getCityLccationFromId(member)
            })

    data = moveFlyInfo(player_id)
    flyData = []
    if data:
        for member in data:
            flyData.append(
                {
                    'id': member,
                    'location': basic.getCityLccationFromId(member)
                })

    data = moveRcInfo(player_id)
    rcData = []
    if data[0]:
        for member in data:
            rcData.append(
                {
                    'id': member,
                    'location': basic.getCityLccationFromId(member)
                })
    else: rcData = False

    move_dict ={
        'drive': driveData,
        'fly': flyData,
        'jet': moveJetInfo(player_id),
        'rc': rcData
    }

    return move_dict

def player_own_info(player_id):
    data = SQL.queryAll(f"select card_id from player_own where player_id = {player_id}")
    return_data = []
    for i in data:
        city = SQL.queryOne(f"select city_name, virus from city where id = {i[0]}; ")
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
    city_card = moveJetInfo(player_id)
    if city_card:
        city_check = SQL.queryOne(f"select research_center from city where id = {city_card};")
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
    card_check = SQL.queryAll(f"select virus,id from player_own, city "
                               f"where player_id = {player_id} and card_id = city.id order by virus;")
    rc_check = SQL.queryOne(f"select research_center from city, player_current "
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