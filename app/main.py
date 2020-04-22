from flask import Flask, redirect, render_template, request, url_for, Blueprint
from flask_login import login_required, current_user
import sqlite3
from .product import Product
from .recipes import Recipe
from .fridge import Fridge
from .ingredient import Ingredient


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', products=Fridge.get_by_user_id(current_user.id))


@main.route('/recipes')
def recipes():
    return render_template('recipes.html', recipes=Recipe.all())


@main.route('/recipes/<int:id>', methods=['GET', 'POST'])
def show_recipe(id):
    if current_user.is_authenticated:
        recipe = Recipe.find(id)
        user_id = str(current_user.id)
        ingredients = Ingredient.find_by_recipe_id(recipe.id)
        return render_template('view_recipe.html', recipe=recipe, user_id=user_id, ingredients=ingredients, product=Product)
    else:
        recipe = Recipe.find(id)
        ingredients = Ingredient.find_by_recipe_id(recipe.id)
        return render_template('view_recipe.html', recipe=recipe, ingredients=ingredients, product=Product)


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
        recipe.name = request.form['recipe_name']
        recipe.description = request.form['description']
        recipe.time = request.form['time']
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
        values = (
            None,
            request.form['recipe_name'],
            current_user.id,
            request.form['description'],
            0,
            request.form['time']
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
        recipe.delete()
        Ingredient.delete_by_recipe(recipe.id)

    return redirect(url_for('main.my_recipes'))


@main.route('/recipes/<int:id>/<int:ingredient_id>/delete', methods=['POST'])
@login_required
def delete_ingredient(id, ingredient_id):
    recipe = Recipe.find(id)
    ingredient = Ingredient.find(ingredient_id)
    if int(recipe.user_id) == current_user.id:
        if int(recipe.id) == int(ingredient.recipe_id):
            ingredient.delete()
            return redirect(url_for('main.edit_recipe', id=recipe.id))
        else:
            return redirect(url_for('main.recipes'))

    return redirect(url_for('main.recipes'))


if __name__ == '__main__':
    main.app.run()
