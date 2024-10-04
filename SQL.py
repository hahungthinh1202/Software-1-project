import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1202',
    database='pandemic'
)

def query_one(command):
    cursor = connection.cursor()
    cursor.execute(command)
    data = cursor.fetchone()
    discard = cursor.fetchall()
    return data

def query_all(command):
    cursor = connection.cursor()
    cursor.execute(command)
    return cursor.fetchall()

def update(command):
    cursor = connection.cursor()
    cursor.execute(command)
    connection.commit()


