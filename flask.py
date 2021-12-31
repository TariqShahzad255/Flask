from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Asif24121999'
app.config['MYSQL_DB'] = 'LAB6'
mysql = MySQL(app)

@app.route("/")
def mainpage():
    return redirect('/signup')
    return render_template('mainpage.html')

@app.route("/", methods=['GET', 'POST'])
def Signup():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        password = userDetails['password']
        confirm_password = userDetails['confirm_password']
        if password==confirm_password:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO User(name, password) VALUES(%s, %s)", (name, password))
            mysql.connection.commit()
            cur.close()
            return redirect('/login')
        else:
            message="Passwords do not match"
            return render_template('Signup.html', message=message)
    return render_template('Signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM User WHERE name=%s and password=%s",(name, password))
        if result>0:
            return redirect('/posts')
        else:
            message="Invalid Credentials"
            return render_template('Login.html', message=message)
    return render_template('Login.html')

@app.route("/posts")
def posts():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM User")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template("Posts.html", user=userDetails) 