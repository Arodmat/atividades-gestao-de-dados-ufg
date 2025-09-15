"""
consulta_clima.py

Script para consultar dados meteorológicos via OpenWeatherMap API e salvar em CSV.
Campos extraídos:
- Cidade
- Temperatura (°C)
- Umidade (%)
- Condição
- Data/Hora da consulta

Melhorias:
- Limite de tentativas (retry) em caso de falha
- CSV de saída para histórico
- Mensagens claras para o usuário
"""

import requests
from datetime import datetime
import csv
import time

API_KEY = "5cb26e90c9b207c2d0c9f4d47925f42b"
MAX_RETRIES = 3
OUTPUT_CSV = "clima.csv"

def consultar_clima(cidade):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            dados = response.json()
            clima = {
                "Cidade": dados.get("name"),
                "Temperatura": dados["main"]["temp"],
                "Umidade": dados["main"]["humidity"],
                "Condicao": dados["weather"][0]["description"],
                "DataHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return clima
        except requests.exceptions.HTTPError:
            print(f"❌ Cidade '{cidade}' não encontrada.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Tentativa {attempt} de {MAX_RETRIES} falhou: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(2)  # espera antes de tentar novamente
            else:
                print("❌ Falha ao consultar a API após várias tentativas.")
                return None

def salvar_clima_csv(clima):
    try:
        # Se arquivo não existir, cria e escreve cabeçalho
        try:
            with open(OUTPUT_CSV, "x", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=clima.keys())
                writer.writeheader()
        except FileExistsError:
            pass  # arquivo já existe

        # Append dos dados
        with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=clima.keys())
            writer.writerow(clima)
        print(f"✅ Dados salvos em {OUTPUT_CSV}")
    except Exception as e:
        print(f"❌ Erro ao salvar CSV: {e}")

if __name__ == "__main__":
    cidade_input = input("Digite o nome da cidade: ")
    resultado = consultar_clima(cidade_input)

    if resultado:
        print("\n🌍 Dados do clima:")
        print("Cidade:", resultado["Cidade"])
        print("Temperatura:", resultado["Temperatura"], "°C")
        print("Umidade:", resultado["Umidade"], "%")
        print("Condição:", resultado["Condicao"])
        print("Data/Hora da consulta:", resultado["DataHora"])

        salvar_clima_csv(resultado)
