import requests
import random
import mysql.connector
from faker import Faker

# Conectando ao banco de dados
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",  # Insira sua senha aqui
        database="pipocando"
    )

    # Chave da API TMDb
    api_key = "2d01d0da6467094e9c7a26d73f53dc8c"

    # Criando um cursor
    cursor = conn.cursor()

    # Inicializando o Faker
    fake = Faker()

    # Função para obter dados reais de filmes da API TMDb
    def obter_filmes_tmdb(num_filmes):
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

    # Função para obter atores da API TMDb
    def obter_atores_tmdb(num_atores):
        atores = []
        pagina = 1
        while len(atores) < num_atores:
            url = f'https://api.themoviedb.org/3/person/popular?api_key={api_key}&language=pt-BR&page={pagina}'
            response = requests.get(url)
            data = response.json()
            if 'results' in data:
                atores.extend(data['results'])
                pagina += 1
            else:
                print("Erro: Não foi possível obter os atores da API TMDb.")
                break
        return atores[:num_atores]

    # Função para obter gêneros da API TMDb
    def obter_generos_tmdb():
        url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=pt-BR'
        response = requests.get(url)
        data = response.json()
        if 'genres' in data:
            return data['genres']
        else:
            print("Erro: Não foi possível obter os gêneros da API TMDb.")
            return []

    # Função para obter filmes, atores e gêneros da API TMDb
    def obter_filmes_atores_generos_tmdb(num_registros):
        filmes = obter_filmes_tmdb(num_registros['filme'])
        # Supondo que cada filme tenha até 5 atores principais
        atores = obter_atores_tmdb(num_registros['ator'])
        generos = obter_generos_tmdb()

        filmes_atores_generos = []

        for filme in filmes:
            # Selecionando atores aleatórios para o filme
            atores_filme = random.sample(
                atores, min(random.randint(1, 5), len(atores)))
            atores_ids = [ator['id'] for ator in atores_filme]

            # Selecionando gêneros aleatórios para o filme
            generos_filme = random.sample(
                generos, min(random.randint(1, 3), len(generos)))
            generos_ids = [genero['id'] for genero in generos_filme]

            filme_data = {
                **filme,
                'atores_ids': atores_ids,
                'generos_ids': generos_ids
            }
            filmes_atores_generos.append(filme_data)

        return filmes_atores_generos

    # Função para inserir dados na tabela diretor
    def popular_tabela_diretor(num_registros):
        for _ in range(num_registros['diretor']):
            nome_diretor = fake.name()
            cursor.execute(
                "INSERT INTO diretor (nome) VALUES (%s)", (nome_diretor,))
        conn.commit()

    # Função para inserir dados na tabela ator
    def popular_tabela_ator(num_registros):
        atores = obter_atores_tmdb(num_registros['ator'])
        for ator in atores:
            nome_ator = ator['name']
            cursor.execute("INSERT INTO ator (nome) VALUES (%s)", (nome_ator,))
        conn.commit()

    # Função para inserir dados na tabela genero
    def popular_tabela_genero(num_registros):
        generos = obter_generos_tmdb()
        for genero in generos:
            nome_genero = genero['name']
            cursor.execute(
                "INSERT INTO genero (nome) VALUES (%s)", (nome_genero,))
        conn.commit()

    # Função para inserir dados na tabela usuario
    def popular_tabela_usuario(num_registros):
        # Determinar o próximo ID disponível na tabela usuario
        cursor.execute("SELECT MAX(id) FROM usuario")
        max_id = cursor.fetchone()[0]
        next_id = max_id + 1 if max_id is not None else 1

        # Inserir registros com IDs sequenciais a partir do próximo ID disponível
        for i in range(num_registros['usuario']):
            nome = fake.user_name()
            email = fake.email()
            senha = fake.password(length=10)
            try:
                cursor.execute(
                    "INSERT INTO usuario (id, nome, email, senha) VALUES (%s, %s, %s, %s)", (next_id, nome, email, senha))
                conn.commit()
                print(f"Inserido registro de usuário com ID {next_id}")
            except mysql.connector.Error as err:
                print(f"Erro ao inserir registro de usuário com ID {next_id}: {err}")
            next_id += 1

    # Função para preencher os IDs de gênero na tabela filme_genero com números de 1 a 19
    def popular_tabela_filme_genero(filme_id, generos_ids):
        for genero_id in generos_ids:
            # Ajustando o ID do gênero para estar no intervalo de 1 a 19
            id_genero = genero_id % 19 + 1
            cursor.execute(
                "INSERT IGNORE INTO filme_genero (id_filme, id_genero) VALUES (%s, %s)", (filme_id, id_genero))

    # Função para preencher os IDs de ator na tabela filme_ator com números de 1 a 100
    def popular_tabela_filme_ator(filme_id, atores_ids):
        for ator_id in atores_ids:
            # Ajustando o ID do ator para estar no intervalo de 1 a 100
            id_ator = ator_id % 100 + 1
            cursor.execute(
                "INSERT IGNORE INTO filme_ator (id_ator, id_filme) VALUES (%s, %s)", (id_ator, filme_id))

    # Função para preencher as tabelas filme_ator e filme_genero
    def popular_tabelas_filme_ator_genero(filmes, num_registros):
        for filme in filmes:
            atores_ids = filme['atores_ids']
            generos_ids = filme['generos_ids']

            # Inserindo dados na tabela filme
            cursor.execute("INSERT INTO filme (nome, banner, sinopse, ano_lancamento, id_diretor) VALUES (%s, %s, %s, %s, %s)",
                           # Substituído o ID de diretor aleatório por um valor dentro do intervalo de IDs existentes
                           (filme['title'], f"https://image.tmdb.org/t/p/original/{filme['poster_path']}", filme['overview'], filme['release_date'], random.randint(1, num_registros['diretor'])))

            filme_id = cursor.lastrowid

            # Inserindo dados na tabela filme_ator
            popular_tabela_filme_ator(filme_id, atores_ids)

            # Inserindo dados na tabela filme_genero
            popular_tabela_filme_genero(filme_id, generos_ids)
        conn.commit()

    # Função para preencher a tabela de avaliação de forma desigual entre os usuários
    def popular_tabela_avaliacao_desigual(num_registros):
        contadorAvaliacao = 0

        for usuario_id in range(1, num_registros['usuario'] + 1):
            # Determina o número de avaliações para este usuário
            num_avaliacoes_usuario = random.randint(1, 100)

            for _ in range(num_avaliacoes_usuario):
                # Supondo que existam num_registros filmes na tabela filme
                id_filme = random.randint(1, num_registros['filme'])
                favorito = fake.boolean()
                texto = fake.paragraph(
                    nb_sentences=3) if random.random() < 0.5 else None
                nota = random.uniform(0, 10)
                data_avaliacao = fake.date_time_this_year()

                # Verificar se a avaliação já existe
                cursor.execute(
                    "SELECT COUNT(*) FROM avaliacao WHERE id_usuario = %s AND id_filme = %s", (usuario_id, id_filme))
                count = cursor.fetchone()[0]

                # Se a avaliação não existe, inserir
                if count == 0:
                    if contadorAvaliacao<1000:
                      cursor.execute("INSERT INTO avaliacao (id_usuario, id_filme, favorito, texto, nota, data_avaliacao) VALUES (%s, %s, %s, %s, %s, %s)",
                                   (usuario_id, id_filme, favorito, texto, nota, data_avaliacao))
                      conn.commit()
                      contadorAvaliacao += 1

    # Definindo o número de registros a serem inseridos
    num_registros = {
        'diretor': 25,
        'ator': 30,
        'genero': 19,
        'usuario': 15,
        'filme': 50
    }

    # Preenchendo todas as tabelas
    popular_tabela_diretor(num_registros)
    popular_tabela_ator(num_registros)
    popular_tabela_genero(num_registros)
    popular_tabela_usuario(num_registros)

    filmes = obter_filmes_atores_generos_tmdb(num_registros)
    popular_tabelas_filme_ator_genero(filmes, num_registros)

    popular_tabela_avaliacao_desigual(num_registros)

    # Fechando o cursor e a conexão
except mysql.connector.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
finally:
    # Fechando o cursor e a conexão
    cursor.close()
    conn.close()
