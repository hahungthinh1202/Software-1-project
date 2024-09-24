
import update_func
import mysql.connector



"""
from flask import Flask, request, render_template
app = Flask(__name__)
@app.route('/')
def main():
    mylist = [20, 20 , 3]
    return render_template('main.html', mylist=mylist,debug=True)
if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
"""
update_func.reset_infection_deck()
print(update_func.set_up_infection_deck())