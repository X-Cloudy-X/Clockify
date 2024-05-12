import sqlite3
from datetime import *

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



def drop_table():
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS dates_table")
    db.commit()
    db.close()



def create_dates_table(path):
    global db_path
    db_path = path
    
    db = sqlite3.connect(resource_path(db_path))
    
    cursor = db.cursor()
    
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS dates_table(
            id INTEGER PRIMARY KEY,
            uid TEXT,
            role TEXT,
            team TEXT,
            date TEXT,
            time TEXT,
            unix INTEGER
            )
        '''
        )
    
    db.commit()
    db.close()



def search_dates_data(search_term):
    db = sqlite3.connect(resource_path(db_path))
    
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM dates_table WHERE uid LIKE? OR role LIKE? OR team LIKE? OR date LIKE? OR time LIKE?", 
                   ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
    dates_data = cursor.fetchall()
    db.close()
    return dates_data



def fetch_dates_data():
    db = sqlite3.connect(resource_path(db_path))
    cursor = db.cursor()
    
    cursor.execute('SELECT uid, role, team, date, time FROM dates_table ORDER BY unix')
    data = cursor.fetchall()
    data = reversed(data)
    db.close()
    return data



def get_ppl_data(uid):
    db = sqlite3.connect(resource_path(db_path))
    cursor = db.cursor()
    
    cursor.execute(f'SELECT role, team, name, surname FROM people_table WHERE uid = "{uid}" ')
    
    data = cursor.fetchall()
    data = data[0]
    
    db.commit()
    db.close
    
    return data



def insert_dates_data(uid, date, time):
    
    data = get_ppl_data(uid)
    
    role = data[0]
    team = data[1]
    name = data[2]
    surname = data[3]
    
    
    db = sqlite3.connect(resource_path(db_path))
    cursor = db.cursor()
    
    date_obj = datetime.strptime(str(date) + " " + time+":00", "%d-%m-%Y %H:%M:%S")
    unix = round(date_obj.timestamp())
    # print(uid, team, role, date, time, unix)
    # print(type(unix))
    # print()
    cursor.execute(
        '''
        INSERT INTO dates_table (uid, role, team, date, time, unix)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (uid, role, team, date, time, unix))
    
    cursor.execute(
        '''
        INSERT INTO home_table (uid, name, surname, date, time, unix)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (uid, name, surname, date, time, unix))
    
    db.commit()
    db.close()
    

def auto_insert_dates_data(uid, date, time, unix):
    
    data = get_ppl_data(uid)
    
    role = data[0]
    team = data[1]
    name = data[2]
    surname = data[3]
    
    
    db = sqlite3.connect(resource_path(db_path))
    cursor = db.cursor()
    
    cursor.execute(
        '''
        INSERT INTO dates_table (uid, role, team, date, time, unix)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (uid, role, team, date, time, unix))
    
    cursor.execute(
        '''
        INSERT INTO home_table (uid, name, surname, date, time, unix)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (uid, name, surname, date, time, unix))
    
    db.commit()
    db.close()



def delete_dates_data(uid, date, time):
    db = sqlite3.connect(resource_path(db_path))
    cursor = db.cursor()
    
    cursor.execute('DELETE FROM dates_table WHERE uid = ? AND date = ? AND time = ?', (uid, date, time))
    cursor.execute('DELETE FROM home_table WHERE uid = ? AND date = ? AND time = ?', (uid, date, time))
    
    db.commit()
    db.close()


#   if you accidently logged wrong user,
#   im sorry for you (not)
#   now be so kind, since you cant edit the entry, 
#   just delete them and do it anew :)
#   welcome to limiting user rights - discord 2024



# drop_table()
# create_dates_table()