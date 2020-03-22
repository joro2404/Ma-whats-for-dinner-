from .database import DB


class Recipe:
    def __init__(self, id, name, user_id, description, rating, product1_id, product1_quantity, product2_id, product2_quantity, product3_id, product3_quantity, product4_id, product4_quantity, product5_id, product5_quantity, product6_id, product6_quantity, product7_id, product7_quantity, product8_id, product8_quantity, product9_id, product9_quantity, product10_id, product10_quantity):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.description = description
        self.rating = rating
        self.product1_id = product1_id
        self.product1_quantity = product1_quantity
        self.product2_id = product2_id
        self.product2_quantity = product2_quantity
        self.product3_id = product3_id
        self.product3_quantity = product3_quantity
        self.product4_id = product4_id
        self.product4_quantity = product4_quantity
        self.product5_id = product5_id
        self.product5_quantity = product5_quantity
        self.product6_id = product6_id
        self.product6_quantity = product6_quantity
        self.product7_id = product7_id
        self.product7_quantity = product7_quantity
        self.product8_id = product8_id
        self.product8_quantity = product8_quantity
        self.product9_id = product9_id
        self.product9_quantity = product9_quantity
        self.product10_id = product10_id
        self.product10_quantity = product10_quantity


    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM recipes').fetchall()
            return [Recipe(*row) for row in rows]

    def create(self):
        with DB() as db:
            values = (self.name, self.user_id, self.description, self.product1_id, self.product1_quantity, self.product2_id, self.product2_quantity,self. product3_id, self.product3_quantity, self.product4_id, self.product4_quantity, self.product5_id, self.product5_quantity, self.product6_id, self.product6_quantity, self.product7_id, self.product7_quantity, self.product8_id, self.product8_quantity, self.product9_id, self.product9_quantity, self.product10_id, self.product10_quantity)
            db.execute('''
                INSERT INTO recipes(name, user_id, description, product1_id, product1_quantity, product2_id, product2_quantity, product3_id, product3_quantity, product4_id, product4_quantity, product5_id, product5_quantity, product6_id, product6_quantity, product7_id, product7_quantity, product8_id, product8_quantity, product9_id, product9_quantity, product10_id, product10_quantity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', values)
            return self

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM recipes WHERE id = ?',(id,)).fetchone()
            return Recipe(*row)

    @staticmethod
    def find_by_name(name):
        if not name:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM recipes WHERE name = ?',
                (name,)
            ).fetchone()
            if row:
                return Recipe(*row)

    @staticmethod
    def get_by_user_id(user_id):
        with DB() as db:
            rows = db.execute('SELECT * FROM recipes WHERE user_id = ?', (user_id,)).fetchall()
            return [Recipe(*row) for row in rows]

    def save(self, products):
        with DB() as db:
            values = [self.name, self.description]
            for i in range(10):
                values[i+2] = products[i]
            values[12] = self.id
            db.execute('UPDATE recipes SET name = ?, description = ?, product1_id = ?, product2_id = ?, product3_id = ?, product4_id = ?, product5_id = ?, product6_id = ?, product7_id = ?, product8_id = ?, product9_id = ?, product10_id = ? WHERE id = ?', values)
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM recipes WHERE id = ?', (self.id,))
            return self