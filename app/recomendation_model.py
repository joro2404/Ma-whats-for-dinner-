from .database import DB
from flask_login import current_user

def get_users_count():
    all_user_list = []

    with DB() as db:
        all_users_count = db.execute('SELECT id FROM users').fetchall()
        for i in all_users_count:
            all_user_list.append(i[0])

        return max(all_users_count)


def all_user_ratings_by_user_id(user_id):
    all_user_ratings_list = []

    with DB() as db:
        all_users_ratings_tuple = db.execute('SELECT recipe_id FROM rating WHERE user_id = ?', (user_id,)).fetchall()
        for i in all_users_ratings_tuple:
            all_user_ratings_list.append(i[0])

        all_user_ratings_list.sort()
        return all_user_ratings_list



def get_user_common_rated_recipes(user_id):
    current_user_ratings =  all_user_ratings_by_user_id(current_user.id)
    an_user_ratings = all_user_ratings_by_user_id(user_id)

    current_user_ratings_set = set(current_user_ratings)
    intersection = current_user_ratings_set.intersection(an_user_ratings)

    intersection_list = list(intersection)

    return intersection_as_list


