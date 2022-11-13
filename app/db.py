import sqlite3
from datetime import datetime

DB_FILE="discobandit.db"

##USER FUNCTIONS##
def create_tables():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()   
    #checks to see if the tables exist, if not the tables will be created
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS blogs(id INT, username TEXT, title TEXT, content TEXT,time TEXT)")
    
    db.commit()
    db.close()

def check_user_exist(username): #returns True if the username already exists
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username FROM users WHERE username=?", (username,))

    user = c.fetchone()

    db.close()

    if user == None:
        return False
    return True

def create_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("INSERT INTO users VALUES(?, ?)", (username, password))

    db.commit()
    db.close()

def login_check(username, password): #return True is username and password match 
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE (username = ? AND password = ?)", (username, password))
    status = c.fetchone() 

    db.close()

    if status == None: 
        return False
    return True


##BLOG FUNCTIONS##
def create_blog(id, username, title, content):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    t = datetime.now()
    time = t.strftime("%B %d, %Y %H:%M")
    c.execute("INSERT INTO blogs VALUES(?, ?, ?, ?, ?)", (id, username, title, content, time))

    db.commit()
    db.close()

def edit_blog_check(id, username): #returns True if the user is editing their own blog
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT username FROM blogs WHERE (id = ? AND username = ?)", (id, username))
    status = c.fetchone() 

    db.close()

    if status == None:
        return False
    return True

def edit_blog(id, new_content):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    t = datetime.now()
    new_time = t.strftime("%B %d, %Y %H:%M")
    c.execute("UPDATE blogs SET content = ?, time  = ? WHERE id = ?", (new_content, new_time, id))

    db.commit()
    db.close()


##GET FUNCTIONS##
def get_usernames(): 
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT username FROM users")
    all_users = c.fetchall()

    db.close()

    return all_users

def get_usernames_passwords():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM users")
    all_users = c.fetchall()

    db.close()

    return all_users

def get_all_blogs():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM blogs")
    all_blogs = c.fetchall()

    db.close()

    return all_blogs

def get_blog_info(id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM blogs WHERE id = ?", id)
    blog = c.fetchall()

    db.close()

    return blog

def get_user_blogs(username): 
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM blogs WHERE username = ?", username)
    user_blogs = c.fetchall()

    db.close()

    return user_blogs


db = sqlite3.connect(DB_FILE)
c = db.cursor()

db.execute("DROP TABLE IF EXISTS users") 
db.execute("DROP TABLE IF EXISTS blogs")

create_tables()
#print(check_user_exist("akitiss")) #False
create_user("akitiss", "hellaur")
#print(check_user_exist("akitiss")) #True
#print(login_check("akitiss", "hellaur")) # True
#print(login_check("akitiss", "sup")) # False
create_user("pie", "apple")

create_blog(20, "akitiss", "title", "content")
print(edit_blog_check(20, "akitiss")) #True
print(edit_blog_check(10, "akitiss")) #False
edit_blog(10, "hellaururuur")

print(get_usernames())
print(get_usernames_passwords())
print(get_all_blogs())
