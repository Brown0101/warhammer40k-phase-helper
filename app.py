import re
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config.settings import FLASK_DEBUG, SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

import logging

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)


current_phase = ["All"]


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phase = db.Column(db.String(100))
    action = db.Column(db.String(100))
    type = db.Column(db.String(100))  # offensive, defensive, aura
    is_alive = db.Column(db.Boolean, default=True)
    display = db.Column(db.Boolean, default=True)

    def __init__(self, name, phase, action, type):
        self.name = name
        self.phase = phase
        self.action = action
        self.type = type


db.create_all()


@app.route('/')
def index():
    unit_data = Data.query.all()

    return render_template('pages/index.html', unit_data=unit_data, current_phase=current_phase)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        phase = request.form['phase']
        action = request.form['action']
        type = request.form['type']
        unit_data = Data(name, phase, action, type)
        db.session.add(unit_data)
        db.session.commit()

        flash("Unit was added successfully!")

        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        unit_data = Data.query.get(request.form.get('id'))

        unit_data.name = request.form['name']
        unit_data.phase = request.form['phase']
        unit_data.action = request.form['action']
        unit_data.type = request.form['type']

        db.session.commit()
        flash("Unit data updated successfully!")

        return redirect(url_for('index'))


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    unit_data = Data.query.all()

    for unit in unit_data:
        unit.display = True
        unit.is_alive = True

    current_phase[0] = "All"

    db.session.commit()

    if unit_data:
        logging.info(unit_data)
        flash("All units are now displayed.")
    else:
        flash(u"No units to display in this list.", "error")

    return redirect(url_for('index', current_phase=current_phase))


@app.route('/display/<name>', methods=['GET', 'POST'])
def display(name):
    unit_data = Data.query.all()

    for unit in unit_data:
        if unit.name == name:
            print("I FOUND THE UNIT")
            update_unit = Data.query.get(unit.id)
            update_unit.display = False

    db.session.commit()

    flash(f"{name} will not be displayed anymore.")

    return redirect(url_for('index'))


@app.route('/kill/<id>/', methods=['GET', 'POST'])
def kill(id):
    unit_data = Data.query.get(id)
    unit_data.is_alive = False
    db.session.commit()

    flash(f"{unit_data.name} was alive but status set to killed...")

    return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    unit_data = Data.query.get(id)
    db.session.delete(unit_data)
    db.session.commit()

    flash("Unit action(s) was removed successfully.")

    return redirect(url_for('index'))


@app.route('/phase/<text>/', methods=['GET', 'POST'])
def phase(text):
    if text == 'before':
        current_phase[0] = text.capitalize()
    else:
        current_phase[0] = text.capitalize()

    flash(f"Change to {current_phase[0]}")

    return redirect(url_for('index', current_phase=current_phase))


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)
