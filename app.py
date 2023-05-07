import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_cliente(cliente_id):
    conn = get_db_connection()
    cliente = conn.execute('SELECT * FROM cliente WHERE id = ?',
                        (cliente_id,)).fetchone()
    conn.close()
    if cliente is None:
        abort(404)
    return cliente


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
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']

        if not nome:
            flash('É necessário inserir o nome!')
        elif not sobrenome:
            flash('É necessário inserir o sobrenome!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO cliente (nome, sobrenome) VALUES (?, ?)',
                             (nome, sobrenome))
            conn.commit()
            conn.close()
            return redirect(url_for('clientes'))

    return render_template('cadastro.html')

@app.route('/<int:id>/editar/', methods=('GET', 'POST'))
def editar(id):
    cliente = get_cliente(id)

    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']

        if not nome:
            flash('É necessário inserir o nome!')
        elif not sobrenome:
            flash('É necessário inserir o sobrenome!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE cliente SET nome = ?, sobrenome = ?'
                         ' WHERE id = ?',
                         (nome, sobrenome, id))
            conn.commit()
            conn.close()
            return redirect(url_for('clientes'))

    return render_template('editar.html', cliente=cliente)

@app.route('/<int:id>/excluir/', methods=('POST',))
def excluir(id):
    cliente = get_cliente(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM cliente WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" foi excluido com sucesso!'.format(cliente['nome']))
    return redirect(url_for('clientes'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


#colocar inicio na tela base.html
