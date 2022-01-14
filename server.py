from flask import Flask, request, render_template

import sqlite3
from sqlite3 import Error


import ocr
import setCategory

from datetime import datetime

database = 'cashflowManagement.db'


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def insertIntoRegister(dataValue):
    conn = create_connection(database)
    with conn:
        sql = """ INSERT INTO register(username,pswd)
              VALUES(?,?) """
        cur = conn.cursor()
        cur.execute(sql, dataValue)
        conn.commit()
        print('user id:', cur.lastrowid)


def insertIntoData(dataValue):
    conn = create_connection(database)
    with conn:
        sql = """ INSERT INTO data(username,category,actual_item,cost,date)
              VALUES(?,?,?,?,?) """
        cur = conn.cursor()
        cur.execute(sql, dataValue)
        conn.commit()
        print('item id:', cur.lastrowid)


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route("/")
def test():
    return render_template("test.html")


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pswd = request.form['pswd']
        userData = (username, pswd)
        print(userData)
        insertIntoRegister(userData)
        return "cool"
    else:
        return "weird"


@app.route('/form', methods=['POST'])
def form():
    if request.method == 'POST':
        username = request.form['username']
        actual_item = request.form['actual_item']
        cost = request.form['cost']
        date = datetime.today().strftime('%d-%m-%Y')
        category = request.form['category']
        if category == 'something weird':
            category = setCategory.run_model(actual_item)
        formData = (username, category, actual_item, cost, date)
        print(formData)
        insertIntoData(formData)
        return "cool"
    else:
        return "weird"


@app.route('/image', methods=['POST'])
def image():
    if request.method == 'POST':
        imagefile = request.files.get('imagefile', '')
        imagefile.save('img1.jpg')
        result = ocr.runOCR('img1.jpg')
        username = request.form['username']
        for i in range(len(result[0])):
            #   print(result[0][i], result[1][i])
            actual_item = result[0][i]
            cost = result[1][i]
            category = setCategory.run_model(actual_item)
            date = datetime.today().strftime('%d-%m-%Y')
            formData = (username, category, actual_item, cost, date)
            insertIntoData(formData)
        return "cool"
    else:
        return "weird"


@app.route('/sms', methods=['POST'])
def sms():
    if request.method == 'POST':
        username = request.form['username']
        sms = request.form['sms']
        return "cool"
    else:
        return "weird"


if __name__ == '__main__':
    app.run(debug=True)
