import sqlite3


def create_db(dbname='db.sqlite'):
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    statement = 'SELECT COUNT(1) FROM SQLITE_MASTER WHERE TYPE = "table"'
    cur.execute(statement)
    if not cur.fetchone()[0]:
        print('SEEMS LIKE DB IS MISSING. CREATE NEW DB')
        with open('create_db.sql', 'r') as f:
            text = f.read()
        cur.executescript(text)
    else:
        print('SEEMS LIKE DB IS EXISTING ALREADY')
    cur.close()
    con.close()
