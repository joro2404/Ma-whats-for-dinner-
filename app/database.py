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
CREATE TABLE IF NOT EXISTS fridge
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity DOUBLE(1, 3) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS recipes
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id TEXT NOT NULL,
        description TEXT NOT NULL,
        rating DOUBLE(1, 1) NOT NULL,
        time INTEGER NOT NULL,
        picture TEXT
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS ingredients
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity DOUBLE(1, 3) NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS rating
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rating INTEGER NOT NULL,
        recipe_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES recipes(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS sensors
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        apds0 INTEGER NOT NULL,
        apds1 INTEGER NOT NULL,
        apds2 INTEGER NOT NULL,
        apds3 INTEGER NOT NULL,
        apds4 INTEGER NOT NULL,
        apds5 INTEGER NOT NULL,
        apds6 INTEGER NOT NULL,
        apds7 INTEGER NOT NULL
    )
''')

conn.commit()

class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
