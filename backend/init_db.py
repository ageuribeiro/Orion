import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    senha TEXT NOT NULL)
''')

cursor.execute('''INSERT INTO usuarios (email, senha) VALUES (?, ?)
''', ('teste@email.com', '1234567890'))

conn.commit()
conn.close()
