from .database import DB


class Product:
    def __init__(self, id, name, unit):
        self.id = id
        self.name = name
        self.unit = unit


    def create(self):
        with DB() as db:
       		values = (self.id, self.name, self.quantity, self.unit)
        	db.execute('''
            	INSERT INTO products (id, name, quantity, unit)
            	VALUES (?, ?, ?, ?)''', values)
        	return self


    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM products').fetchall()
            return [Product(*row) for row in rows]


    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM products WHERE id = ?',(id,)).fetchone()
            return Product(*row)


    @staticmethod
    def find_by_name(name):
        if not name:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM products WHERE name = ?',
                (name,)
            ).fetchone()
            if row:
                return Product(*row)
