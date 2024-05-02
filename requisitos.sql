-- Cria uma view que combina informações de filmes, atores, diretores e gêneros
create view filmes_atores_diretores as
select 
    f.id as id_filme,
    f.nome as nome_filme,
    f.ano_lancamento,
    d.nome as nome_diretor,
    group_concat(distinct a.nome separator ', ') as atores,
    group_concat(distinct g.nome separator ', ') as generos
from 
    filme f
join 
    diretor d on f.id_diretor = d.id
join 
    filme_ator fa on f.id = fa.id_filme
join 
    ator a on fa.id_ator = a.id
join 
    filme_genero fg on f.id = fg.id_filme
join 
    genero g on fg.id_genero = g.id
group by 
    f.id;

-- Cria uma view que combina informações sobre avaliações de filmes e usuários
create view avaliacoes_detalhadas as
select 
    a.id_usuario,
    u.nome as nome_usuario,
    f.id as id_filme,
    f.nome as nome_filme,
    f.ano_lancamento,
    fg.id_genero,
    g.nome as genero,
    a.favorito,
    a.texto as texto_avaliacao,
    a.nota,
    a.data_avaliacao
from 
    avaliacao a
join 
    filme f on a.id_filme = f.id
join 
    usuario u on a.id_usuario = u.id
join 
    filme_genero fg on f.id = fg.id_filme
join 
    genero g on fg.id_genero = g.id;

-- Cria uma view que mostra o nome do filme e sua respectiva nota média
create view medias_filmes as
select nome as filme, media from filme_media
join filme f where id_filme = f.id
order by nome;

-- Cria uma view que lista todos os filmes cadastrados
create view filmes_cadastrados as
select * from filme;


delimiter //
-- Cria um procedimento para obter os detalhes de um filme pelo ID do filme
create procedure detalhes_filme(in filme_id int)
begin
    select 
        nome_filme,
        ano_lancamento,
        nome_diretor,
        atores,
        generos
    from 
        filmes_atores_diretores
    where 
        id_filme = filme_id;
end//

-- Cria um procedimento para listar todas as avaliações de um filme específico pelo ID do filme
create procedure listar_avaliacoes_filme(in filme_id int)
begin
    select 
        nome_filme,
        nome_usuario,
        group_concat(distinct genero separator ', ') as generos,
        favorito,
        texto_avaliacao,
        nota,
        data_avaliacao
    from 
        avaliacoes_detalhadas
    where 
        id_filme = filme_id
    group by 
        nome_filme, nome_usuario, favorito, texto_avaliacao, nota, data_avaliacao;
end//

-- Cria uma procedure que calcula a quantidade de filmes por gênero
create procedure calcular_qtd_filmes_por_genero_simples_sem_truncate()
begin
    insert into qtd_filmes_genero (id_genero, qtd_filmes)
    select id_genero, count(*)
    from filme_genero
    group by id_genero
    on duplicate key update qtd_filmes = values(qtd_filmes);
end//

-- Cria uma procedure para listar filmes e banners por gênero
create procedure listar_filmes_e_banners_por_genero(
    in genero_nome varchar(20)
)
begin
    select
        f.nome as nome_filme,
        obter_banner_por_nome(f.nome) as banner
    from
        filme f
    inner join
        filme_genero fg on f.id = fg.id_filme
    inner join
        genero g on fg.id_genero = g.id
    where
        g.nome = genero_nome;
end//

-- Cria uma procedure para listar filmes favoritos de um usuário
create procedure listar_filmes_favoritos(idu int)
begin
    select f.nome as favoritos
    from usuario u, filme f
    where u.id = idu and verificar_favorito(u.id, f.id) = true
    order by f.nome;
end//

-- Cria uma procedure para verificar o nível de um usuário com base no número de avaliações
create procedure verificar_nivel_usuario(
    in usuario_id int
)
begin
    declare qtd_avaliacoes int;
    declare nivel_usuario varchar(10);

    select count(*) into qtd_avaliacoes
    from avaliacao
    where id_usuario = usuario_id;

    set nivel_usuario = nivel_usuario(qtd_avaliacoes);

    select nivel_usuario;
