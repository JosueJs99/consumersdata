import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


#Rotas

@app.route('/')
def index():
    conn = get_db_connection()
    cliente = conn.execute('SELECT * FROM cliente').fetchall()
    conn.close()
    return render_template('index.html', cliente=cliente)

@app.route('/clientes')
def clientes():
    conn = get_db_connection()
    cliente = conn.execute('SELECT * FROM cliente').fetchall()
    conn.close()
    return render_template('clientes.html', cliente=cliente)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


#colocar inicio na tela base.html
