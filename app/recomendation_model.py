from .database import DB
from flask_login import current_user
from scipy import spatial

def get_users_count():
    all_user_list = []

    with DB() as db:
        all_users_count = db.execute('SELECT id FROM users').fetchall()

    for i in all_users_count:
        all_user_list.append(i[0])

    all_user_list.sort()
    return all_user_list


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
    intersection_list.sort()
    return intersection_list

def get_ratings_from_common_recipes(common_recipes, user_id):
    result = [[], []]

    for i in common_recipes:
        with DB() as db:
            result[0].append(db.execute('SELECT rating FROM rating WHERE user_id = ? AND recipe_id = ?', (current_user.id, i,)).fetchone()[0])
            result[1].append(db.execute('SELECT rating FROM rating WHERE user_id = ? AND recipe_id = ?', (user_id, i,)).fetchone()[0])

    return result


def calculate_euclidean_spatial_distance():
    all_users = get_users_count()
    top_five_euclidean_scores = {0: 1000, 0: 1000, 0: 1000, 0: 1000, 0: 1000}
    global_dict = {}

    for i in all_users:
        if i == current_user.id:
            continue
        else:
            common_recipes_with_an_user = get_user_common_rated_recipes(i)

            result = get_ratings_from_common_recipes(common_recipes_with_an_user, i)

            if len(result[0]) > 0 and len(common_recipes_with_an_user) > 3:
                euclidean_spatial_distance = spatial.distance.euclidean(result[0], result[1])
                if euclidean_spatial_distance < list(top_five_euclidean_scores.values())[-1] : 
                    last_value = list(top_five_euclidean_scores.values())[-1]
                    last_key = list(top_five_euclidean_scores.keys())[-1]
                    top_five_euclidean_scores.popitem()
                    top_five_euclidean_scores.update({i: euclidean_spatial_distance})

                    top_five_euclidean_scores = sorted(top_five_euclidean_scores.items(), key=lambda x: x[1])
                    top_five_euclidean_scores = dict(top_five_euclidean_scores)
                    global_dict.update(top_five_euclidean_scores)
            
            else:
                continue

    return global_dict

def get_best_matching_user_id():
    top_five_euclidean_scores = calculate_euclidean_spatial_distance()

    list_of_top_five_user_id = list(top_five_euclidean_scores.keys())

    best_user_id = 0
    best_cosine_score = 1000

    for i in list_of_top_five_user_id:
        temp = get_user_common_rated_recipes(i)

        result = (temp, i)

        cosine_spatial_distance = spatial.distance.cosine(result[0], result[1])

        top_five_euclidean_scores[i] = cosine_spatial_distance

    top_five_euclidean_scores = sorted(top_five_euclidean_scores.items(), key=lambda x: x[1])
    top_five_euclidean_scores = dict(top_five_euclidean_scores)

    return top_five_euclidean_scores


def get_recommended_recipes_for_user():
    dict_of_ids_cosine = get_best_matching_user_id()

    list_of_top_five_user_id = list(dict_of_ids_cosine.keys())

    result = []

    for id in list_of_top_five_user_id:
        with DB() as db:
            an_user_raitings_for_common_recipes = db.execute('SELECT recipe_id FROM rating WHERE user_id = ?', (id,)).fetchall()
            current_user_ratings_for_common_recipes = db.execute('SELECT recipe_id FROM rating WHERE user_id = ?', (current_user.id,)).fetchall()

            current_user_ratings_for_common_recipes_list = []
            an_user_raitings_for_common_recipes_list = []

            for j in current_user_ratings_for_common_recipes:
                current_user_ratings_for_common_recipes_list.append(j[0])

            for j in an_user_raitings_for_common_recipes:
                rating_of_recipe_j = db.execute('SELECT rating FROM rating WHERE user_id = ? AND recipe_id =?', (id, j[0])).fetchone()
                if rating_of_recipe_j[0] > 1:
                    an_user_raitings_for_common_recipes_list.append(j[0])

        result = set(an_user_raitings_for_common_recipes_list) - set(current_user_ratings_for_common_recipes_list)
        if len(list(result)) == 0:
            continue
        else:
            break

    return list(result)
