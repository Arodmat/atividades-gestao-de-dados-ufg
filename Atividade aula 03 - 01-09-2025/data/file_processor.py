# file_processor.py
import pandas as pd

CSV_FILE = "produtos.csv"

try:
    # --- Leitura do CSV com encoding ---
    df = pd.read_csv(CSV_FILE, encoding="utf-8-sig")

    print("✅ Arquivo carregado com sucesso!\n")
    print("📊 Prévia original:")
    print(df.head())

    # --- Limpeza e Normalização ---
    df["Título"] = df["Título"].str.strip()
    df["Preço"] = (
        df["Preço"]
        .str.replace("Â", "", regex=False)   # remove caractere extra
        .str.replace("£", "", regex=False)   # remove símbolo da moeda
        .str.replace(",", "", regex=False)   # remove vírgulas
        .astype(float)
    )
    df["Disponibilidade"] = df["Disponibilidade"].str.lower().map({
        "in stock": 1,
        "out of stock": 0
    })

    print("\n✅ Dados limpos e normalizados!\n")
    print("📊 Prévia dos dados transformados:")
    print(df.head())

    # --- Salvar arquivo limpo ---
    df.to_csv("produtos_limpos.csv", index=False)
    print("\n💾 Arquivo 'produtos_limpos.csv' salvo.")

    # --- Parte 3: Agregações ---
    print("\n📊 Estatísticas dos produtos:")

    total_produtos = len(df)
    media_preco = df["Preço"].mean()
    preco_min = df["Preço"].min()
    preco_max = df["Preço"].max()
    disponiveis = df["Disponibilidade"].sum()  # soma porque 1=disponível
    indisponiveis = total_produtos - disponiveis

    print(f"🔹 Total de produtos: {total_produtos}")
    print(f"🔹 Preço médio: £{media_preco:.2f}")
    print(f"🔹 Preço mínimo: £{preco_min:.2f}")
    print(f"🔹 Preço máximo: £{preco_max:.2f}")
    print(f"🔹 Produtos disponíveis: {disponiveis}")
    print(f"🔹 Produtos indisponíveis: {indisponiveis}")

except Exception as e:
    print("❌ Erro ao processar o arquivo:", e)

    # --- Parte 4: Relatórios Visuais ---
import matplotlib.pyplot as plt
import os

# Cria pasta reports se não existir
os.makedirs("reports", exist_ok=True)

# 1️⃣ Distribuição de preços
plt.figure(figsize=(8,5))
plt.hist(df["Preço"], bins=20, color="skyblue", edgecolor="black")
plt.title("Distribuição de Preços dos Produtos")
plt.xlabel("Preço (£)")
plt.ylabel("Quantidade de Produtos")
plt.grid(axis="y", alpha=0.75)
plt.tight_layout()
plt.savefig("reports/precos_distribuicao.png")
plt.close()
print("💾 Gráfico 'precos_distribuicao.png' salvo em reports/")

# Contagem de disponibilidade com todos os valores 0 e 1 garantidos
disponibilidade_counts = df["Disponibilidade"].value_counts().reindex([1,0], fill_value=0)

plt.figure(figsize=(5,5))
plt.pie(
    disponibilidade_counts,
    labels=["Disponível", "Indisponível"],
    autopct="%1.1f%%",
    colors=["green","red"],
    startangle=90
)
plt.title("Disponibilidade de Produtos")
plt.tight_layout()
plt.savefig("reports/disponibilidade.png")
plt.close()
print("💾 Gráfico 'disponibilidade.png' salvo em reports/")


print("✅ Relatórios visuais gerados com sucesso!")

