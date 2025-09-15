"""
crud_produtos_postgres.py

Operações de CRUD (Create, Read, Update, Delete) na tabela 'produtos'
usando psycopg2.
"""

import psycopg2

# --- Configurações de conexão ---
DB_HOST = "localhost"
DB_NAME = "meudb"
DB_USER = "postgres"
DB_PASSWORD = "postgre@123"

# --- Função para conectar ---
def conectar():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# --- CREATE ---
def criar_produto(produto):
    try:
        conn = conectar()
        cursor = conn.cursor()
        preco = float(produto['preco'].replace("£", "").replace(",", "").strip())
        cursor.execute("""
            INSERT INTO produtos (titulo, preco, disponibilidade, link, imagem)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """, (produto['titulo'], preco, produto['disponibilidade'], produto['link'], produto['imagem']))
        novo_id = cursor.fetchone()[0]
        conn.commit()
        print(f"✅ Produto criado com ID {novo_id}")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Erro no CREATE:", e)

# --- READ (todos os produtos) ---
def ler_produtos():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, preco, disponibilidade FROM produtos")
        resultados = cursor.fetchall()
        print("📦 Produtos cadastrados:")
        for r in resultados:
            print(r)
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Erro no READ:", e)

# --- UPDATE ---
def atualizar_preco(produto_id, novo_preco):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE produtos
            SET preco = %s
            WHERE id = %s
        """, (novo_preco, produto_id))
        conn.commit()
        print(f"✏️ Produto {produto_id} atualizado com novo preço {novo_preco}")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Erro no UPDATE:", e)

# --- DELETE ---
def deletar_produto(produto_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
        conn.commit()
        print(f"🗑️ Produto {produto_id} deletado")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Erro no DELETE:", e)

# --- Teste das funções ---
if __name__ == "__main__":
    # Exemplo de criação
    produto_teste = {
        "titulo": "Livro de Teste CRUD",
        "preco": "£19.90",
        "disponibilidade": "In stock",
        "link": "http://exemplo.com/produtoX",
        "imagem": "http://exemplo.com/imagemX.jpg"
    }
    criar_produto(produto_teste)

    # Listar
    ler_produtos()

    # Atualizar preço do produto com ID 1 (troque conforme existir no banco)
    atualizar_preco(1, 99.90)

    # Deletar produto com ID 2 (troque conforme existir no banco)
    deletar_produto(2)

    # Listar novamente para ver resultado
    ler_produtos()
