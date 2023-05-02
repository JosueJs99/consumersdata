from flask import Flask, render_template
import os, datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import cursor
from sqlalchemy.orm import backref
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.exceptions import abort

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))


app = Flask('__name__')
app.debug = True
app.config['SECRET_KEY'] ='your secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

#Tablelas de Banco de Dados

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    sobrenome = db.Column(db.String(30), nullable=False)

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clienteid = db.Column(db.Integer, db.ForeignKey('Cliente.id'))
    #cliente = db.relationship("NOME", backref=backref("nome", uselist=False))
    rua = db.Column(db.String(150), nullable=False)
    numero = db.Column(db.String(20))
    bairro = db.Column(db.String(50))
    complemento = db.Column(db.String(150))

class Telefone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(3), nullable=False)
    numero = db.Column(db.String(15), nullable=False)
    clienteid = db.Column(db.Integer, db.ForeignKey('Cliente.id'))
    #cliente = db.relationship("NOME", backref=backref("nome", uselist=False))

#Rotas

@app.route('/')
def index():
    clientesf = Cliente.query.all()
    return render_template('index.html', clientesf=clientesf)

@app.route('/clientes')
def clientes():
    return render_template('clientes.html',)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


#colocar inicio na tela base.html
