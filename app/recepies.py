from database import DB
from user import User

class Recepie:
    def __init__(self, id, name, user, description, rating, products):
        self.id = id
        self.name = name
        self.user = user
        self.description = description
        self.rating = rating
        self.products = products


    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM recepies').fetchall()
            return [Recepie(*row) for row in rows]

    def create(self):
        with DB() as db:
            values = (self.name, self.user, self.description)
            for i in range(10):
                values[i+3] = products[i]
            db.execute('''
                INSERT INTO recepies(name, user, description, product1_id, product2_id, product3_id, product4_id, product5_id, product6_id, product7_id, product8_id, product9_id, product10_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', values)
            return self

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM recepies WHERE id = ?',(id,)).fetchone()
            return Recepie(*row)

    @staticmethod
    def find_by_name(name):
        if not name:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM recepies WHERE name = ?',
                (name,)
            ).fetchone()
            if row:
                return Recepie(*row)

    def save(self):
        with DB() as db:
            values = (self.name, self.description)
            for i in range(10):
                values[i+2] = products[i]
            values[12] = self.id
            db.execute('UPDATE recepies SET name = ?, description = ?, product1_id = ?, product2_id = ?, product3_id = ?, product4_id = ?, product5_id = ?, product6_id = ?, product7_id = ?, product8_id = ?, product9_id = ?, product10_id = ? WHERE id = ?', values)
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM recepies WHERE id = ?', (self.id,))
            return self