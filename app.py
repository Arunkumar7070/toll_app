from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/add_user')
def add_user():
    return render_template('add_user.html')

@app.route('/add_user_into_db', methods=['POST'])
def add_user_into_db():
    if request.method == 'POST':
        carno = request.form['carno']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        amount = request.form['amount']
        conn=sqlite3.connect('datbase/toll_management.db')
        cursor=conn.cursor()
        cursor.execute("INSERT INTO users (carno, email, password, name, balance) VALUES (?, ?, ?, ?, ?)", (carno, email, password, username, amount))
        conn.commit()
        conn.close()
        message="registeres successfully"
        return render_template('result.html',msg=message)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/login_detail", methods=["POST"])
def login_detail():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn=sqlite3.connect('datbase/toll_management.db')
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (username, password))
        row=cursor.fetchone()
        if row:
            conn.close()
            return render_template('login_user_detail.html',data=row)
        else:
            conn.close()
            message="invalid username or password"
            return render_template('result.html',msg=message)

@app.route("/system")
def system():
    return render_template('system_pwd_check.html') 

@app.route("/system_pwd_check_valid", methods=["POST"])
def system_pwd_check_valid():
    if request.method == 'POST':
        password = request.form['password']
        if password=="system":
            return render_template('system_input.html')
        else:
            message="invalid password"
            return render_template('result.html',msg=message)

@app.route("/system_detail", methods=["POST"])
def system_detail():
    if request.method == 'POST':
        carno = request.form['carno']
        amount = request.form['amount']
        date = request.form['date']
        conn=sqlite3.connect('datbase/toll_management.db')
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users WHERE carno=?", (carno,))
        row=cursor.fetchone()
        if row:
            balance=row[4]
            balance=balance-int(amount)
            cursor.execute("INSERT INTO transactions (carno, amount, date) VALUES (?, ?, ?)", (carno, amount, date))
            cursor.execute("UPDATE users SET balance=? WHERE carno=?", (balance,carno))
            conn.commit()
            conn.close()
            message="toll crossed successfully"
            return render_template('result.html',msg=message)
        else:
            conn.close()
            message="invalid carno"
            return render_template('result.html',msg=message)


@app.route("/admin")
def admin():
    return render_template('admin.html')
        
@app.route("/admin_detail", methods=["POST"])
def admin_detail():
    if request.method == 'POST':
        password = request.form['password']
        if password=="admin":
            conn=sqlite3.connect('datbase/toll_management.db')
            cursor=conn.cursor()    
            cursor.execute("SELECT * FROM transactions")
            rows=cursor.fetchall()
            return render_template('admin_detail_display.html',data=rows)
            conn.close()
        else:
            message="invalid password"
            return render_template('result.html',msg=message)



@app.route("/print")
def user_detail():
    conn=sqlite3.connect('datbase/toll_management.db')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows=cursor.fetchall()
    return render_template('user_detail.html',data=rows)



if __name__ == '__main__':
    app.run(debug=True)