end//

-- Cria uma procedure para verificar se um usuário é válido
create procedure verificarusuario(
    in p_nome varchar(100),
    in p_senha varchar(20),
    out p_valido boolean
)
begin
    declare usuario_id int;
    
    select id into usuario_id
    from usuario
    where nome = p_nome and senha = p_senha;
    
    if usuario_id is not null then
        set p_valido = true;
    else
        set p_valido = false;
    end if;
end//

-- Cria uma procedure para listar os filmes
create procedure mostrar_filmes()
begin
   select nome,banner,sinopse,ano_lancamento
   from filmes_cadastrados;
end//

-- Cria uma procedure para retornar o ID do usuário com base no nome e senha
create procedure retornaIdUsuario(IN nome varchar(100), IN senha varchar(100))
begin
    select id
    from usuario
    where usuario.nome = nome and usuario.senha = senha;
end//

-- Cria uma procedure para retornar o ID do filme com base no nome do filme
create procedure retornIdFilme(IN nome_filme varchar(70))
begin
    select id from filme
    where nome = nome_filme;
end//

-- Cria uma função para obter o banner de um filme pelo nome do filme
create function obter_banner_por_nome(nome_filme varchar(70))
returns varchar(1000) deterministic
begin
    declare banner_filme varchar(1000);

    select banner into banner_filme from filme where nome = nome_filme limit 1;

    return banner_filme;
end//

-- Cria uma função para verificar se um usuário tem um filme como favorito
create function verificar_favorito(usuario_id int, filme_id int) 
returns boolean deterministic
begin
    declare favorito_boolean boolean;

    select favorito into favorito_boolean
    from avaliacao
    where id_usuario = usuario_id and id_filme = filme_id
    limit 1;

    return favorito_boolean;
end//

-- Cria uma função para determinar o nível do usuário com base no número de avaliações
create function nivel_usuario(qtd_avaliacoes int) 
returns varchar(10) deterministic
begin
    declare nivel varchar(10);

    if qtd_avaliacoes < 10 then
        set nivel = 'Bronze';
    elseif qtd_avaliacoes >= 10 and qtd_avaliacoes < 20 then
        set nivel = 'Prata';
    else
        set nivel = 'Ouro';
    end if;

    return nivel;
end//

-- Trigger que verifica se um novo usuário já existe na tabela antes de inserir
create trigger antes_de_inserir_usuario
before insert on usuario
for each row
begin
    declare usuario_existe int;
    
    select count(*) into usuario_existe
    from usuario
    where nome = new.nome;

    if usuario_existe > 0 then
        signal sqlstate '45000'
        set message_text = 'Erro: O usuário já existe na base de dados';
    end if;
end//

-- Trigger para calcular a média de avaliação após inserir uma nova avaliação
create trigger calcular_media_avaliacao
after insert on avaliacao
for each row
begin
    declare media_avaliacao float;
    declare existe_media int;
    
    select count(*) into existe_media from filme_media where id_filme = new.id_filme;

    if existe_media > 0 then
        select avg(nota) into media_avaliacao from avaliacao where id_filme = new.id_filme;
        update filme_media set media = media_avaliacao where id_filme = new.id_filme;
    else
        select avg(nota) into media_avaliacao from avaliacao where id_filme = new.id_filme;
        insert into filme_media (id_filme, media) values (new.id_filme, media_avaliacao);
    end if;
end//

-- Trigger para verificar se o tamanho do comentário não excede o limite máximo
create trigger limite_caracteres_comentario
before insert on comentario_avaliacao
for each row
begin
    declare limite_maximo int default 200;
    
    if length(new.texto) > limite_maximo then
        signal sqlstate '45000' set message_text = 'O comentário excede o limite máximo de caracteres permitidos.';
    end if;
end//

