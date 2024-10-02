import random
import infection
from os.path import curdir
import basic
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1202',
    database='pandemic'
)

def draw(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select city_id from player_card_current limit 1;")
    data = cursor.fetchall()
    data = data[-1][0]

    if int(data)<0 :
        infection.epidemic()
    else:
        cursor.execute(f"insert into player_own values({player_id},{data});")

    cursor.execute(f"delete from player_card_current where city_id = {data};")
    connection.commit()

def discard(player_id,card_id):
    cursor = connection.cursor()
    cursor.execute(f"delete from player_own where player_id = {player_id} and card_id = {card_id};")
    connection.commit()

def display(player_id):
    cursor = connection.cursor()
    cursor.execute(f"select city_name,virus from player_own,city_db where player_id = {player_id} and card_id = id order by virus;")
    data = cursor.fetchall()
    return data