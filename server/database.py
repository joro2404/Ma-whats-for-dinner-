import sqlite3

DB_NAME = 'gesko.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS users
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        sensor_id INTEGER UNIQUE NOT NULL
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS products
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        quantity INTEGER UNIQUE NOT NULL,
        unit TEXT UNIQUE NOT NULL
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS recepies
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product1_id INTEGER UNIQUE,
        product2_id INTEGER UNIQUE,
        product3_id INTEGER UNIQUE,
        product4_id INTEGER UNIQUE,
        product5_id INTEGER UNIQUE,
        product6_id INTEGER UNIQUE,
        product7_id INTEGER UNIQUE,
        product8_id INTEGER UNIQUE,
        product9_id INTEGER UNIQUE,
        product10_id INTEGER UNIQUE,
        FOREIGN KEY (product1) REFERENCES products(id),
        FOREIGN KEY (product1) REFERENCES products(id),
        FOREIGN KEY (product1) REFERENCES products(id),
        FOREIGN KEY (product1) REFERENCES products(id),
        FOREIGN KEY (product1) REFERENCES products(id),
        FOREIGN KEY (product1) REFERENCES products(id),
        FOREIGN KEY (product1) REFERENCES products(id),
        FOREIGN KEY (product1) REFERENCES products(id),
        FOREIGN KEY (product1) REFERENCES products(id),
        FOREIGN KEY (product1) REFERENCES products(id),
        FOREIGN KEY (product1) REFERENCES products(id)

        
    )
''')

conn.commit()

class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
