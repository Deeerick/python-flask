from flask import Flask, render_template, request, redirect, url_for, flash, session


app = Flask(__name__)
app.secret_key = '666666'

users = {
    "adm": "666"
}


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


@app.route('/home')
def home():
    return render_template("index.html")


app.run(debug=True)