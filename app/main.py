from flask import Flask, redirect, render_template, request, url_for, Blueprint
from flask_login import login_required, current_user
import sqlite3
from .product import Product
from .recipes import Recipe


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/recipes')
def recipes():
    return render_template('recipes.html')


@main.route('/my_recipes')
@login_required
def my_recipes():
    #current user again
    return render_template('my_recipes.html', recipes=Recipe.get_by_user_id(current_user.id))


@main.route('/create_recipe', methods=['GET', 'POST'])
@login_required
def create_recipe():
    if request.method == 'GET':
        return render_template('create_recipe.html')
    elif request.method == 'POST':
        number_of_products = request.form['number_of_products']
        values = [
            None,
            name,
            current_user.id,
            description,
            rating
        ]
        products = []
        for i in range(number_of_products):
            produc_id = '' + (i+1)
            products[i] = request.form['product_id']
        values[5] = products
        if number_of_products < 10:
            while(number_of_products<10):
                products[number_of_products] = None
                number_of_products += 1
        Recipe(*values).create()
        return redirect(url_for('my_recepies'))


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


@main.route('/my_recipes/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_recipe(id):
    recipe = Recipe.find(id)
    if recipe.user_id == current_user.id:
        recipe.delete()

    return redirect(url_for('my_recipes'))


if __name__ == '__main__':
    app.run()
