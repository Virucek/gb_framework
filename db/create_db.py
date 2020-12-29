import sqlite3

dbname = 'db.sqlite'
con = sqlite3.connect(dbname)
cur = con.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()
cur.executescript(text)
cur.close()
con.close()