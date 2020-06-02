from .database import DB
from .product import Product


class Fridge:
    def __init__(self, id, user_id, product_id, quantity):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity


    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM fridge').fetchall()
            return [Fridge(*row) for row in rows]


    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM fridge WHERE id = ?',(id,)).fetchone()
            return Fridge(*row)


    @staticmethod
    def get_by_product_id(id):
        with DB() as db:
            row = db.execute('SELECT * FROM fridge WHERE product_id = ?',(id,)).fetchone()
            return Fridge(*row)


    @staticmethod
    def find_by_product_id(product_id):
        with DB() as db:
            row = db.execute('SELECT * FROM products WHERE id = ?',(product_id,)).fetchone()
            return Product(*row)


    @staticmethod
    def get_by_user_id(user_id):
        with DB() as db:
            rows = db.execute('SELECT * FROM fridge WHERE user_id = ?', (user_id,)).fetchall()
            return [Fridge(*row) for row in rows]
    
