import sqlite3
#create if not exist
conn = sqlite3.connect('29_01_2025.db')

##allow access column by bame
conn.row_factory = sqlite3.Row

# 3 create cursor
cursor = conn.cursor()

# 4
cursor.execute(
    '''
   CREATE TABLE IF NOT EXIST users (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   username text NOT NULL,
   pwd text NOT NULL check(length(ped)>=4) 
   ) 
    ''')

conn.commit()
