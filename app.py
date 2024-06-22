from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3


app = Flask(__name__)
app.secret_key = '666666'

users = {
    "adm": "666"
}


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    if 'username' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            flash('Login bem Sucedido!', 'success')
            return redirect(url_for('index'))

        else:
            flash('Login não realizado', 'danger')

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Você foi desconectado!', 'success')
    return redirect(url_for('login'))


@app.route('/clientes')
def clientes():
    if 'username' in session:
        conn = get_db_connection()
        listar_clientes = conn.execute('SELECT * FROM clientes').fetchall()
        conn.close()
        return render_template('clientes.html', clientes=listar_clientes)
    else:
        return redirect(url_for('login'))


@app.route('/novo_cliente', methods=['GET', 'POST'])
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
        return redirect(url_for('clientes'))

    return render_template("index.html")


@app.route('/eliminar_cliente/<int:cliente_id>', methods=['POST'])
def eliminar_cliente(cliente_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    conn.close()
    flash('Cliente eliminado com sucesso!', 'success')
    return redirect(url_for('clientes'))


app.run(debug=True)
