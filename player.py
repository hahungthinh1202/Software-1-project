import SQL
import basic
import infection
from prettytable import PrettyTable


def draw(player_id):
    data = SQL.query_all(f"select city_id from player_card_current limit 1;")
    if not data:
        return False
    else:
        data = data[-1][0]
        if int(data)<0 :
            print(f"player draw epidemic card")
            infection.epidemic()
        else:
            print(f"player draw {basic.cityId_to_cityName(data)} card")
            SQL.update(f"insert into player_own values({player_id},{data});")
        SQL.update(f"delete from player_card_current where city_id = {data};")
        return True

def discard(player_id,card_id):
    SQL.update(f"delete from player_own where player_id = {player_id} and card_id = {card_id};")

def display(player_id):
    my_table = PrettyTable()
    data = SQL.query_all(f"select city_name,virus from player_own,city_db "
                         f"where player_id = {player_id} and card_id = id order by virus;")
    for i in data:
        my_table.add_column(i[0], [i[1]])
    print(my_table)
    return my_table