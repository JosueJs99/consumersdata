import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


#Rotas

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    conn = get_db_connection()
    cliente = conn.execute('SELECT * FROM cliente').fetchall()
    conn.close()
    return render_template('clientes.html', cliente=cliente)

@app.route('/cadastro/', methods=('GET', 'POST'))
def cadastro():
    if request.method == 'post':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']

        if not nome:
            flash('É necessário inserir o nome!')
        elif not sobrenome:
            flash('É necessário inserir o nome!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO cliente (nome, sobrenome) VALUES (?, ?)',
                             (nome, sobrenome))
            conn.commit()
            conn.close()
            return redirect(url_for('clientes'))

    return render_template('cadastro.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


#colocar inicio na tela base.html
