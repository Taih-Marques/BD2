from faker import Faker
import requests
import random
import mysql.connector

# Conectando ao banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pipocando"
)

# Criando um cursor
cursor = conn.cursor()

# Inicializando o Faker
fake = Faker()

# Função para obter dados reais de filmes da API TMDb
def obter_filmes_tmdb(num_filmes):
    api_key = '41f3ff693475e55ec20d2e275b3dbdbd'
    filmes = []
    pagina = 1
    while len(filmes) < num_filmes:
        url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=pt-BR&sort_by=popularity.desc&include_adult=false&include_video=false&page={pagina}'
        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            filmes.extend(data['results'])
            pagina += 1
        else:
            print("Erro: Não foi possível obter os filmes da API TMDb.")
            break

    return filmes[:num_filmes]


# Função para inserir dados na tabela diretor
def popular_tabela_diretor(num_registros):
    for _ in range(num_registros):
        nome_diretor = fake.name()
        cursor.execute("INSERT INTO diretor (nome) VALUES (%s)", (nome_diretor,))

# Função para inserir dados na tabela ator
def popular_tabela_ator(num_registros):
    for _ in range(num_registros):
        nome_ator = fake.name()
        cursor.execute("INSERT INTO ator (nome) VALUES (%s)", (nome_ator,))

# Função para inserir dados na tabela genero
def popular_tabela_genero(num_registros):
    for _ in range(num_registros):
        nome_genero = fake.word()
        cursor.execute("INSERT INTO genero (nome) VALUES (%s)", (nome_genero,))

# Função para inserir dados na tabela usuario
def popular_tabela_usuario(num_registros):
    for _ in range(num_registros):
        nome_usuario = fake.name()
        email_usuario = fake.email()
        senha_usuario = fake.password()
        cursor.execute("INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)", (nome_usuario, email_usuario, senha_usuario))

# Função para inserir dados na tabela filme
def popular_tabela_filme_com_tmdb(num_registros):
    filmes = obter_filmes_tmdb(num_registros)
    for filme in filmes:
        nome_filme = filme['title']
        banner = f"https://image.tmdb.org/t/p/original/{filme['poster_path']}"
        sinopse = filme['overview']
        ano_lancamento = filme['release_date']
        id_diretor = random.randint(1, 100)  # Supondo que existam 100 diretores na tabela diretor
        cursor.execute("INSERT INTO filme (nome, banner, sinopse, ano_lancamento, id_diretor) VALUES (%s, %s, %s, %s, %s)",
                       (nome_filme, banner, sinopse, ano_lancamento, id_diretor))

# Função para inserir dados na tabela filme_ator
def popular_tabela_filme_ator(num_registros):
    for _ in range(num_registros):
        id_ator = random.randint(1, 100)  # Supondo que existam 100 atores na tabela ator
        id_filme = random.randint(1, 1000)  # Supondo que existam 1000 filmes na tabela filme
        cursor.execute("INSERT INTO filme_ator (id_ator, id_filme) VALUES (%s, %s)", (id_ator, id_filme))

# Função para inserir dados na tabela filme_genero
def popular_tabela_filme_genero(num_registros):
    for _ in range(num_registros):
        id_filme = random.randint(1, 1000)  # Supondo que existam 1000 filmes na tabela filme
        id_genero = random.randint(1, 100)  # Supondo que existam 100 gêneros na tabela genero
        cursor.execute("INSERT INTO filme_genero (id_filme, id_genero) VALUES (%s, %s)", (id_filme, id_genero))

# Função para inserir dados na tabela avaliacao
def popular_tabela_avaliacao(num_registros):
    for _ in range(num_registros):
        id_usuario = random.randint(1, 100)  # Supondo que existam 100 usuários na tabela usuario
        id_filme = random.randint(1, 1000)  # Supondo que existam 1000 filmes na tabela filme
        assistido = fake.boolean()
        favorito = fake.boolean()
        texto = fake.paragraph(nb_sentences=3) if random.random() < 0.5 else None
        nota = random.uniform(0, 10)
        data_avaliacao = fake.date_time_this_year()
        cursor.execute("INSERT INTO avaliacao (id_usuario, id_filme, assistido, favorito, texto, nota, data_avaliacao) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (id_usuario, id_filme, assistido, favorito, texto, nota, data_avaliacao))

# Função para inserir dados na tabela comentario_avaliacao
def popular_tabela_comentario_avaliacao(num_registros):
    for _ in range(num_registros):
        id_avaliacao = random.randint(1, 1000)  # Supondo que existam 1000 avaliações na tabela avaliacao
        id_usuario = random.randint(1, 100)  # Supondo que existam 100 usuários na tabela usuario
        texto = fake.paragraph(nb_sentences=3)
        data_comentario = fake.date_time_this_year()
        cursor.execute("INSERT INTO comentario_avaliacao (id_avaliacao, id_usuario, texto, data_comentario) VALUES (%s, %s, %s, %s)",
                       (id_avaliacao, id_usuario, texto, data_comentario))

# Função para inserir dados na tabela curtida_avaliacao
def popular_tabela_curtida_avaliacao(num_registros):
    for _ in range(num_registros):
        id_avaliacao = random.randint(1, 1000)  # Supondo que existam 1000 avaliações na tabela avaliacao
        id_usuario = random.randint(1, 100)  # Supondo que existam 100 usuários na tabela usuario
        cursor.execute("INSERT INTO curtida_avaliacao (id_avaliacao, id_usuario) VALUES (%s, %s)", (id_avaliacao, id_usuario))

# Definindo o número de registros a serem inseridos (1000 registros no total)
num_registros = 1000

# Populando todas as tabelas
popular_tabela_diretor(num_registros)
popular_tabela_ator(num_registros)
popular_tabela_genero(num_registros)
popular_tabela_usuario(num_registros)
popular_tabela_filme_com_tmdb(num_registros)
popular_tabela_filme_ator(int(num_registros * 0.8))  # 80% das tuplas
popular_tabela_filme_genero(num_registros)
popular_tabela_avaliacao(num_registros)
popular_tabela_comentario_avaliacao(num_registros)
popular_tabela_curtida_avaliacao(num_registros)

# Commitando as alterações
conn.commit()

# Fechando o cursor e a conexão
cursor.close()
conn.close()
