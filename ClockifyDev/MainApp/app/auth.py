import sqlite3
import hashlib
import random

import people_table, dates_table, home_table

import sys
import os


db_path = ''

#   https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:

        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


userauthdb_path = resource_path('MainApp/data/main/userauth.db')


def drop_table():
    db = sqlite3.connect(userauthdb_path)
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS users_table")
    db.commit()
    db.close()



def create_users_table():
    db = sqlite3.connect(userauthdb_path)
    cursor = db.cursor()
    
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users_table(
            id INTEGER PRIMARY KEY,
            username TEXT,
            dbname TEXT,
            password TEXT
            )
        '''
        )
    
    db.commit()
    db.close()


def make_db_name(username):
    
    temp_dbname = username.encode().hex()
    
    temp_list = list(temp_dbname)
    temp_dbname = ''
    
    for q in range(random.randrange(len(temp_list)+1)):
        temp_dbname += random.choice(temp_list)
    
    temp_list = list(temp_dbname.encode().hex())
    temp_dbname = ''
    
    for z in range(8):
        temp_dbname += random.choice(temp_list)
    
    return temp_dbname


def hash_user_password(password):
    salt = password.encode().hex()
    
    password_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return password_hash


def insert_user(username, password):
    db = sqlite3.connect(userauthdb_path)
    cursor = db.cursor()
    
    temp_dbname = make_db_name(username)
    dbname = f'{username}_{temp_dbname}'
    
    hashed_password = hash_user_password(password)
    
    cursor.execute(
        '''
        INSERT INTO users_table (username, dbname, password)
        VALUES (?, ?, ?)
        ''',
        (username, dbname, hashed_password))
    
    db.commit()
    db.close()
    
    db_path = f'MainApp/data/userdata/{dbname}.db'
    print(db_path)
        
    people_table.create_people_table(db_path)
    dates_table.create_dates_table(db_path)
    home_table.create_home_table(db_path)



def login_check(username, password):
    global db_path
    db = sqlite3.connect(userauthdb_path)
    cursor = db.cursor()
    
    hashed_provided_password = hash_user_password(password)
    
    cursor.execute("SELECT dbname FROM users_table WHERE password = ?  AND username = ?", (hashed_provided_password, username))
    
    result = cursor.fetchone()
    db.close()
    
    if result is not None:
        result = result[0]
        db_path = f'MainApp/data/userdata/{result}.db'
        # print(db_path)
        
        people_table.create_people_table(db_path)
        dates_table.create_dates_table(db_path)
        home_table.create_home_table(db_path)
        return True
    else:
        return False
    




def check_user(username):
    db = sqlite3.connect(userauthdb_path)
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users_table WHERE username = ?", (username,))

    result = cursor.fetchone()
    
    db.close()
    
    return result is not None



# drop_table()
# create_users_table()