from flask import Blueprint, render_template, request, redirect, url_for, flash
from .database import DB

sensors = Blueprint('sensors', __name__)

@sensors.route('/insert', methods=['GET', 'POST'])
def get_sensors_info():
    if request.method == 'GET':
        return redirect("http://188.126.25.95:81", code=302)
    if request.method == 'POST':
        values = []

        content = request.get_json()

        for i in range(0, 8):
            values.append(content.get(str(i)))

        with DB() as db:
            db.execute('UPDATE sensors SET apds0 = ?, apds1 = ?, apds2 = ?, apds3 = ?, apds4 = ?, apds5 = ?, apds6 = ?, apds7 = ? WHERE id = 1', values)

        update_eggs_in_fridge()

        return 'OK'

    return 'OK'


def get_taken_count():
    count = 0
    with DB() as db:
        values_of_sensors = db.execute('SELECT apds0, apds1, apds2, apds3, apds4, apds5, apds6, apds7 FROM sensors WHERE id = 1').fetchone()

    for value in values_of_sensors:
        if value == 1:
            count += 1

    return count


def update_eggs_in_fridge():
    values = (
        get_taken_count(),
        1,
        2
    )
    with DB() as db:
        db.execute('UPDATE fridge SET quantity = ? WHERE user_id = ? AND product_id = ?', values)