-- Trigger para impedir a atualização da nota de avaliação para o mesmo valor
create trigger before_update_avaliacao
before update on avaliacao
for each row
begin
    if old.nota = new.nota then
        signal sqlstate '45000' 
        set message_text = 'A nova nota é igual à nota existente. Não é permitido atualizar.';
    end if;
end//

-- Trigger para deletar as relações de um filme ao deletar um gênero
create trigger deletar_relacoes_filme_genero
before delete on genero
for each row
begin
    delete from filme_genero where id_genero = old.id;
end//

-- Trigger para atualizar o nível do usuário após inserir uma nova avaliação
create trigger atualizar_usuario_nivel after insert on avaliacao
for each row
begin
    declare qtd_avaliacoes int;
    declare nivel_atual varchar(10);

    select count(*) into qtd_avaliacoes from avaliacao where id_usuario = new.id_usuario;

    select nivel into nivel_atual from usuario_nivel where id_usuario = new.id_usuario;

    if nivel_atual is null then
        insert into usuario_nivel (id_usuario, nivel, qtd_avaliacoes_total) values (new.id_usuario, 'Bronze', 1);
    else
        update usuario_nivel set qtd_avaliacoes_total = qtd_avaliacoes_total + 1 where id_usuario = new.id_usuario;
    end if;

    select nivel_usuario(qtd_avaliacoes) into nivel_atual;

    update usuario_nivel set nivel = nivel_atual where id_usuario = new.id_usuario;
end//

-- Trigger para atualizar o nível do usuário após deletar uma avaliação
create trigger atualizar_nivel_after_delete
after delete on avaliacao
for each row
begin
    declare usuario_id int;
    declare qtd_avaliacoes int;
    declare nivel_usuario varchar(10);
    declare usuario_count int;

    set usuario_id = old.id_usuario;

    select count(*) into usuario_count from usuario_nivel where id_usuario = usuario_id;

    select count(*) into qtd_avaliacoes
    from avaliacao
    where id_usuario = usuario_id;

    select nivel_usuario into nivel_usuario from usuario_nivel where id_usuario = usuario_id;

    if usuario_count = 0 then
        insert into usuario_nivel (id_usuario, nivel, qtd_avaliacoes_total)
        values (usuario_id, nivel_usuario(qtd_avaliacoes), qtd_avaliacoes);
    else
        update usuario_nivel
        set nivel = nivel_usuario(qtd_avaliacoes), qtd_avaliacoes_total = qtd_avaliacoes
        where id_usuario = usuario_id;
    end if;
end//


-- Trigger para atualizar os contadores de filmes por gênero após atualizar o filme_genero
create trigger after_update_filme_genero
after update on filme_genero
for each row
begin
    declare contador int;
    declare genero_id_antigo int;
    declare genero_id_novo int;

    select old.id_genero into genero_id_antigo;
    select new.id_genero into genero_id_novo;

    update qtd_filmes_genero
    set qtd_filmes = (select count(*) from filme_genero where id_genero = genero_id_antigo)
    where id_genero = genero_id_antigo;

    update qtd_filmes_genero
    set qtd_filmes = (select count(*) from filme_genero where id_genero = genero_id_novo)
    where id_genero = genero_id_novo;
end//

DELIMITER $$

CREATE PROCEDURE atualiza_cadastro(IN id_user INT, IN novo_nome VARCHAR(100), IN nova_senha VARCHAR(20))
BEGIN
    UPDATE usuario
    SET nome = novo_nome, senha = nova_senha
    WHERE id = id_user;
END$$

DELIMITER ;

-- use pipocando3;
DELIMITER //
CREATE PROCEDURE delete_user(IN user_id INT)
BEGIN
    -- Excluir avaliações do usuário
    DELETE FROM avaliacao WHERE id_usuario = user_id;
    
    -- Excluir nível de usuário
    DELETE FROM usuario_nivel WHERE id_usuario = user_id;
    
    -- Finalmente, excluir o usuário
    DELETE FROM usuario WHERE id = user_id;
END//
DELIMITER ;