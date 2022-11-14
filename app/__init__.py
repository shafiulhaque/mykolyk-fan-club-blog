from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session
from flask import redirect

from db import *
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O  
import os

app = Flask(__name__)

app.secret_key = os.urandom(32)

create_tables()
create_user('shaf','bruh1234')
create_user('akitiss','horanghae')
            

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
    if request.method == 'POST':
        if not login_check(request.form['username'], request.form['password']):
            return render_template('login.html', error="Incorrect password or username")
        else: 
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            return redirect('/response')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect('/response')
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        if (check_user_exist(request.form['username'])):
            return render_template('signup.html', error ="Username already in use")
        if (request.form['password'] == ""):
            return render_template('signup.html', error ="Blank password")
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        create_user(session['username'], session['password'])
    return redirect('/response')

@app.route("/logout", methods=['GET', 'POST'])
def disp_logoutpage():
    session.pop('username')
    session.pop('password')
    return redirect('/')

@app.route("/response", methods=['GET', 'POST'])
def mainpage():
    return render_template('response.html', username = session['username'])




if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
