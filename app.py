from flask import Flask, render_template, request, redirect, url_for, flash, session
from clientes.clientes import clientes_blueprint


app = Flask(__name__)
app.register_blueprint(clientes_blueprint)


app.secret_key = '666666'
users = {
    "adm": "666"
}


# Contexto global para variável 'classe'
@app.context_processor
def inject_classe():
    return dict(classe='active')


@app.route('/')
def index():
    if 'username' in session:
        return render_template("index.html", route_name='index')
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
    return redirect(url_for('login'))


app.run(debug=True)
