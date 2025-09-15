### Objetivo Exercício 1

Implementar um sistema de coleta automatizada de dados utilizando scraping em Python para extrair informações de produtos de um e-commerce de teste, e utilizar API pública de meteorologia para coletar dados climáticos.

O projeto mostra:

Capacidade de extrair dados de uma fonte web e estruturá-los.
Consumo de uma API externa com tratamento de erros.
Armazenamento dos dados em CSV para análise posterior.

### Ferramentas e Bibliotecas Usadas
Ferramenta / Biblioteca	Finalidade
Python 3.13	Linguagem de programação
requests	Fazer requisições HTTP para site e API
BeautifulSoup4	Parsear HTML para scraping
csv (builtin)	Salvar dados em CSV
pandas (opcional)	Facilitar manipulação e visualização dos dados
OpenWeatherMap API	Fonte de dados meteorológicos

Observação: A escolha de Python + requests + BeautifulSoup é porque o exercício pediu coleta automatizada de dados, e esses pacotes são simples, robustos e amplamente utilizados.

### Coleta de dados do e-commerce
##### 3.1 Site usado

Books to Scrape (http://books.toscrape.com
) — site de teste público com produtos fictícios de livros.

##### 3.2 Campos extraídos
Campo	Tipo	Descrição
Título	string	Nome do produto (livro)
Preço	string	Preço do produto, em libra esterlina (£)
Disponibilidade	string	Status em estoque (ex.: "In stock")
Link	string	URL direta para a página do produto
Imagem	string	URL da imagem do produto

##### 3.3 Processo do scraper

Loop através das 50 páginas do site de exemplo.

Para cada página:

Fazer requisição HTTP com requests.get.
Parsear HTML com BeautifulSoup.
Extrair cada produto usando seletor article.product_pod.
Para cada produto, coletar título, preço, disponibilidade, link e imagem.
Armazenar todos os produtos em um único CSV (produtos.csv) com cabeçalho adequado.
Printar no console o progresso, página por página.

##### 3.4 Tratamento de erros

Se a página não existir (status != 200), o scraper pula para a próxima página e registra mensagem de erro no console.

Todos os dados são limpos de espaços extras (strip()) para consistência.

### Coleta de dados de meteorologia (API pública)
##### 4.1 API usada

OpenWeatherMap (https://openweathermap.org/api
)

Consulta do tempo atual por cidade.
Requer API Key para autenticação.

##### 4.2 Campos extraídos
Campo	Tipo	Descrição
Cidade	string	Nome da cidade consultada
Temperatura	float	Temperatura em Celsius
Umidade	int	Percentual de umidade
Condição	string	Descrição do clima (ex.: "céu limpo")
DataHora	string	Data e hora da consulta (local)

##### 4.3 Processo da API

O usuário digita o nome da cidade no console (input).
Construção da URL com parâmetros: cidade, API Key, unidades métricas, idioma português.
Requisição HTTP via requests.get.
Parsear resposta JSON e extrair campos desejados.

Tratamento de erros:

Se cidade não existir → mensagem amigável.
Se problema de conexão ou timeout → mensagem de erro clara.

### Organização do projeto
projeto_coleta_dados/
│
├─ scraper_produtos.py       # Script de scraping de produtos
├─ consulta_clima.py         # Script de consulta meteorológica
├─ produtos.csv              # CSV gerado pelo scraper
└─ README_documentacao.md    # Esta documentação detalhada

### Como rodar os scripts

Instalar bibliotecas necessárias:

pip install requests beautifulsoup4 pandas

Rodar scraper de produtos:
python scraper_produtos.py

Resultado: arquivo produtos.csv com todos os produtos.

Rodar consulta de clima:
python consulta_clima.py


Digitar o nome da cidade quando solicitado.
Resultado: dados do clima impressos no console.

### Boas práticas e segurança

API Key armazenada no código apenas para fins de teste. Em produção, usar variável de ambiente ou arquivo .env.
Todos os scripts têm tratamento de erros para evitar que o programa quebre.
CSV gerado está codificado em UTF-8 para compatibilidade com Excel e Power BI.

### Conclusão

O projeto demonstra:

Coleta automatizada de dados de fontes web e API pública.
Armazenamento estruturado em CSV para análise futura.
Implementação de tratamento de erros e mensagens claras.
Documentação dos campos e do processo de coleta.




