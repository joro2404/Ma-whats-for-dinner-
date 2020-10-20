from flask import Flask, redirect, render_template, request, url_for, Blueprint
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from .product import Product
from .recipes import Recipe
from .fridge import Fridge
from .ingredient import Ingredient
from .recomendation_model import *


main = Blueprint('main', __name__)
#gosho
upload_folder = "/home/georgi/Desktop/Ma-whats-for-dinner-/app/static/img/uploads"
default_img = "/home/georgi/Desktop/Ma-whats-for-dinner-/app/static/img/default.jpeg"
#vesko
# upload_folder = "/home/vesko/Desktop/gesko/Ma-whats-for-dinner-/app/static/img/uploads"
# default_img = "/home/vesko/Desktop/gesko/Ma-whats-for-dinner-/app/static/img/default.jpeg"


@main.route('/')
def index():
    if current_user.is_authenticated:
        recipes = get_recommended_recipes_for_user()
        while(len(recipes) > 3):
            recipes.pop()
        recipes_obj = []
        for recipe in recipes:
            recipes_obj.append(Recipe.find(recipe))
        return render_template('index.html', recipes=recipes_obj)
    else: 
        return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    user_products=Fridge.get_by_user_id(current_user.id)
    all_recipes = Recipe.all()
    count_of_fullfilled_recipes = 0
    ingredients = []
    suggested_recipe = Recipe(0, "suggestion failled", 0, "suggestion failled", 0, 0, default_img)

    for current_recipe in all_recipes:
        current_ingredients = Ingredient.find_by_recipe_id(current_recipe.id)
        ingredient_fullfilled = 0
        ingredient_passed = 0
        suggestion_failed = 0
        count_of_fullfilled_recipes = 0

        for i in current_ingredients:
            ingredient_passed += 1

            for j in user_products:
                if j.id == i.product_id and j.quantity >= i.quantity:
                    ingredient_fullfilled += 1

        if ingredient_passed != ingredient_fullfilled:
            suggestion_failed += 1

        if suggestion_failed == 0:
            if suggested_recipe.rating <= current_recipe.rating:
                suggested_recipe = current_recipe
        
        ingredients = Ingredient.find_by_recipe_id(suggested_recipe.id)

    return render_template('profile.html', products=user_products, suggested_recipe=suggested_recipe, ingredients=ingredients, product=Product)


@main.route('/recipes')
def recipes():
    return render_template('recipes.html', recipes=Recipe.all())


@main.route('/recipes/<int:id>', methods=['GET', 'POST'])
def show_recipe(id):
    if request.method == 'GET':
        if current_user.is_authenticated:
            recipe = Recipe.find(id)
            user_id = str(current_user.id)
            ingredients = Ingredient.find_by_recipe_id(recipe.id)
            user_products = Fridge.get_by_user_id(current_user.id)

            recipe_ingredients_names = []
            fridge_products_names = []

            for ingredient in ingredients:
                recipe_ingredients_names.append(Product.find(ingredient.product_id).name)

            for product in user_products:
                fridge_products_names.append(Product.find(product.product_id).name)

            missing_products = []
            missing_products_names = []

            for index, ingredient_name in enumerate(recipe_ingredients_names):
                if ingredient_name in fridge_products_names:
                    product = Fridge.get_by_product_id(ingredients[index].product_id)
                    if ingredients[index].quantity > product.quantity:
                        missing_products.append(ingredients[index])
                        missing_products_names.append(ingredient_name)

                else:
                    missing_products.append(ingredients[index])
                    missing_products_names.append(ingredient_name)

                    
            return render_template('view_recipe.html', recipe=recipe, user_id=user_id, ingredients=ingredients, product=Product, missing_products=missing_products, missing_products_names=missing_products_names)
        else:
            recipe = Recipe.find(id)
            ingredients = Ingredient.find_by_recipe_id(recipe.id)
            missing_products_names = []
            for ingredient in ingredients:
                missing_products_names.append(Product.find(ingredient.product_id).name)
            return render_template('view_recipe.html', recipe=recipe, ingredients=ingredients, product=Product, missing_products_names=missing_products_names)

    elif request.method == 'POST':
        recipe = Recipe.find(id)
        if current_user.is_authenticated:
            rate = request.form['rate']
            recipe.set_rating(rate, current_user.id)
            recipe.set_overall_rating()


        return redirect(url_for('main.show_recipe', id=recipe.id))


@main.route('/recipes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.find(id)
    ingredients = Ingredient.find_by_recipe_id(recipe.id)
    number_of_ingredients = len(ingredients)
    products = Product.all()
    if request.method == 'GET':
        return render_template('edit_recipe.html', recipe=recipe, ingredients=ingredients, number_of_ingredients=number_of_ingredients, Product=Product, products=products)
    elif request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            filename = recipe.picture
        if file and Recipe.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            recipe.remove_picture()
            file.save(os.path.join(upload_folder, filename))

        recipe.name = request.form['recipe_name']
        recipe.description = request.form['description']
        recipe.time = request.form['time']
        recipe.picture = os.path.join("/static/img/uploads", filename)
        recipe.save()

        Ingredient.delete_by_recipe(recipe.id)

        ingredients = [
            None,
            recipe.id,
            None,
            None
        ]

        i = 1
        while(request.form.get('id_of_product' + str(i)) is not None):
            ingredients[2] = request.form.get('id_of_product' + str(i))
            ingredients[3] = request.form.get('quantity_of_product' + str(i))
            Ingredient(*ingredients).create()
            i += 1
        
        return redirect(url_for('main.show_recipe', id=recipe.id))


@main.route('/create_recipe', methods=['GET', 'POST'])
@login_required
def create_recipe():
    if request.method == 'GET':
        products = Product.all()
        return render_template('create_recipe.html', products=products)
    elif request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            filename = secure_filename("/default.jpeg")
            filepath = os.path.join("/static/img", filename)
        if file and Recipe.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))
            filepath = os.path.join("/static/img/uploads", filename)

        values = (
            None,
            request.form['recipe_name'],
            current_user.id,
            request.form['description'],
            0.0,
            request.form['time'],
            filepath
        )
        Recipe(*values).create()

        recipe_id = Recipe.find_last_id()[0]

        ingredients = [
            None,
            recipe_id,
            None,
            None
        ]
        i = 1
        while(request.form.get('id_of_product' + str(i)) is not None):
            ingredients[2] = request.form.get('id_of_product' + str(i))
            ingredients[3] = request.form.get('quantity_of_product' + str(i))
            Ingredient(*ingredients).create()
            i += 1

        return redirect(url_for('main.my_recipes'))


@main.route('/my_recipes')
@login_required
def my_recipes():
    return render_template('my_recipes.html', recipes=Recipe.get_by_user_id(current_user.id))


@main.route('/my_recipes/<int:id>/delete', methods=['POST'])
@login_required
def delete_recipe(id):
    recipe = Recipe.find(id)
    if int(recipe.user_id) == current_user.id:
        recipe.remove_picture()
        recipe.delete()
        Ingredient.delete_by_recipe(recipe.id)

    return redirect(url_for('main.my_recipes'))


if __name__ == '__main__':
    main.app.run()
