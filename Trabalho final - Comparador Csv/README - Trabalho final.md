## Trabalho final - Gestão de Dados
### Objetivo

Foi implementado um comparador de CSV's. O programa roda em localhost e mostra as diferenças entre dois csv's e guarda suas comparacoes em um banco de dados postgre.

#### Hierarquia de usuários

Há o usuário Admin e o de Teste.
 - O admin pode:
**Ver e inserir no banco de dados.**
 - O teste pode:
**Apenas inserir e ver apenas o que ele está fazendo no momento.**

***IMPORTANTE: No arquivo .env, trocar onde está escrito "senhapostgre" pela senha do Postgres do seu computador.***

### Execução do programa
1. Criar o banco de dados comparador_csv no seu postgres.
2. Rodar o arquivo init_db.py para que ele crie as tabelas no banco de dados.
3. Depois rodar o arquivo app_final.py para rodar a aplicação.
