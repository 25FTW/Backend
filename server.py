from flask import Flask, request, render_template
from flask import jsonify
import sqlite3
from sqlite3 import Error


import ocr
import setCategory2

from datetime import datetime

database = 'cashflowManagement.db'


def checkBalance(username):
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT cost FROM data")
    x = []
    for row in cur.fetchall():
        x.append(float(row[0]))
    s = sum(x)
    print("in budget s = ", s)
    cur.execute(
        'SELECT COUNT(*) from budgetTable where username = ?', (username,))
    cur_result = cur.fetchone()
    if cur_result == 0:
        z = 1000
        print("in budget z = ", z)
        if s > z:
            cur.execute(""" INSERT INTO logs(username,log)
                  VALUES(?,?) """, (username, "budget exceeded"))
            conn.commit()
            print('notification id:', cur.lastrowid)
            return "budget crossed"
        elif s == z or s+500 >= z:
            cur.execute(""" INSERT INTO logs(username,log)
                  VALUES(?,?) """, (username, "close to exceeding the budget"))
            conn.commit()
            print('notification id:', cur.lastrowid)
            return "close to exceeding the budget"
        else:
            cur.execute(""" INSERT INTO logs(username,log)
                  VALUES(?,?) """, (username, "transaction was under the budget"))
            conn.commit()
            print('notification id:', cur.lastrowid)
            return "cool"
    cur.execute("SELECT budget FROM budgetTable WHERE username = ?", (username,))
    z = float(cur.fetchall()[0][0])
    print("in budget z = ", z)
    if s > z:
        cur.execute(""" INSERT INTO logs(username,log)
              VALUES(?,?) """, (username, "budget exceeded"))
        conn.commit()
        print('notification id:', cur.lastrowid)
        return "budget crossed"
    elif s == z or s+500 >= z:
        cur.execute(""" INSERT INTO logs(username,log)
              VALUES(?,?) """, (username, "close to exceeding the budget"))
        conn.commit()
        print('notification id:', cur.lastrowid)
        return "close to exceeding the budget"
    else:
        cur.execute(" INSERT INTO logs(username,log) VALUES(?,?) ",
                    (username, "transaction was under the budget"))
        conn.commit()
        print('notification id:', cur.lastrowid)
        return "cool"


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
        cur.execute(" INSERT INTO logs(username,log) VALUES(?,?) ",
                    (dataValue[0], """Welcome, new user. Thankyou for choosing us."""))
        conn.commit()
        print('notification id:', cur.lastrowid)


def insertIntoData(dataValue):
    conn = create_connection(database)
    with conn:
        sql = """ INSERT INTO data(username,category,actual_item,cost,date)
              VALUES(?,?,?,?,?) """
        cur = conn.cursor()
        cur.execute(sql, dataValue)
        conn.commit()
        print('item id:', cur.lastrowid)
        cur.execute(""" INSERT INTO logs(username,log)
              VALUES(?,?) """, (dataValue[0], """A new Transaction was done."""))
        conn.commit()
        print('notification id:', cur.lastrowid)


def insertIntoBudget(dataValue):
    conn = create_connection(database)
    with conn:
        sql = """ INSERT INTO budgetTable(username,budget)
              VALUES(?,?) """
        cur = conn.cursor()
        cur.execute(sql, dataValue)
        conn.commit()
        print('budget id:', cur.lastrowid)
        cur.execute(""" INSERT INTO logs(username,log)
              VALUES(?,?) """, (dataValue[0], "You added your budget!"))
        conn.commit()
        print('notification id:', cur.lastrowid)


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
        print(jsonify([1, 2, 3, 4, 5]))
        return jsonify(["cool"])
    else:
        return "weird"


@app.route('/getLogs', methods=['POST'])
def getLogs():
    if request.method == 'POST':
        username = request.form['username']
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("SELECT log FROM logs where username=?", (username,))
        x = [row[0] for row in cur.fetchall()]
        '''v = {}
        for i in range(x)'''
        return jsonify(x[::-1])
    else:
        return "weird"


@app.route('/setBudget', methods=['POST'])
def setBudget():
    if request.method == 'POST':
        budget = request.form['budget']
        username = request.form['username']
        budgetData = (username, budget)
        insertIntoBudget(budgetData)
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
            category = setCategory2.run_model(actual_item)
        formData = (username, category, actual_item, cost, date)
        print(formData)
        insertIntoData(formData)
        v = checkBalance(username)
        return v
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
            category = setCategory2.run_model(actual_item.lower())
            date = datetime.today().strftime('%d-%m-%Y')
            formData = (username, category, actual_item, cost, date)
            print(formData)
            insertIntoData(formData)
        return "cool"
    else:
        return "weird"


@app.route('/sms', methods=['POST'])
def sms():
    if request.method == 'POST':
        username = request.form['username']
        sms = request.form['sms']
        actual_item = request.form['actual_item']
        category = request.form['category']
        return "cool"
    else:
        return "weird"


if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True)
