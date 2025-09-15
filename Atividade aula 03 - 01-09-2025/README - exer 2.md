# Exercício 2 – Integração PostgreSQL + MongoDB

Este projeto implementa um **CRUD completo** em duas bases de dados diferentes:  
- **PostgreSQL** (relacional)  
- **MongoDB** (NoSQL, orientado a documentos)  

O objetivo é praticar conceitos de **persistência de dados**, **operações CRUD**, **índices** e comparação entre os dois modelos.

---

## Estrutura dos Dados

### PostgreSQL (Relacional)

- **Tabela:** `produtos`
- **Esquema dos campos:**

| Campo   | Tipo           | Descrição                              |
|---------|---------------|----------------------------------------|
| `id`    | SERIAL (PK)   | Identificador único, chave primária     |
| `titulo`| VARCHAR(100)  | Nome ou título do produto               |
| `preco` | NUMERIC       | Preço do produto                        |

- **Índices criados:**
  - `PRIMARY KEY` sobre `id`
  - Índice `idx_produtos_titulo` em `titulo` para melhorar buscas com `ILIKE`
---
### MongoDB (NoSQL – Documentos)

- **Coleção:** `produtos`
- **Exemplo de documento:**
```json
{
  "_id": ObjectId("650f9a2e8f9c123abc456def"),
  "titulo": "Livro Python",
  "preco": 29.90
}
