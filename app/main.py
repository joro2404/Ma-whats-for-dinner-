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
    return render_template('profile.html', current_user=current_user)


@main.route('/my_recipes')
@login_required
def my_recipes():
    #current user again
    return render_template('my_recipes.html')


@main.route('/create_recipe', methods=['GET', 'POST'])
@login_required
def create_recipe():
    if request.method == 'GET':
        return render_template('create_recipe.html')
    elif request.method == 'POST':
    #current user again
        values = (
            None,
            name,
            current_user.id,
            description,
            rating,
            #help
        )
        Recepie(*values).create()
        return redirect(url_for('my_recepies'))

@main.route('/my_recipes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.find(id)
    if request.method == 'GET':
        return render_template('edit_recipe.html', recipe=recipe)
    elif request.method == 'POST':
        recipe.name = request.form['name']
        recipe.description = request.form['description']
        #products to be added/deleted
        recipe.save()
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