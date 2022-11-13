import sqlite3

DB_FILE="discobandit.db"

def create_tables():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()   
    #checks to see if the tables exist, if not the tables will be created
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS blogs(id INT, username TEXT, title TEXT, content TEXT,time TEXT)")
    
    db.commit()
    db.close()


def check_user_exist(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username FROM users WHERE username=?", (username,))

    user = c.fetchone()
#    print(user)

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


#checks to see if username and password match
def login_check(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE (username = ? AND password = ?)", (username, password))
    status = c.fetchone() 

    db.close()

    if status == None: 
        return False
    return True


create_tables()
db = sqlite3.connect(DB_FILE)
'''
db.execute("DROP TABLE IF EXISTS users") 
create_tables()
print(check_user_exist("akitiss")) #False
create_user("akitiss", "hellaur")
print(check_user_exist("akitiss")) #True
print(login_check("akitiss", "hellaur")) # True
print(login_check("akitiss", "sup")) # False
'''

db.execute("DROP TABLE IF EXISTS blogs")
create_tables()