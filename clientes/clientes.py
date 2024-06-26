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
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = 10  # Número de registros por página
        offset = (page - 1) * per_page

        conn = get_db_connection()
        listar_clientes = conn.execute('SELECT * FROM clientes LIMIT ? OFFSET ?', (per_page, offset)).fetchall()

        # Obter o total de registros para calcular o número de páginas
        total_clientes = conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]
        conn.close()

        total_pages = (total_clientes + per_page - 1) // per_page

        return render_template('clientes.html', clientes=listar_clientes, page=page, total_pages=total_pages, route_name='clientes')
    else:
        return redirect(url_for('login'))



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


@clientes_blueprint.route('/procurar_clientes', methods=['GET'])
def procurar_clientes():
    if 'username' in session:
        query = request.args.get('query', '')

        conn = get_db_connection()
        listar_clientes = conn.execute("""
            SELECT * FROM clientes
            WHERE nome LIKE ? OR endereco LIKE ? OR telefone LIKE ? OR interesse LIKE ?
        """, ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%')).fetchall()
        conn.close()

        return render_template('clientes.html', clientes=listar_clientes, route_name='clientes')
    else:
        return redirect(url_for('login'))