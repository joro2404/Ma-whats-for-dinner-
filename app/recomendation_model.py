from .database import DB
from flask_login import current_user
from scipy import spatial

def get_users_count():
    all_user_list = []

    with DB() as db:
        all_users_count = db.execute('SELECT id FROM users').fetchall()
        for i in all_users_count:
            all_user_list.append(i[0])

        return all_user_list


def all_user_ratings_by_user_id(user_id):
    all_user_ratings_list = []

    with DB() as db:
        all_users_ratings_tuple = db.execute('SELECT recipe_id FROM rating WHERE user_id = ?', (user_id,)).fetchall()
        # print(all_users_ratings_tuple)
        # print(list(all_users_ratings_tuple))
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
    result = ((), ())

    for i in common_recipes():
        with DB() as db:
            result[0].appened('SELECT raiting FROM raiting WHERE user_id = ? and recipe_id = ?', (current_user.id, i,).fetchone())
            result[1].append('SELECT rating FROM raiting WHERE user_id = ?, and recipe_id = ?', (user_id, i,).fetchone())

    return result

def calculate_euclidean_spatial_distance():
    all_users = get_users_count()
    top_five_euclidean_scores = {0: 1000, 0: 1000, 0: 1000, 0: 1000, 0: 1000}

    for i in all_users:
        if i == current_user.id:
            continue
        else:
            common_recipes_with_an_user = get_user_common_rated_recipes(i)


            result = get_ratings_from_common_recipes(common_recipes_with_an_user, i)

            

            euclidean_spatial_distance = spatial.distance.euclidean(result[0], result[1])
            if euclidean_spatial_distance < list(top_five_euclidean_scores.values())[-1] : 
                last_value = list(top_five_euclidean_scores.values())[-1]
                last_key = list(top_five_euclidean_scores.keys())[-1]
                top_five_euclidean_scores.popitem()
                top_five_euclidean_scores.update({i: euclidean_spatial_distance})

                top_five_euclidean_scores = sorted(top_five_euclidean_scores.items(), key=lambda x: x[1])
                top_five_euclidean_scores = dict(top_five_euclidean_scores)

    return top_five_euclidean_scores


def get_best_matching_user_id():
    top_five_euclidean_scores = calculate_euclidean_spatial_distance()

    list_of_top_five_user_id = list(top_five_euclidean_scores.keys())

    best_user_id = 0
    best_cosine_score = 1000

    # all_user_ratings_by_user_id(current_user.id)

    for i in list_of_top_five_user_id:
        temp = get_user_common_rated_recipes(i)

            result = (temp, i)

            cosine_spatial_distance = spatial.distance.cosine(result[0], result[1])

            if cosine_spatial_distance < best_cosine_score:
                best_cosine_score = cosine_spatial_distance
                best_user_id = i

    return best_user_id

def get_recommended_recipes_for_user():
    id = get_best_matching_user_id()

    with DB() as db:
            an_user_raitings_for_common_recipes = db.execute('SELECT id FROM recipes WHERE user_id = ?', (id,)).fetchall()
            current_user_ratings_for_common_recipes = db.execute('SELECT id FROM racipes WHERE user_id = ?', (current_user,)).fetchall()

            current_user_ratings_for_common_recipes_list = []
            an_user_raitings_for_common_recipes_list = []

            for j in current_user_ratings_for_common_recipes:
                current_user_ratings_for_common_recipes_list.append(j[0])

            for j in an_user_raitings_for_common_recipes:
                an_user_raitings_for_common_recipes_list.append(j[0])

    result = set(an_user_raitings_for_common_recipes_list) - set(current_user_ratings_for_common_recipes_list)

    return list(result)

    #line 43 fuction need revising, not gettign the common recipes, gettign the whole list of thier rated recipes 
    # to be done 




            


            





