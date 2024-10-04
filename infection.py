import mysql.connector
import random

import SQL
import basic

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1202',
    database='pandemic'
)
#shuffle all 48 card together
def reset_deck():
    SQL.update("delete from infection_deck;")
    order = list(range(1,49))
    random.shuffle(order)
    for i in order:
        SQL.update(f"insert into infection_deck values ({i});")

#first reset deck, pick 3 card to put 3 cube, 2 cards to put 2 cube and 1 card to put 1 cube
#return dictionary

def init():
    reset_deck()
    reset_discard()
    three_cube = select_top_three()
    two_cube = select_top_three()
    one_cube = select_top_three()
    return {3: three_cube,2: two_cube,1: one_cube}

#move one card from active deck to discard pile
def discard(card_id):
    SQL.update(f"insert into infection_discard values ({card_id});")
    SQL.update(f"delete from infection_deck where city_id = {card_id};")

#remove all card data from discard pile
def reset_discard():
    SQL.update("delete from infection_discard;")

#return the top card of the active deck
def select_top():
    data = SQL.query_all(f"select * from infection_deck;")
    return data[-1][0]


#return the bottom card of the active deck
def select_bottom():
    data = SQL.query_all(f"select * from infection_deck limit 1;")
    return data[-1][0]

#shuffle all card from discard pile and put back on top of the active deck
def return_discard():
    data = SQL.query_all(f"select * from infection_discard;")
    data_out = []
    for i in data:
        data_out.append(i[0])
    random.shuffle(data_out)
    for i in data_out:
        SQL.update(f"insert into infection_deck values ({i});")
    reset_discard()
    return data_out

#pick 3 top card from active deck and put into the discard pile
def select_top_three():
    data = SQL.query_all(f"select city_id, virus from infection_deck right join city_db on id = city_id limit 3;")
    data_out = []
    for i in data:
        data_out.append(i)
        SQL.update(f"delete from infection_deck where city_id = {i[0]};")
        discard(i[0])
    return data_out

def epidemic():
    city_id = select_bottom()
    virus = SQL.query_one(f"select virus from city_db where id = {city_id};")
    basic.put_cube(city_id, virus[0],3)
    discard(city_id)
    print(f"Epidemic happen at {basic.cityId_to_cityName(city_id)}!")
    SQL.update(f"update game_current set infection_track = infection_track + 1;")
    return_discard()

def infect():
    infection_rate = basic.return_game_info()[0]
    card_draw = 2
    if infection_rate in [3,4]:
        card_draw = 3
    elif infection_rate >= 5:
        card_draw = 4
    for i in range(card_draw):
        city_id = select_top()
        print(f"Infect state! Disease level at {basic.cityId_to_cityName(city_id)} increased by 1")
        virus = SQL.query_one(f"select virus from city_db where id = {city_id};")
        basic.put_cube(city_id, virus[0], 1)
        discard(city_id)


