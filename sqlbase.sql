create database if not exists pipocando;

use pipocando;

drop table if exists curtida_avaliacao;

drop table if exists comentario_avaliacao;

drop table if exists avaliacao;

drop table if exists filme_genero;

drop table if exists filme_ator;

drop table if exists qtd_filmes_genero;

drop table if exists filme_media;

drop table if exists filme;

drop table if exists usuario_nivel;

drop table if exists usuario;

drop table if exists genero;

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

CREATE TABLE usuario_nivel (
    id_usuario INT NOT NULL PRIMARY KEY,
    nivel VARCHAR(10),
    qtd_avaliacoes_total INT,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);

CREATE TABLE filme(
  id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nome varchar(70) NOT NULL,
  banner varchar(1000) NOT NULL,
  sinopse text NOT NULL,
  ano_lancamento date NOT NULL,
  id_diretor int NOT NULL,
  FOREIGN KEY (id_diretor) REFERENCES diretor(id) ON DELETE CASCADE
);

CREATE TABLE filme_ator(
  id_filme int NOT NULL,
  id_ator int NOT NULL,
  PRIMARY KEY (id_filme, id_ator),
  FOREIGN KEY (id_filme) REFERENCES filme(id) ON DELETE CASCADE,
  FOREIGN KEY (id_ator) REFERENCES ator(id) ON DELETE CASCADE
);

CREATE TABLE filme_genero(
  id_filme int NOT NULL,
  id_genero int NOT NULL,
  PRIMARY KEY (id_filme, id_genero),
  FOREIGN KEY (id_filme) REFERENCES filme(id) ON DELETE CASCADE,
  FOREIGN KEY (id_genero) REFERENCES genero(id) ON DELETE CASCADE
);

create table filme_media(
	id int not null primary key auto_increment,
	id_filme int not null,
    media float,
    foreign key(id_filme) references filme(id) on delete cascade
);

CREATE TABLE avaliacao(
  id_usuario int NOT NULL,
  id_filme int NOT NULL,
  favorito boolean DEFAULT false,
  texto text,
  nota float,
  data_avaliacao datetime NOT NULL,
  PRIMARY KEY (id_usuario, id_filme),
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
  FOREIGN KEY (id_filme) REFERENCES filme(id) ON DELETE CASCADE
);

CREATE TABLE qtd_filmes_genero (
    id_genero INT NOT NULL PRIMARY KEY,
    qtd_filmes INT,
    FOREIGN KEY (id_genero) REFERENCES genero(id) ON DELETE CASCADE
);

CREATE TABLE comentario_avaliacao(
  id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  id_usuario int NOT NULL,
  id_filme int NOT NULL,
  texto text NOT NULL,
  data_comentario datetime NOT NULL,
  FOREIGN KEY (id_usuario, id_filme) REFERENCES avaliacao(id_usuario, id_filme) ON DELETE CASCADE,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);

CREATE TABLE curtida_avaliacao(
  id_avaliacao int NOT NULL,
  id_usuario int NOT NULL,
  id_filme int NOT NULL,
  PRIMARY KEY (id_avaliacao, id_usuario),
  FOREIGN KEY (id_usuario, id_filme) REFERENCES avaliacao(id_usuario, id_filme) ON DELETE CASCADE,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);