import sys
import mysql.connector


# Função para estabelecer conexão com o banco de dados MySQL
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pipocando"
    )


# Função para cadastrar um novo usuário no banco de dados
def cadastrar_usuario(nome_usuario, email, senha_usuario):
    try:
        # Define 'res' como 1, supondo que o usuário será cadastrado com sucesso
        res = 1
        # Estabelece conexão com o banco de dados
        conexao = conectar()
        cursor = conexao.cursor()
        # Executa a inserção na tabela 'usuario'
        cursor.execute("INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)",
                       (nome_usuario, email, senha_usuario))
        # Comita as mudanças no banco de dados
        conexao.commit()
    except mysql.connector.Error as err:
        # Se ocorrer um erro específico indicando que o usuário já existe, define 'res' como 0
        if err.errno == 1644:
            res = 0
    finally:
        # Fecha o cursor e a conexão com o banco de dados e retorna 'res'
        cursor.close()
        conexao.close()
        return res


# Função para validar as credenciais de um usuário
def validar_usuario(nome_usuario, senha_usuario):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Executa uma stored procedure para verificar as credenciais do usuário
        cursor.execute("CALL VerificarUsuario(%s, %s, @valido)",
                       (nome_usuario, senha_usuario))
        cursor.execute("SELECT @valido")
        # Retorna o valor da variável @valido que foi definida pela stored procedure
        valido = cursor.fetchone()[0]
        return valido
    finally:
        cursor.close()
        conexao.close()

# Função para mostrar todos os filmes cadastrados no banco de dados


def mostrar_filmes():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Executa uma stored procedure para listar todos os filmes
        cursor.execute("CALL mostrar_filmes()")
        resultados = cursor.fetchall()
        print('\n')
        for nome, banner, sinopse, ano_lancamento in resultados:
            print(f"Filme: {nome}, Banner: {banner}, Sinopse: {
                  sinopse}, Ano: {ano_lancamento}")
            print('\n')
    finally:
        cursor.close()
        conexao.close()

# Função para mostrar a média das notas dos filmes cadastrados


def mostrar_media_filmes():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Executa uma consulta para obter a média das notas dos filmes
        cursor.execute("SELECT * FROM medias_filmes;")
        resultados = cursor.fetchall()
        print('\n')
        for filme, media in resultados:
            print(f"Filme: {filme}, Média: {media}")
        print('\n')
    finally:
        cursor.close()
        conexao.close()


# Função para listar filmes e banners de um determinado gênero
def listar_filmes_e_banners_por_genero(genero):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Verifica se o gênero fornecido está presente na base de dados
        cursor.execute(f"SELECT 1 FROM genero WHERE nome = '{genero}'")
        genero_valido = cursor.fetchone()

        if genero_valido:
            # Se o gênero existe, executa uma stored procedure para listar os filmes desse gênero
            cursor.execute(
                "CALL listar_filmes_e_banners_por_genero(%s)", (genero,))
            resultados = cursor.fetchall()
            if resultados:
                print('\n')
                for nome_filme, banner in resultados:
                    print(f"Filme: {nome_filme}, Banner: {banner}")
                print('\n')
            else:
                print(f"Nenhum filme possui o gênero '{
                      genero}' na base de dados.")
        else:
            print(f"Nenhum filme possui o gênero '{genero}' na base de dados.")
    finally:
        cursor.close()
        conexao.close()


