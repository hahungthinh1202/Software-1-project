import mysql.connector
import random

import basic

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1202',
    database='pandemic'
)
#shuffle all 48 card together
def reset_deck():
    cursor = connection.cursor()
    cursor.execute("delete from infection_deck;")
    connection.commit()
    order = list(range(1,49))
    random.shuffle(order)
    for i in order:
        cursor.execute(f"insert into infection_deck values ({i});")
        connection.commit()

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
    cursor = connection.cursor()
    cursor.execute(f"insert into infection_discard values ({card_id});")
    cursor.execute(f"delete from infection_deck where city_id = {card_id};")
    connection.commit()

#remove all card data from discard pile
def reset_discard():
    cursor = connection.cursor()
    cursor.execute("delete from infection_discard;")
    connection.commit()

#return the top card of the active deck
def select_top():
    cursor = connection.cursor()
    cursor.execute(f"select * from infection_deck;")
    data = cursor.fetchall()
    return data[-1][0]


#return the bottom card of the active deck
def select_bottom():
    cursor = connection.cursor()
    cursor.execute(f"select * from infection_deck limit 1;")
    data = cursor.fetchall()
    return data[-1][0]

#shuffle all card from discard pile and put back on top of the active deck
def return_discard():
    cursor = connection.cursor()
    cursor.execute(f"select * from infection_discard;")
    data = cursor.fetchall()
    data_out = []
    for i in data:
        data_out.append(i[0])
    random.shuffle(data_out)
    for i in data_out:
        cursor.execute(f"insert into infection_deck values ({i});")
    connection.commit()
    reset_discard()
    return data_out

#pick 3 top card from active deck and put into the discard pile
def select_top_three():
    cursor = connection.cursor()
    cursor.execute(f"select city_id, virus from infection_deck right join city_db on id = city_id limit 3;")
    data = cursor.fetchall()
    data_out = []
    for i in data:
        data_out.append(i)
        cursor.execute(f"delete from infection_deck where city_id = {i[0]};")
        connection.commit()
        discard(i[0])
    return data_out

def epidemic():
    cursor = connection.cursor()
    city_id = select_bottom()
    cursor.execute(f"select virus from city_db where id = {city_id};")
    virus = cursor.fetchone()[0]
    basic.put_cube(city_id, virus,3)
    discard(city_id)
    print("epidemic happen! new city", basic.city_id_to_name(city_id))
    cursor.execute(f"update game_current set infection_track = infection_track + 1;")
    return_discard()

def infect():
    cursor = connection.cursor()
    infection_rate = basic.return_game_info()[0]
    card_draw = 2
    if infection_rate in [3,4]:
        card_draw = 3
    elif infection_rate >= 5:
        card_draw = 4
    for i in range(card_draw):
        city_id = select_top()
        print(f"Infect state! Disease level at {basic.city_id_to_name(city_id)} increased by 1")
        cursor.execute(f"select virus from city_db where id = {city_id};")
        virus = cursor.fetchone()[0]
        basic.put_cube(city_id, virus, 1)
        discard(city_id)

    connection.commit()

