import sqlite3

connection = sqlite3.connect('datab.db')

with open('scheme.sql') as f:
    connection.executescript(f.read())



connection.execute("INSERT INTO authent (user_id, pw) VALUES (?, ?)",
            ('sanail', 'samuel')
            )


connection.commit()

print(connection.execute('SELECT * FROM authent').fetchall())
connection.close()