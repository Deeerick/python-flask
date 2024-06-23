import sqlite3


conn = sqlite3.connect('database.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        endereco TEXT NOT NULL,
        telefone INTEGER NOT NULL,
        interesse TEXT NOT NULL
    )
''')


conn.commit()
conn.close()
