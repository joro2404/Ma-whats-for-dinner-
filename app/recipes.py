from .database import DB


class Recipe:
    def __init__(self, id, name, user_id, description, rating, time):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.description = description
        self.rating = rating
        self.time = time


    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM recipes').fetchall()
            return [Recipe(*row) for row in rows]


    def create(self):
        with DB() as db:
            values = (self.name, self.user_id, self.description, self.time)
            db.execute('''
                INSERT INTO recipes(name, user_id, description, time)
                VALUES (?, ?, ?, ?)''', values)
            return self


    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM recipes WHERE id = ?',(id,)).fetchone()
            return Recipe(*row)


    @staticmethod
    def find_last_id():
        with DB() as db:
            last_id = db.execute('SELECT MAX(id) from recipes').fetchone()
            return last_id


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
            # tuka nz kvo se sluchva oshte
            values = [self.name, self.description]
            for i in range(10):
                values[i+2] = products[i]
            values[12] = self.id
            db.execute('UPDATE recipes SET name = ?, description = ?, time = ? WHERE id = ?', values)
            return self


    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM recipes WHERE id = ?', (self.id,))
            return self