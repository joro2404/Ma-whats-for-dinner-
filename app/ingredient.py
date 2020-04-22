from .database import DB


class Ingredient:
    def __init__(self, id, recipe_id, product_id, quantity):
        self.id = id
        self.recipe_id = recipe_id
        self.product_id = product_id
        self.quantity = quantity


    def create(self):
        with DB() as db:
            values = (self.recipe_id, self. product_id, self.quantity)
            db.execute('''
                INSERT INTO ingredients(recipe_id, product_id, quantity)
                VALUES (?, ?, ?)''', values)
            return self


    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM ingredients WHERE id = ?',(id,)).fetchone()
            return Ingredient(*row)


    @staticmethod
    def find_by_recipe_id(recipe_id):
        with DB() as db:
            rows = db.execute('SELECT * FROM ingredients WHERE recipe_id = ?', (recipe_id,)).fetchall()
            return [Ingredient(*row) for row in rows]


    @staticmethod
    def delete_by_recipe(recipe_id):
        with DB() as db:
            db.execute('DELETE FROM ingredients WHERE recipe_id = ?', (recipe_id,))

    
    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM ingredients WHERE id = ?', (self.id,))
            return self