create database if not exists pipocando;

use pipocando;

drop table if exists curtida_avaliacao;

drop table if exists comentario_avaliacao;

drop table if exists avaliacao;

drop table if exists filme_genero;

drop table if exists filme_ator;

drop table if exists filme;

drop table if exists usuario;

DROP TABLE IF EXISTS genero;

drop table if exists ator;

drop table if exists diretor;

create table diretor(
  id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nome varchar(100) NOT NULL
);

create table ator(
  id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nome varchar (100) NOT NULL
);

CREATE TABLE genero(
  id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nome varchar(20) NOT NULL
);

CREATE TABLE usuario(
  id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nome varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  senha varchar(20) NOT NULL
);

CREATE TABLE filme(
  id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nome varchar(70) NOT NULL,
  banner varchar(1000) NOT NULL,
  sinopse text (2000) NOT NULL,
  ano_lancamento date NOT NULL,
  id_diretor int NOT NULL,
  FOREIGN KEY (id_diretor) REFERENCES diretor(id) ON DELETE CASCADE
);

CREATE TABLE filme_ator(
  id_ator int NOT NULL,
  id_filme int NOT NULL,
  FOREIGN KEY (id_ator) REFERENCES ator(id) ON DELETE CASCADE,
  FOREIGN KEY (id_filme) REFERENCES filme(id) ON DELETE CASCADE
);

CREATE TABLE filme_genero(
  id_filme int NOT NULL,
  id_genero int NOT NULL,
  FOREIGN KEY (id_filme) REFERENCES filme(id) ON DELETE CASCADE,
  FOREIGN KEY (id_genero) REFERENCES genero(id) ON DELETE CASCADE
);

CREATE TABLE avaliacao(
  id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  id_usuario int NOT NULL,
  id_filme int NOT NULL,
  assistido boolean DEFAULT false,
  favorito boolean DEFAULT false,
  texto text,
  nota float,
  data_avaliacao datetime NOT NULL,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
  FOREIGN KEY (id_filme) REFERENCES filme(id) ON DELETE CASCADE
);

CREATE TABLE comentario_avaliacao(
  id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  id_avaliacao int NOT NULL,
  id_usuario int NOT NULL,
  texto text NOT NULL,
  data_comentario datetime NOT NULL,
  FOREIGN KEY (id_avaliacao) REFERENCES avaliacao(id) ON DELETE CASCADE,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);

CREATE TABLE curtida_avaliacao(
  id_avaliacao int NOT NULL,
  id_usuario int NOT NULL,
  FOREIGN KEY (id_avaliacao) REFERENCES avaliacao(id) ON DELETE CASCADE,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);