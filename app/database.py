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
        unit TEXT NOT NULL
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS recipes
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id TEXT NOT NULL,
        description TEXT NOT NULL,
        rating INTEGER,
        product1_id INTEGER UNIQUE,
        product1_quantity INTEGER,
        product2_id INTEGER UNIQUE,
        product2_quantity INTEGER,
        product3_id INTEGER UNIQUE,
        product3_quantity INTEGER,
        product4_id INTEGER UNIQUE,
        product4_quantity INTEGER,
        product5_id INTEGER UNIQUE,
        product5_quantity INTEGER,
        product6_id INTEGER UNIQUE,
        product6_quantity INTEGER,
        product7_id INTEGER UNIQUE,
        product7_quantity INTEGER,
        product8_id INTEGER UNIQUE,
        product8_quantity INTEGER,
        product9_id INTEGER UNIQUE,
        product9_quantity INTEGER,
        product10_id INTEGER UNIQUE,
        product10_quantity INTEGER,
        FOREIGN KEY (product1_id) REFERENCES products(id),
        FOREIGN KEY (product2_id) REFERENCES products(id),
        FOREIGN KEY (product3_id) REFERENCES products(id),
        FOREIGN KEY (product4_id) REFERENCES products(id),
        FOREIGN KEY (product5_id) REFERENCES products(id),
        FOREIGN KEY (product6_id) REFERENCES products(id),
        FOREIGN KEY (product7_id) REFERENCES products(id),
        FOREIGN KEY (product8_id) REFERENCES products(id),
        FOREIGN KEY (product9_id) REFERENCES products(id),
        FOREIGN KEY (product10_id) REFERENCES products(id)     
    )
''')

conn.commit()

class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
