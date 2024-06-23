from flask import Blueprint, Flask, request, redirect, url_for, render_template, session, flash
import sqlite3


clientes_blueprint = Blueprint('clientes', __name__, template_folder='templates')


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@clientes_blueprint.route('/clientes')
def clientes():
    if 'username' in session:
        conn = get_db_connection()
        listar_clientes = conn.execute('SELECT * FROM clientes').fetchall()
        conn.close()
        return render_template('clientes.html', clientes=listar_clientes, route_name='clientes')
    else:
        return redirect(url_for('clientes.login'))


@clientes_blueprint.route('/novo_cliente', methods=['GET', 'POST'])
def novo_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        interesse = request.form['interesse']

        conn = get_db_connection()
        conn.execute('INSERT INTO clientes (nome, endereco, telefone, interesse) VALUES (?, ?, ?, ?)',
                     (nome, endereco, telefone, interesse))
        conn.commit()
        conn.close()

        flash('Cliente registrado com sucesso!', 'success')
        return redirect(url_for('clientes.clientes'))

    return render_template("index.html")


@clientes_blueprint.route('/eliminar_cliente/<int:cliente_id>', methods=['POST'])
def eliminar_cliente(cliente_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    conn.close()
    flash('Cliente eliminado com sucesso!', 'danger')
    return redirect(url_for('clientes.clientes'))