# Função para listar as avaliações de um filme
def listar_avaliacoes_filme(filme_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Executa uma stored procedure para listar as avaliações de um filme
        cursor.execute("CALL listar_avaliacoes_filme(%s)", (filme_id,))
        resultados = cursor.fetchall()
        print("\n")
        for nome_filme, nome_usuario, generos, favorito, texto_avaliacao, nota, data_avaliacao in resultados:
            print(f"Filme: {nome_filme}, Usuário: {nome_usuario}, Gêneros: {generos}, Favorito: {
                  favorito}, Texto: {texto_avaliacao}, Nota: {nota}, Data: {data_avaliacao}")
    finally:
        cursor.close()
        conexao.close()


# Função para verificar o nível de um usuário no sistema
def verificar_nivel_usuario(credencialID):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Executa uma stored procedure para verificar o nível do usuário
        cursor.execute("CALL  verificar_nivel_usuario(%s)", (credencialID,))
        resultado = cursor.fetchone()
        print("\n")
        if resultado is not None:
            print(f"Seu nível é: {resultado[0]}")
        elif resultado == None:
            print("Você ainda não realizou nenhuma avaliação")
        else:
            print("Usuário não encontrado ou erro na consulta.")
    finally:
        cursor.close()
        conexao.close()


# Função para retornar o ID de um usuário baseado no nome e senha
def retornaIdUsuario(nome, senha):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Executa uma stored procedure para retornar o ID do usuário
        cursor.execute("CALL retornaIdUsuario(%s,%s)", (nome, senha))
        resultado = cursor.fetchone()[0]
        return resultado
    finally:
        cursor.close()
        conexao.close()


def retornaIdFilme(filme):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("CALL retornIdFilme(%s)", (filme,))
        resultados = cursor.fetchall()
        if resultados:
            # Supondo que apenas uma linha é retornada
            id_filme = resultados[0][0]
            return id_filme
        else:
            print("Filme não encontrado.")
            return None
    finally:
        cursor.close()
        conexao.close()


# Função para cadastrar uma avaliação de um filme
def cadastrar_avaliacao(id_usuario, id_filme, favorito, texto, nota):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Obtendo a data atual
        cursor.execute("SELECT current_timestamp()")
        data = cursor.fetchone()[0]

        # Inserindo a avaliação na tabela 'avaliacao'
        cursor.execute("INSERT INTO avaliacao (id_usuario, id_filme, favorito, texto, nota, data_avaliacao) VALUES (%s, %s, %s, %s, %s, %s)",
                       (id_usuario, id_filme, favorito, texto, nota, data))

        conexao.commit()
        print("\n")
        print("Avaliação cadastrada com sucesso")
    except mysql.connector.Error as err:
        print("Ocorreu um erro ao cadastrar avaliação:", err)
    finally:
        cursor.close()
        conexao.close()


# Função para mostrar detalhes de um filme
def mostrar_detalhes_filmes(id_filme):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Executa uma stored procedure para obter os detalhes de um filme
        cursor.execute("CALL detalhes_filme(%s)", (id_filme,))
        resultados = cursor.fetchall()
        print("\n")
        for nome_filme, ano_lancamento, nome_diretor, atores, generos in resultados:
            print(f"Filme: {nome_filme}, Ano: {ano_lancamento}, Diretor: {
                  nome_diretor}, Atores: {atores}, Gênero: {generos}")
    finally:
        cursor.close()
        conexao.close()


# Função para listar os filmes favoritos de um usuário
def mostra_favoritos(id_usuario):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Executa uma stored procedure para listar os filmes favoritos de um usuário
        cursor.execute("CALL listar_filmes_favoritos(%s)", (id_usuario,))
        resultados = cursor.fetchall()
        if resultados:
            print("\n")
            print("Filmes favoritos:")
            for favorito in resultados:
                print(favorito[0])
        else:
            print("Você não tem nenhum filme favoritado.")
        print("\n")
    finally:
        cursor.close()
        conexao.close()


# Função para atualizar o cadastro de um usuário (nome de usuário e senha)
def atualiza_cadastro(id_usuario, novoNome, novaSenha):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Executa uma stored procedure para atualizar o cadastro do usuário
        cursor.execute("CALL atualiza_cadastro (%s,%s,%s)",
                       (id_usuario, novoNome, novaSenha))
        conexao.commit()
        print("Cadastro atualizado com sucesso")
    except mysql.connector.Error as err:
        print("Ocorreu um erro ao cadastrar as novas credenciais", err)
    finally:
        cursor.close()
        conexao.close()


# Função para excluir o cadastro de um usuário
def exclui_cadastro(id_usuario):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Executa uma stored procedure para excluir o cadastro do usuário
        cursor.execute("CALL delete_user(%s)", (id_usuario,))
        conexao.commit()
        print("Conta excluída com sucesso")
    except mysql.connector.Error as err:
        print("Ocorreu um erro ao cadastrar as novas credenciais", err)
    finally:
        cursor.close()
        conexao.close()


# Função principal que inicia o programa e direciona para o menu apropriado
def main():
    while True:
        nome_usuario = input("Digite o nome de usuário: ")
        senha_usuario = input("Digite a senha: ")

        valido = validar_usuario(nome_usuario, senha_usuario)

        if valido:
            credencialID = retornaIdUsuario(nome_usuario, senha_usuario)
            if credencialID is not None:
                menu_usuario_valido(credencialID)
            else:
                print("Não existe id para esse usuário")
        else:
            menu_usuario_nao_valido()


# Menu para usuários válidos
def menu_usuario_valido(credencialID):
    while True:
        print('\n')
        print("Usuário válido. Escolha uma opção:")
        print("1 - Mostrar filmes cadastrados")
        print("2 - Mostrar média das notas dos filmes")
        print("3 - Listar filmes e banners por gênero")
        print("4 - Fazer avaliação de um filme")
        print("5 - Listar filmes favoritos")
        print("6 - Verificar nível no sistema")
        print("7 - Verificar detalhes filme")
        print("8 - Listar avaliações de um filme")
        print("9 - Atualizar cadastro(nome de usuário e senha)")
        print("10 - Excluir conta")
        print("11 - Encerrar o programa")

        opcao = int(input("Opção: "))

        if opcao == 1:
            mostrar_filmes()
        elif opcao == 2:
            mostrar_media_filmes()
        elif opcao == 3:
            genero = input("Digite o gênero: ")
            listar_filmes_e_banners_por_genero(genero)
        elif opcao == 4:
            mostrar_filmes()
            filme = input("Digite o nome do filme: ")
            idFilme = retornaIdFilme(filme)
            favorito = int(
                input("Digite 1 se você favorita o filme e 0 se você não favorita: "))
            texto = input(
                "Digite algum comentário, se desejar, sobre o filme: ")
            nota = float(input("Digite uma nota para o filme: "))
            cadastrar_avaliacao(credencialID, idFilme, favorito, texto, nota)
        elif opcao == 5:
            mostra_favoritos(credencialID)
        elif opcao == 6:
            verificar_nivel_usuario(credencialID)
        elif opcao == 7:
            mostrar_filmes()
            filme = input("Digite o nome do filme: ")
            idFilme = retornaIdFilme(filme)
            mostrar_detalhes_filmes(idFilme)
        elif opcao == 8:
            mostrar_filmes()
            filme = input("Digite o nome do filme: ")
            idFilme = retornaIdFilme(filme)
            listar_avaliacoes_filme(idFilme)
        elif opcao == 9:
            novoNome = input("Digite um novo nome de usuário: ")
            novaSenha = input("Digite uma nova senha: ")
            atualiza_cadastro(credencialID, novoNome, novaSenha)
            break
        elif opcao == 10:
            exclui_cadastro(credencialID)
            break
        elif opcao == 11:
            print("\n")
            print("Encerrando o programa...")
            sys.exit(0)
        else:
            print("\n")
            print("Opção inválida, digite novamente")


# Menu para usuários não cadastrados
def menu_usuario_nao_valido():
    while True:
        print('\n')
        print("Usuário não cadastrado. Escolha uma opção:")
        print("1 - Mostrar filmes cadastrados")
        print("2 - Mostrar média das notas dos filmes")
        print("3 - Listar filmes e banners por gênero")
        print("4 - Se cadastrar")
        print("5 - Encerrar o programa")

        opcao = int(input("Opção: "))

        if opcao == 1:
            mostrar_filmes()
        elif opcao == 2:
            mostrar_media_filmes()
        elif opcao == 3:
            genero = input("Digite o gênero: ")
            listar_filmes_e_banners_por_genero(genero)
        elif opcao == 4:
            efetuou = cadastrar_usuario(input("Digite seu nome: "), input(
                "Digite email: "), input("Digite uma senha: "))
            if efetuou == 1:
                print("\n")
                print("Usuário inserido com sucesso.")
                break
            elif efetuou == 0:
                print("\n")
                print("Usuário já cadastrado na base de dados.")
                break
            else:
                print("\n")
                print("Erro ao cadastrar usuário.")
                continue
        elif opcao == 5:
            print("\n")
            print("Encerrando o programa...")
            sys.exit(0)
        else:
            print("\n")
            print("Opção inválida, digite novamente")


if __name__ == "__main__":
    main()
