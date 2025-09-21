## Exercício – Proposta de DW
### Objetivo

Planejar e desenvolver um Data Warehouse (DW) simplificado a partir da base transacional criada nos exercícios anteriores, cumprindo as características fundamentais de um DW: organização em dimensões e fatos, suporte a análises históricas e relatórios automáticos.

#### Estrutura do DW

O DW foi criado no banco dw_ecommerce com as seguintes tabelas:

dim_produto → informações estáticas do produto (ID, título, link, imagem).
dim_tempo → calendário (data, ano, mês, dia).
dim_localidade → localidade de referência (cidade/pais).
fato_preco_produto → preços e disponibilidade dos produtos ao longo do tempo.

#### Processo ETL

Extração → dados originais vindos da tabela produtos no banco transacional meudb.
Transformação → ajustes de disponibilidade (texto → boolean).
Carga → inserção nas tabelas dimensionais e na tabela fato.

#### Relatórios Criados

Visão de preços por produto → evolução diária do preço.
Disponibilidade de produtos → status ao longo do tempo.
Consulta consolidada → vw_precos_produtos para análise rápida.

#### Alertas de Anomalias

Criada a view vw_anomalias para monitorar situações incomuns:
Preço menor ou igual a 0.
Produto indisponível.
Preço muito acima da média histórica.

#### Conclusão

O DW proposto permite:

Organização dos dados em dimensões e fatos.
Histórico de preços e disponibilidade.
Relatórios e alertas automáticos para suporte à decisão.
