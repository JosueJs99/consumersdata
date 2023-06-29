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

def get_endereco(endereco_id):
    conn = get_db_connection()
    endereco = conn.execute('SELECT * FROM endereco WHERE id = ?',
                        (endereco_id,)).fetchone()
    conn.close()
    if endereco is None:
        abort(404)
    return endereco

def get_telefone(telefone_id):
    conn = get_db_connection()
    telefone = conn.execute('SELECT * FROM telefone WHERE id = ?',
                        (telefone_id,)).fetchone()
    conn.close()
    if telefone is None:
        abort(404)
    return telefone


#Rotas

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes', methods=('GET', 'POST'))
def clientes():
    conn = get_db_connection()
    if request.method == 'POST':
        busca = request.form['busca'].capitalize()
        todos = conn.execute("SELECT t.tipo, t.telnum, i.rua, i.numero, i.bairro, i.complemento, l.id, l.nome, l.sobrenome \
                                FROM cliente l\
                                INNER JOIN endereco i\
                                ON i.clienteid = l.id \
                                INNER JOIN telefone t\
                                ON t.clienteid = l.id \
                                WHERE l.nome = (?)\
                                ORDER BY l.nome;",(busca,)).fetchall()
    else:
        todos = conn.execute('SELECT t.tipo, t.telnum, i.rua, i.numero, i.bairro, i.complemento, l.id, l.nome, l.sobrenome \
                                        FROM cliente l\
                                        INNER JOIN endereco i\
                                        ON i.clienteid = l.id \
                                        INNER JOIN telefone t\
                                        ON t.clienteid = l.id \
                                        ORDER BY l.id;').fetchall()

    conn.close()
    return render_template('clientes.html', todos=todos)

@app.route('/cadastro/', methods=('GET', 'POST'))
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        rua = request.form['rua']
        numero = request.form['numero']
        bairro = request.form['bairro']
        complemento = request.form['complemento']
        tipo = request.form['tipo'].upper()
        telnum = request.form['telnum']

        if not nome:
            flash('É necessário inserir o nome!')
        elif not sobrenome:
            flash('É necessário inserir o sobrenome!')
        elif not rua:
            flash('É necessário inserir a rua!')
        elif not numero:
            flash('É necessário inserir o numero da casa!')
        elif not bairro:
            flash('É necessário inserir o bairro!')
        elif not tipo:
            flash('É necessário selecionar o tipo de telefone!')
        elif tipo != 'CEL' and tipo != 'RES' and tipo != 'COM':
            flash('Tipo incorreto! Selecionar entre CEL para celular ou RES para residencial ou COM para Comercial.')
        elif not telnum:
            flash('É necessário inserir o telefone!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO cliente (nome, sobrenome) VALUES (?, ?)',
                             (nome, sobrenome))
            clienteid = conn.execute('SELECT id FROM cliente WHERE nome = (?);',
                                   (nome,)).fetchone()['id']

            conn.execute('INSERT INTO endereco (clienteid, rua, numero, bairro, complemento) VALUES (?, ?, ?, ?, ? )',
                         (clienteid, rua, numero, bairro, complemento))

            conn.execute('INSERT INTO telefone (clienteid, tipo, telnum) VALUES (?, ?, ?)',
                         (clienteid, tipo, telnum))

            conn.commit()
            conn.close()
            return redirect(url_for('clientes'))

    return render_template('cadastro.html')

@app.route('/<int:id>/editar/', methods=('GET', 'POST'))
def editar(id):
    cliente = get_cliente(id)
    endereco = get_endereco(id)
    telefone = get_telefone(id)

    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        rua = request.form['rua']
        numero = request.form['numero']
        bairro = request.form['bairro']
        complemento = request.form['complemento']
        tipo = request.form['tipo'].upper()
        telnum = request.form['telnum']


        if not nome:
            flash('É necessário inserir o nome!')
        elif not sobrenome:
            flash('É necessário inserir o sobrenome!')
        elif not rua:
            flash('É necessário inserir a rua!')
        elif not numero:
            flash('É necessário inserir o numero da casa!')
        elif not bairro:
            flash('É necessário inserir o bairro!')
        elif not tipo:
            flash('É necessário selecionar o tipo de telefone!')
        elif tipo != 'CEL' and tipo != 'RES' and tipo != 'COM':
            flash('Tipo incorreto! Selecionar entre CEL para celular ou RES para residencial ou COM para Comercial.')
        elif not telnum:
            flash('É necessário inserir o telefone!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE cliente SET nome = ?, sobrenome = ?'
                         ' WHERE id = ?',
                         (nome, sobrenome, id))

            conn.execute('UPDATE endereco SET rua = ?, numero = ?, bairro = ?, complemento = ?'
                         ' WHERE id = ?',
                         (rua, numero, bairro, complemento, id))

            conn.execute('UPDATE telefone SET tipo = ?, telnum = ?'
                         ' WHERE id = ?',
                         (tipo, telnum, id))
            conn.commit()
            conn.close()
            return redirect(url_for('clientes'))

    return render_template('editar.html', cliente=cliente, endereco=endereco, telefone=telefone)

@app.route('/<int:id>/excluir/', methods=('POST',))
def excluir(id):
    cliente = get_cliente(id)
    endereco = get_endereco(id)
    telefone = get_telefone(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM cliente WHERE id = ?', (id,))
    conn.execute('DELETE FROM endereco WHERE id = ?', (id,))
    conn.execute('DELETE FROM telefone WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" foi excluido com sucesso!'.format(cliente['nome']))
    return redirect(url_for('clientes'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


#colocar inicio na tela base.html
