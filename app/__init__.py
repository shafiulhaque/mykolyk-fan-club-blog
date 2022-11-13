from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session
from flask import redirect

from db import create_tables, check_user_exist
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O  

app = Flask(__name__)

mydict = {}

app.secret_key = 'hi'
username = 'bruh'
password = 'bruh2'

@app.route('/')
def show():
    if 'username' in session: #if user is already in session, will go to response page logged in
        return render_template('response.html', username = session['username'])
    return render_template('main.html') #if user isn't already logged in go to login page

@app.route('/login', methods=['GET', 'POST'])
def disp_loginpage():
    if 'username' in session:
        return redirect('/response')
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form['username']
    pw = request.form['password']
    if request.method == 'POST' and user == username:
        if pw == password:
            session['username'] = user
            return redirect('/response')
        return render_template('login.html', error="Error: Incorrect Password") #in case the password is incorrect
    return render_template('login.html', error ="Error: Incorrect Username") #in case the username is incorrect

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect('/response')
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        session['username'] = request.form['username']
    return redirect('/response')

@app.route("/logout", methods=['GET', 'POST'])
def disp_logoutpage():
    session.pop('username')
    return redirect('/')

@app.route("/response", methods=['GET', 'POST'])
def mainpage():
    return render_template('response.html', username = session['username'])




if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
