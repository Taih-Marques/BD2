# Projeto Avaliativo - BD2

Projeto de Banco de dados 2 de avaliação de filmes com recursos: visões, trigger e procedures e apis para acessos à consulta ao banco via aplicação.

### MySQL

É necessário ter o MySQL em execução.

---

Caso queira utilizar a api utilizado no projeto, deve-se cadastrar no site [Link da API](https://www.themoviedb.org/settings/api)

Apos o cadastro, vá em: `profile>settings` para gerar uma chave de API
Assim que for gerada insira a sua chave no código presente na Main do projeto `(scriptAPI.py)` na parte

```ini
def obter_filmes_tmdb(num_filmes):
    api_key = 'insira_sua_chave_aqui'
```

Os comandos dos módulos necessario para a manipulação dos dados API e conexão com o banco de dados são:

```ini
pip install faker
pip install requests
pip install mysql-connector-python
```
