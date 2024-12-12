import SQL
import infection


# This module include all the functions that are related to player interaction with player card

# This function simulate drawing a card, this could be either an epidemic card (bad news) or a city card.
# First get the top card id from the player_card_current table and then check
# If a negative id card is draw (epidemic card) an epidemic from infection module is executed
# else update the player_own table by inserting a new row of card id and player id
def draw(player_id):
    data = SQL.query_all(f"select city_id from player_card_current limit 1;")
    returnData = False
    if not data:
        return returnData
    else:
        data = data[-1][0]
        if int(data)<0 :
            print(f"player draw epidemic card")
            returnData = {
                'eventType' : 'cardDrawEpidemic',
                'story' : infection.epidemic()
            }
        else:
            SQL.update(f"insert into player_own values({player_id},{data});")
            cityName = SQL.query_one(f"select city_name from city where id = {int(data)};")[0]
            returnData = {
                'eventType' : 'cardDraw',
                'story': f"You have drawn<n>{cityName} card"
            }
        SQL.update(f"delete from player_card_current where city_id = {data};")
        return returnData

# This function simply delete a specific row from player_own database
def discard(player_id,card_id):
    SQL.update(f"delete from player_own where player_id = {player_id} and card_id = {card_id};")

