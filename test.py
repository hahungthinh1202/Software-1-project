from prettytable import PrettyTable
from sqlalchemy.sql.operators import truediv
import player
import action
import basic
import infection
from basic import city_name_to_id, return_player_coordinate
import prettytable

#basic.game_init(6,2)
data_list = basic.return_game_info()

print(type(data_list[0]))

