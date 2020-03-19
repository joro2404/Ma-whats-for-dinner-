from flask import Flask, redirect, render_template, request, url_for
import sqlite3
 
 from product import Product
 from recepies import Recepie

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    #to be done by vesko
    #need to get current user
    return render_template('profile.html')

@app.route('/my_recepies')
#need to be log in
def my_recepies():
    #current user again
    return render_template('my_recepies.html')

@app.route('/create_recepie', methods=['GET', 'POST'])
#need to be log in
def my_recepies():
    if request.method == 'GET':
        return render_template('create_recepie.html')
    elif request.method == 'POST':
    #current user again
    values = (
        None,
        name,
        user,
        description,
        rating,
        #help
    )
    Recepie(*values).create()
    return redirect(url_for('my_recepies'))

@app.route('/my_recepies/<int:id>/edit', methods=['GET', 'POST'])
#need to be log in
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

@app.route('/my_recepies/<int:id>/delete', methods=['GET', 'POST'])
#need to be log in
def delete_recepie(id):
    recepie = Recepie.find(id)
    #checker if the user thats is logg ined is the current user
        recepie.delete()
    return redirect(url_for('my_recepies'))

if __name__ == '__main__':
    app.run()