DROP TABLE IF EXISTS cliente;
DROP TABLE IF EXISTS endereco;
DROP TABLE IF EXISTS telefone;

CREATE TABLE cliente(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nome TEXT(30) NOT NULL,
	sobrenome TEXT(30) NOT NULL
);

CREATE TABLE endereco(
	id INT(10) PRIMARY KEY,
	clienteid INT,
	rua TEXT(150) NOT NULL,
	numero TEXT(20),
	bairro TEXT(50) NOT NULL,
	complemento TEXT (150),
	CONSTRAINT fk_endereco_cliente FOREIGN KEY(clienteid) REFERENCES cliente(id)
);

CREATE TABLE telefone(
	id INT PRIMARY KEY,
	tipo TEXT(3) NOT NULL,
	numero TEXT(15) NOT NULL,
	clienteid INT,
	CHECK (TIPO IN ('RES','COM','CEL')),
	FOREIGN KEY(clienteid) REFERENCES cliente(id)
);