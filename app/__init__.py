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
            

@app.route('/', methods=['GET', 'POST'])
def show():
    if 'username' in session: #if user is already in session, will go to response page logged in
        return redirect('/response')
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
        if (request.form['username'].isspace()):
            return render_template('signup.html', error ="Blank username")
        if (check_user_exist(request.form['username'])):
            return render_template('signup.html', error ="Username already in use")
        if (request.form['password'].isspace()):
            return render_template('signup.html', error ="Blank password")
        if (len(request.form['password']) <= 7):
            return render_template('signup.html', error ="Password is too short")
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
    return render_template('response.html', username = session['username'], all_blogs = get_all_blogs())

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'GET':
        return render_template('create.html', username = session['username'])
    if request.method == 'POST':
        if (request.form['title'].isspace() or len(request.form['title']) == 0):
            return render_template('create.html', username = session['username'], error="There needs to be a title!")
        if (request.form['content'].isspace() or len(request.form['content']) == 0):
            return render_template('create.html', username = session['username'], error="Content is empty.")
        create_blog(session['username'], request.form['title'], request.form['content'])
        all_blogs = get_all_blogs()
        return redirect('/response')
    
@app.route('/view', methods=['GET', 'POST'])
def view():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'GET':
        info = get_blog_info(list(request.args)[0])[0]
        print(info)
        return render_template('view.html', username = session['username'], infor = info)
    if request.method == 'POST':
        if (request.form['content'].isspace() or len(request.form['content']) == 0):
            return render_template('view.html', username = session['username'], error="Content is empty.")
        edit_blog(list(request.form)[1], request.form['content'])
        info = get_blog_info(list(request.form)[1])[0]
        return render_template('view.html', username = session['username'], infor = info)
    
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'GET':
        info = get_blog_info(list(request.args)[0])[0]
        if edit_blog_check(info[0], session['username']):
            return render_template('edit.html', username = session['username'], infor = info)
        return render_template('view.html', username = session['username'], infor = info, error ="This blog doesn't belong to you")
    if request.method == 'POST':
        return redirect('/view')
        
    
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'GET':
        user = list(request.args)[0]
        info = get_user_info(user)[0]
        blogs = get_user_blogs(user)
        return render_template('profile.html', username = session['username'], u=info, blogs=blogs)
    if request.method == 'POST':
        change_bio(request.form['user'], request.form['bio'])
        info = get_user_info(request.form['user'])[0]
        blogs = get_user_blogs(request.form['user'])
        return render_template('profile.html', username = session['username'], u=info, blogs=blogs)


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
