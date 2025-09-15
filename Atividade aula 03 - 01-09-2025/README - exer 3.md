# Exercício 3 – Pipeline de Processamento de Dados

## Objetivo
Desenvolver um pipeline de processamento utilizando MCP File Processor e MCP Stream Processor para transformar, analisar e gerar insights dos dados coletados no exercício anterior.

---
## Estrutura do Pipeline

### 1️⃣ Leitura de Arquivos (File Processor)
- Arquivo CSV utilizado: `produtos.csv`
- Leitura realizada com `pandas.read_csv()` usando encoding `'utf-8-sig'` para garantir caracteres especiais corretos.
- Pré-visualização dos dados realizada com `df.head()`.

### 2️⃣ Limpeza e Normalização dos Dados
- **Título**: remoção de espaços extras (`.str.strip()`)
- **Preço**: conversão de texto (`£51.77`) para número decimal (`float`)  
  - Remoção de caracteres indesejados: `Â`, `£`, `,`
- **Disponibilidade**: padronização para valores binários  
  - `"In stock"` → `1`  
  - `"Out of stock"` → `0`

- O resultado é salvo em `produtos_limpos.csv`.

### 3️⃣ Agregações e Estatísticas
- Total de produtos
- Preço médio, mínimo e máximo
- Quantidade de produtos disponíveis vs. indisponíveis

**Exemplo de saída:**
Total de produtos: 1000
Preço médio: £35.07
Preço mínimo: £10.00
Preço máximo: £59.99
Produtos disponíveis: 1000
Produtos indisponíveis: 0

### 4️⃣ Relatórios Visuais / Dashboards
- **Histograma de Preços**: distribuição dos produtos por faixa de preço  
  - Arquivo gerado: `reports/precos_distribuicao.png`
- **Gráfico de Pizza da Disponibilidade**: proporção de produtos disponíveis vs. indisponíveis  
  - Arquivo gerado: `reports/disponibilidade.png`
- Diretório `reports/` criado automaticamente se não existir.
- Gráficos gerados com `matplotlib.pyplot`.
-
## Estrutura de Arquivos do Exercício 3
file_processor.py # Script principal do pipeline
produtos.csv # CSV original coletado
produtos_limpos.csv # CSV transformado e normalizado
reports/ # Pasta contendo gráficos
├─ precos_distribuicao.png
└─ disponibilidade.png

### Observações

O pipeline é modular e pode ser facilmente adaptado para outros datasets similares.
O código trata casos de encoding e caracteres indesejados, garantindo que os dados fiquem prontos para análises futuras.
Apesar do Stream Processor não estar implementado em tempo real, a estrutura permite fácil extensão para processamentos contínuos.
