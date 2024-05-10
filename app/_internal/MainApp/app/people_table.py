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

    cursor.execute("DROP TABLE IF EXISTS people_table")
    db.commit()
    db.close()



def create_people_table():
    db = sqlite3.connect(resource_path('MainApp/data/database.db'))
    
    cursor = db.cursor()
    
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS people_table(
            id INTEGER PRIMARY KEY,
            uid TEXT,
            name TEXT,
            surname TEXT,
            gender TEXT,
            role TEXT,
            team TEXT
            )
        '''
        )
    
    db.commit()
    db.close()



def search_people_data(search_term):
    db = sqlite3.connect(resource_path('MainApp/data/database.db'))
    
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM people_table WHERE name LIKE? OR surname LIKE? OR role LIKE? OR team LIKE? OR uid LIKE?", 
                   ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
    people_data = cursor.fetchall()
    db.close()
    return people_data



def fetch_people_data():
    db = sqlite3.connect(resource_path('MainApp/data/database.db'))
    cursor = db.cursor()
    
    cursor.execute('SELECT uid, name, surname, gender, role, team FROM people_table')
    data = cursor.fetchall()
    
    db.close()
    return data



def insert_people_data(name, surname, gender, role, team):
    db = sqlite3.connect(resource_path('MainApp/data/database.db'))
    cursor = db.cursor()
    

    cursor.execute("SELECT MAX(id) FROM people_table")
    last_id = cursor.fetchone()[0]
    if last_id is None:
        last_id = 0

    uid = f'{last_id+1}{name[0]}{surname[0]}'
    # print(uid)

    cursor.execute(
        '''
        INSERT INTO people_table (uid, name, surname, gender, role, team)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (uid, name, surname, gender, role, team)
    )

    db.commit()
    db.close()



def delete_people_data(uid):
    db = sqlite3.connect(resource_path('MainApp/data/database.db'))
    cursor = db.cursor()
    
    cursor.execute(f'DELETE FROM people_table WHERE uid = "{uid}"')
    
    db.commit()
    db.close()



def update_people_data(new_name, new_surname, new_gender, new_role, new_team, uid):
    db = sqlite3.connect(resource_path('MainApp/data/database.db'))
    cursor = db.cursor()
    
    cursor.execute(f'SELECT id FROM people_table WHERE uid = "{uid}"')
    
    id = cursor.fetchone()[0]

    new_uid = f'{id}{new_name[0]}{new_surname[0]}'
    
    cursor.execute("UPDATE people_table SET uid = ?, name = ?, surname = ?, gender = ?, role = ?, team = ? WHERE uid = ?",
                   (new_uid, new_name, new_surname, new_gender, new_role, new_team, uid))
    
    db.commit()
    db.close()



def export_uids():
    db = sqlite3.connect(resource_path('MainApp/data/database.db'))
    cursor = db.cursor()

    cursor.execute("SELECT uid FROM people_table")
    
    all_uids = cursor.fetchall()
        
    uids = []
    for i in all_uids:
        uids.append(i[0])
        
    db.close()

    return uids


# drop_table()
# create_people_table()
# generate_data()