import sqlite3


import sys
import os
#   https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:

        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def drop_table():
    db = sqlite3.connect(resource_path('MainApp/data/database.db'))
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS home_table")
    db.commit()
    db.close()



def create_home_table():
    db = sqlite3.connect(resource_path('MainApp/data/database.db'))
    cursor = db.cursor()
    
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS home_table(
            id INTEGER PRIMARY KEY,
            uid TEXT,
            name TEXT,
            surname TEXT,
            date TEXT,
            time TEXT,
            unix INTEGER,
            FOREIGN KEY (uid) REFERENCES people_table (uid),
            FOREIGN KEY (name) REFERENCES people_table (name),
            FOREIGN KEY (surname) REFERENCES people_table (surname),
            FOREIGN KEY (date) REFERENCES date_table (date),
            FOREIGN KEY (time) REFERENCES date_table (time),
            FOREIGN KEY (unix) REFERENCES date_table (unix)
            )
        '''
        )
    
    db.commit()
    db.close()




def fetch_home_data():
    db = sqlite3.connect(resource_path('MainApp/data/database.db'))
    cursor = db.cursor()
    
    cursor.execute('SELECT uid, name, surname, date, time FROM home_table ORDER BY unix')
    data = cursor.fetchall()
    data = reversed(data)
    db.close()
    return data














# drop_table()
# create_home_table()