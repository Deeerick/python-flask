from flask import Blueprint, Flask, request, redirect, url_for, render_template, session, flash
import sqlite3


produtos_blueprint = Blueprint('produtos', __name__, template_folder='templates')


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@produtos_blueprint.route('/produtos')
def produtos():
    if 'username' in session:
        return render_template('produtos.html', route_name='produtos')
    else:
        return redirect(url_for('login'))