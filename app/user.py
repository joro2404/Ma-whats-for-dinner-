from flask_login import UserMixin
from .database import DB


class User(UserMixin):
    def __init__(self, id, username, password, email, sensor_id):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.sensor_id = sensor_id


    def create(self):
    	with DB() as db:
       		values = (self.username, self.password, self.email, self.sensor_id)
        	db.execute('''
            	INSERT INTO users (username, password, email, sensor_id)
            	VALUES (?, ?, ?, ?)''', values)
        	return self


    @staticmethod
    def find(email):
        if not email:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM users WHERE email = ?',(email,)
            ).fetchone()
            if row:
                return User(*row)


    @staticmethod
    def find_by_id(id):
        if not id:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM users WHERE id = ?',(id,)
            ).fetchone()
            if row:
                return User(*row)

