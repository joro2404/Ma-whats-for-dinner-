from flask import Flask, redirect, render_template, request, url_for, Blueprint
from flask_login import login_required, current_user
import sqlite3
from .product import Product
from .recepies import Recepie


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)


@main.route('/my_recepies')
@login_required
def my_recepies():
    #current user again
    return render_template('my_recepies.html')


@main.route('/create_recepie', methods=['GET', 'POST'])
@login_required
def create_recepie():
    if request.method == 'GET':
        return render_template('create_recepie.html')
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

@main.route('/my_recepies/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recepie(id):
    recepie = Recepie.find(id)
    if request.method == 'GET':
        return render_template('edit_recepie.html', recepie=recepie)
    elif request.method == 'POST':
        recepie.name = request.form['name']
        recepie.description = request.form['description']
        #products to be added/deleted
        recepie.save()
        return redirect(url_for('my_recepies'))

@main.route('/my_recepies/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_recepie(id):
    recepie = Recepie.find(id)
    if recepie.user_id == current_user.id:
        recepie.delete()

    return redirect(url_for('my_recepies'))

if __name__ == '__main__':
    app.run()