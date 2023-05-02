
import sqlite3


connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Inserindo dados do cliente

cur.execute("INSERT INTO cliente (nome, sobrenome) VALUES (?, ?)",
            ('Ana','Luiza')
            )

cur.execute("INSERT INTO cliente (nome, sobrenome) VALUES (?, ?)",
            ('Bento','Rodrigues')
            )

cur.execute("INSERT INTO cliente (nome, sobrenome) VALUES (?, ?)",
            ('Carla', 'Castro')
            )

cur.execute("INSERT INTO cliente (nome, sobrenome) VALUES (?, ?)",
            ('Daniel', 'Almeida')
            )

# Inserindo o endereço do cliente

cur.execute("INSERT INTO endereco (clienteid, rua, numero, bairro, complemento) VALUES(?, ?, ?, ?, ?)",
           (1, 'São José', '638', 'Cidade Jardim', 'Bloco 2 Apt 23')
            )
cur.execute("INSERT INTO endereco (clienteid, rua, numero, bairro, complemento) VALUES(?, ?, ?, ?, ?)",
            (2, 'São Paulo','619','Centro','Bloco 1 Apt 10')
           )
cur.execute("INSERT INTO endereco (clienteid, rua, numero, bairro, complemento) VALUES(?, ?, ?, ?, ?)",
            (3, 'Santo Antônio', '554','Campus Valle','Casa 3')
            )
cur.execute("INSERT INTO endereco (clienteid, rua, numero, bairro, complemento) VALUES(?, ?, ?, ?, ?)",
            (4, 'Avenida Brasil', '532','Jardim dos Ipês','Proximo a barbearia do bil')
            )

#Inserindo o telefone de contato do cliente

cur.execute("INSERT INTO telefone (tipo, numero, clienteid) VALUES(?, ?, ?)",
            ('RES','4367-1585', 1)
            )

cur.execute("INSERT INTO telefone (tipo, numero, clienteid) VALUES(?, ?, ?)",
            ('CEL','9-9976-0133', 2)
            )
cur.execute("INSERT INTO telefone (tipo, numero, clienteid) VALUES(?, ?, ?)",
            ('RES','4580-1018', 3)
            )
cur.execute("INSERT INTO telefone (tipo, numero, clienteid) VALUES(?, ?, ?)",
            ('CEL','9-9622-1199', 4)
            )

connection.commit()
connection.close()

