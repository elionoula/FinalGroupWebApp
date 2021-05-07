from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
import pymysql
import re

app = Flask(__name__)

mysql = MySQL()

app.secret_key = '1a2b3c4d5e'

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'pythonlogin'
mysql.init_app(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)