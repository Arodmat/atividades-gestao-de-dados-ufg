"""
scraper_produtos.py

Script para coletar produtos do site Books to Scrape e salvar em CSV.
Campos extraídos:
- Título
- Preço
- Disponibilidade
- Link
- Imagem

Melhorias:
- Logs claros no console
- Tratamento de erro se página não existir
"""

import requests
from bs4 import BeautifulSoup
import csv

filename = "produtos.csv"

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Título", "Preço", "Disponibilidade", "Link", "Imagem"])

    for page in range(1, 51):
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"❌ Página {page} não encontrada, pulando...")
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            livros = soup.find_all("article", class_="product_pod")

            if not livros:
                print(f"⚠️ Nenhum produto encontrado na página {page}, pulando...")
                continue

            for livro in livros:
                titulo = livro.h3.a["title"]
                preco = livro.find("p", class_="price_color").text
                disponibilidade = livro.find("p", class_="instock availability").text.strip()
                link = "https://books.toscrape.com/catalogue/" + livro.h3.a["href"]
                imagem = "https://books.toscrape.com/" + livro.img["src"].replace("../", "")

                writer.writerow([titulo, preco, disponibilidade, link, imagem])

            print(f"✅ Página {page} processada com {len(livros)} produtos.")

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao acessar a página {page}: {e}")

print(f"\n📂 Dados salvos com sucesso em {filename}")
