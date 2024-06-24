from flask import Blueprint, Flask, request, redirect, url_for, render_template, session, flash
import sqlite3


vendas_blueprint = Blueprint('vendas', __name__, template_folder='templates')


@vendas_blueprint.route('/vendas')
def vendas():
    if 'username' in session:
        return render_template('vendas.html', route_name='vendas')
    else:
        return redirect(url_for('login'))