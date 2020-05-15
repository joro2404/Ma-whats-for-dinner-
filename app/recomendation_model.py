from .database import DB
from flask_login import current_user

def get_users_count():
    with DB() as db:
        all_users_count = db.execute('SELECT id FROM users').fetchall()
        return max(max(all_users_count))

def get_user_common_rated_recipes():
    get_users_count()
