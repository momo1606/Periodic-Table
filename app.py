from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'jai hind doston'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'santagifts1'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        cursor.execute('call loginproc(%s,%s)',(username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        print(5656)
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            cursor.execute('call userlog(%s)',(username, ))
            mysql.connection.commit()
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'profession' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        profession=request.form['profession']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
        #mysql.connection.commit()
        '''cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        account = cursor.fetchone()
        print("ma nigga")
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
            print(msg)'''
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            try:
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (username, password, email, profession))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
            except:
                msg = 'Account already exists!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
@app.route( '/pythonlogin/def.html')
def details():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (1,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (1,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (1,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def2.html')
def details2():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (2,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (2,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (4,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def2.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def3.html')
def details3():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (3,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (3,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (7,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def3.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def4.html')
def details4():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (4,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (4,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (9,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def4.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def5.html')
def details5():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (5,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (5,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (11,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def5.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def6.html')
def details6():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (6,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (6,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (12,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def6.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def7.html')
def details7():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (7,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (7,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (14,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def7.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def8.html')
def details8():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (8,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (8,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (16,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def8.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def9.html')
def details9():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (9,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (9,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (19,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def9.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def10.html')
def details10():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (10,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (10,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (20,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def10.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def11.html')
def details11():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (11,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (11,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (23,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def11.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def12.html')
def details12():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (12,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (12,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (24,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def12.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def13.html')
def details13():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (13,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (13,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (27,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def13.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def14.html')
def details14():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (14,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (14,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (28,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def14.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def15.html')
def details15():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (15,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (15,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (31,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def15.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def16.html')
def details16():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (16,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (16,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (32,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def16.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def17.html')
def details17():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (17,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (17,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (35,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def17.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def18.html')
def details18():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (18,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (18,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (39,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def18.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def19.html')
def details19():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (19,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (19,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (40,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def19.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def20.html')
def details20():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (20,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (20,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (40,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def20.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def21.html')
def details21():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (21,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (21,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (45,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def21.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def22.html')
def details22():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (22,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (22,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (48,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def22.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def23.html')
def details23():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (23,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (23,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (51,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def23.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def24.html')
def details24():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (24,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (24,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (52,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def24.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def25.html')
def details25():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (25,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (25,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (55,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def25.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def26.html')
def details26():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (26,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (26,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (56,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def26.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def27.html')
def details27():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (27,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (27,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (59,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def27.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def28.html')
def details28():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (28,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (28,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (59,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def28.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def29.html')
def details29():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (29,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (29,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (63,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def29.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def30.html')
def details30():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (30,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (30,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (65,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def30.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def31.html')
def details31():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (31,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (31,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (70,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def31.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def32.html')
def details32():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (32,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (32,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (73,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def32.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def33.html')
def details33():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (33,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (33,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (75,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def33.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def34.html')
def details34():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (34,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (34,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (79,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def34.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def35.html')
def details35():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (35,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (35,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (80,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def35.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def36.html')
def details36():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (36,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (36,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (84,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def36.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def37.html')
def details37():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (37,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (37,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (85,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def37.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def38.html')
def details38():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (38,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (38,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (88,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def38.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def39.html')
def details39():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (39,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (39,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (89,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def39.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def40.html')
def details40():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (40,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (40,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (91,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def40.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def41.html')
def details41():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (41,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (41,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (93,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def41.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def42.html')
def details42():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (42,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (42,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (96,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def42.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def43.html')
def details43():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (43,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (43,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (98,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def43.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def44.html')
def details44():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (44,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (44,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (101,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def44.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def45.html')
def details45():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (45,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (45,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (103,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def45.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def46.html')
def details46():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (46,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (46,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (106,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def46.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def47.html')
def details47():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (47,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (47,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (108,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def47.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def48.html')
def details48():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (48,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (48,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (112,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def48.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def49.html')
def details49():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (49,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (49,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (115,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def49.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def50.html')
def details50():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (50,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (50,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (119,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def50.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def51.html')
def details51():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (51,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (51,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (122,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def51.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def52.html')
def details52():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (52,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (52,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (127,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def52.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def53.html')
def details53():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (53,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (53,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (128,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def53.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def54.html')
def details54():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (54,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (54,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (131,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def54.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def55.html')
def details55():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (55,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (55,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (133,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def55.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def56.html')
def details56():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (56,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (56,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (137,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def56.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def57.html')
def details57():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (57,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (57,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (139,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def57.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def58.html')
def details58():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (58,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (58,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (140,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def58.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def59.html')
def details59():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (59,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (59,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (141,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def59.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def60.html')
def details60():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (60,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (60,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (144,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def60.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def61.html')
def details61():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (61,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (61,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (145,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def61.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def62.html')
def details62():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (62,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (62,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (150,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def62.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def63.html')
def details63():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (63,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (63,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (152,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def63.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def64.html')
def details64():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (64,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (64,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (157,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def64.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def65.html')
def details65():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (65,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (65,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (159,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def65.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def66.html')
def details66():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (66,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (66,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (162,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def66.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def67.html')
def details67():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (67,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (67,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (165,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def67.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def68.html')
def details68():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (68,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (68,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (167,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def68.html', data=data ,data2=data2, data3=data3)
@app.route( '/pythonlogin/def69.html')
def details69():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (69,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (69,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (169,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def69.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def70.html')
def details70():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (70,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (70,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (173,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def70.html', data=data ,data2=data2, data3=data3)



@app.route( '/pythonlogin/def71.html')
def details71():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (71,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (71,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (175,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def71.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def72.html')
def details72():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (72,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (72,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (178,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def72.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def73.html')
def details73():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (73,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (73,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (181,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def73.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def74.html')
def details74():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (74,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (74,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (184,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def74.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def75.html')
def details75():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (75,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (75,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (186,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def75.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def76.html')
def details76():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (76,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (76,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (190,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def76.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def77.html')
def details77():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (77,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (77,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (192,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def77.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def78.html')
def details78():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (78,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (78,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (195,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def78.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def79.html')
def details79():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (79,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (79,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (197,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def79.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def80.html')
def details80():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (80,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (80,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (201,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def80.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def81.html')
def details81():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (81,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (81,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (204,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def81.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def82.html')
def details82():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (82,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (82,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (207,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def82.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def83.html')
def details83():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (83,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (83,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (209,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def83.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def84.html')
def details84():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (84,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (84,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (209,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def84.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def85.html')
def details85():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (85,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (85,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (210,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def85.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def86.html')
def details86():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (86,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (86,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (222,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def86.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def87.html')
def details87():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (87,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (87,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (223,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def87.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def88.html')
def details88():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (88,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (88,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (226,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def88.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def89.html')
def details89():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (89,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (89,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (227,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def89.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def90.html')
def details90():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (90,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (90,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (232,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def90.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def91.html')
def details91():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (91,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (91,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (231,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def91.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def92.html')
def details92():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (92,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (92,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (238,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def92.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def93.html')
def details93():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (93,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (93,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (237,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def93.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def94.html')
def details94():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (94,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (94,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (244,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def94.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def95.html')
def details95():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (95,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (95,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (243,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def95.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def96.html')
def details96():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (96,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (96,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (247,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def96.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def97.html')
def details97():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (97,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (97,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (247,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def97.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def98.html')
def details98():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (98,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (98,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (251,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def98.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def99.html')
def details99():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (99,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (99,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (252,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def99.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def100.html')
def details100():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (100,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (100,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (257,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def100.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def101.html')
def details101():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (101,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (101,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (258,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def101.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def102.html')
def details102():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (102,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (102,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (259,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def102.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def103.html')
def details103():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (103,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (103,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (266,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def103.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def104.html')
def details104():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (104,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (104,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (267,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def104.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def105.html')
def details105():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (105,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (105,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (268,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def105.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def106.html')
def details106():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (106,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (106,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (269,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def106.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def107.html')
def details107():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (107,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (107,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (270,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def107.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def108.html')
def details108():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (108,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (108,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (270,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def108.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def109.html')
def details109():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (109,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (109,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (278,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def109.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def110.html')
def details110():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (110,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (110,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (281,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def110.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def111.html')
def details111():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (111,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (111,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (282,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def111.html', data=data ,data2=data2, data3=data3)



@app.route( '/pythonlogin/def112.html')
def details112():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (112,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (112,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (285,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def112.html', data=data ,data2=data2, data3=data3)



@app.route( '/pythonlogin/def113.html')
def details113():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (113,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (113,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (286,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def113.html', data=data ,data2=data2, data3=data3)



@app.route( '/pythonlogin/def114.html')
def details114():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (114,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (114,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (289,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def114.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def115.html')
def details115():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (115,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (115,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (290,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def115.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def116.html')
def details116():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (116,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (116,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (293,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def116.html', data=data ,data2=data2, data3=data3)


@app.route( '/pythonlogin/def117.html')
def details117():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (117,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (117,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (294,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def117.html', data=data ,data2=data2, data3=data3)

@app.route( '/pythonlogin/def118.html')
def details118():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('call dispGRP(%s)', (118,))
    data = cursor.fetchone()
    print(data)
    data2=None
    data3=None
    try:
        cursor.execute('call dispISOT(%s)', (118,))
        data2=cursor.fetchall()
        print(data2)
        cursor.execute('call dispISOB(%s)', (294,))
        data3 = cursor.fetchall()
        print(data3)
    except:
        pass
    return render_template( 'def118.html', data=data ,data2=data2, data3=data3)

if __name__ == '__main__':
    app.run()
