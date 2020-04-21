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


@main.route('/create_recipe', methods=['GET', 'POST'])
@login_required
def create_recipe():
    if request.method == 'GET':
        products = Product.all()
        ids = []
        names = []
        units = []
        for product in products:
            ids.append(product.id)
            names.append(product.name)
            units.append(product.unit)
        return render_template('create_recipe.html', products=products, ids=ids, names=names, units=units)
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


@main.route('/my_recipes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.find(id)
    number_of_products = len(recipe.products)
    if request.method == 'GET':
        return render_template('edit_recipe.html', recipe=recipe, number_of_products=number_of_products)
    elif request.method == 'POST':
        recipe.name = request.form['name']
        recipe.description = request.form['description']
        products = []
        for i in range(number_of_products):
            produc_id = '' + (i+1)
            products[i] = request.form['product_id']
        if number_of_products < 10:
            while(number_of_products<10):
                products[number_of_products] = None
                number_of_products += 1
        recipe.save(products)
        return redirect(url_for('my_recipes'))


@main.route('/my_recipes/<int:id>/delete', methods=['POST'])
@login_required
def delete_recipe(id):
    recipe = Recipe.find(id)
    if int(recipe.user_id) == current_user.id:
        recipe.delete()

    return redirect(url_for('main.my_recipes'))


if __name__ == '__main__':
    main.app.run()
