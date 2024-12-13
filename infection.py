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

def resetDeck():
    SQL.update("delete from infection_deck;")
    order = list(range(1,49))
    random.shuffle(order)
    for i in order:
        SQL.update(f"insert into infection_deck values ({i});")

#first reset deck, pick 3 card to put 3 cube, 2 cards to put 2 cube and 1 card to put 1 cube
#return dictionary

def initialize():
    resetDeck()
    resetDiscardDeck()
    three_cube = SelectTopThreeCard()
    two_cube = SelectTopThreeCard()
    one_cube = SelectTopThreeCard()
    return {3: three_cube,2: two_cube,1: one_cube}

#move one card from active deck to discard pile
def discard(card_id):
    SQL.update(f"insert into infection_discard values ({card_id});")
    SQL.update(f"delete from infection_deck where city_id = {card_id};")

#remove all card data from discard pile
def resetDiscardDeck():
    SQL.update("delete from infection_discard;")

#return the top card of the active deck
def selectTopCard():
    data = SQL.queryAll(f"select * from infection_deck;")
    return data[-1][0]

#return the bottom card of the active deck
def selectBottomCard():
    data = SQL.queryAll(f"select * from infection_deck limit 1;")
    return data[-1][0]

#shuffle all card from discard pile and put back on top of the active deck
def returnAllDiscardCard():
    data = SQL.queryAll(f"select * from infection_discard;")
    dataOut = []
    for i in data:
        dataOut.append(i[0])
    random.shuffle(dataOut)
    for i in dataOut:
        SQL.update(f"insert into infection_deck values ({i});")
    resetDiscardDeck()
    return dataOut

#pick 3 top card from active deck and put into the discard pile
def SelectTopThreeCard():
    data = SQL.queryAll(f"select city_id, virus from infection_deck right join city on infection_deck.city_id = city.id limit 3;")
    dataOut = []
    for i in data:
        dataOut.append(i)
        SQL.update(f"delete from infection_deck where city_id = {i[0]};")
        discard(i[0])
    return dataOut

def epidemic():
    city_id = selectBottomCard()
    news_title = SQL.queryOne(f"select story from event where id  = {random.randint(1, 3)};")
    news_title = news_title[0].replace('{city_name}', SQL.queryOne(f"select city_name from city where id = {city_id};")[0])
    print(news_title)
    virus = SQL.queryOne(f"select virus from city where id = {city_id};")
    basic.put_cube(city_id, virus[0], 3)
    discard(city_id)
    SQL.update(f"update game_current set infection_track = infection_track + 1;")
    returnAllDiscardCard()
    return news_title




def infect():
    infection_rate = basic.returnGameInfo()['infection_track']
    newlyInfectedCity = []
    card_draw = 2
    if infection_rate in [3,4]:
        card_draw = 3
    elif infection_rate >= 5:
        card_draw = 4
    for i in range(card_draw):
        city_id = selectTopCard()
        virus = SQL.queryOne(f"select virus from city where id = {city_id};")
        basic.put_cube(city_id, virus[0], 1)
        discard(city_id)
        cityName = SQL.queryOne(f"select city_name from city where id = {city_id};")[0]
        newlyInfectedCity.append({
            'eventType' : "infectCity",
            'story': cityName + " has been infected<n>by " + virus[0] + " virus!"
        })
    return newlyInfectedCity



