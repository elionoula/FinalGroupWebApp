from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
import pymysql
import re
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

app = Flask(__name__)

mysql = MySQL()

app.secret_key = '1a2b3c4d5e'

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'pythonlogin'
mysql.init_app(app)

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    """Description: Function to login and read render the index.html page.
                    If incorrect login information is provided will be prompted
                    with an error message.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password has been entered!'
    return render_template('index.html', msg=msg)


@app.route('/')
def home():
    """Description: Function to render the home.html and bring you to the welcome page.
                    If other then will be directed to the index.html file.
    """
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Description: Function to register a new user to the website.
                    If the form is filled out incorrectly it will tell the user
                    to correctly fill it out.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (fullname, username, password, email))
            conn.commit()
            msg = 'You have successfully registered!'
            sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            from_email = Email("ac295@njit.edu")  # Change to your verified sender
            to_email = To(email)  # Change to your recipient
            subject = "Verified Sign Up for IS601 Project"
            content = Content("text/plain", "Thank you for signing up!")
            mail = Mail(from_email, to_email, subject, content)
            # Get a JSON-ready representation of the Mail object
            mail_json = mail.get()
            # Send an HTTP POST request to /mail/send
            response = sg.client.mail.send.post(request_body=mail_json)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route('/profile')
def profile():
    """Description: Function to display profile containing information
                    regarding to each user's profile.
    """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """Description: Function to logout the user.
    """
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)