import SQL
import basic
import infection
from prettytable import PrettyTable

# This module include all the functions that are related to player interaction with player card

# This function simulate drawing a card, this could be either an epidemic card (bad news) or a city card.
# First get the top card id from the player_card_current table and then check
# If a negative id card is draw (epidemic card) an epidemic from infection module is executed
# else update the player_own table by inserting a new row of card id and player id
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

# This function simply delete a specific row from player_own database
def discard(player_id,card_id):
    SQL.update(f"delete from player_own where player_id = {player_id} and card_id = {card_id};")

# This function display all the card that the player id (in parameter) currently own.
# For a better looking card list, I use pretty table module to show
def display(player_id):
    my_table = PrettyTable()
    data = SQL.query_all(f"select city_name,virus from player_own,city_db "
                         f"where player_id = {player_id} and card_id = id order by virus;")
    for i in data:
        my_table.add_column(i[0], [i[1]])
    print(my_table)
    return my_table