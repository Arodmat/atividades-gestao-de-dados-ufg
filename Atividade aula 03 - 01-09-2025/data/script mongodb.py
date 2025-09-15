from pymongo import MongoClient
from datetime import datetime

# Conexão
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["teste_db"]
colecao_clima = db["clima"]

# Funções CRUD
def inserir_clima(cidade, temperatura, umidade):
    doc = {
        "cidade": cidade,
        "temperatura": temperatura,
        "umidade": umidade,
        "datahora": datetime.now()
    }
    colecao_clima.insert_one(doc)
    print("Clima inserido com sucesso!")

def listar_clima(cidade=None):
    filtro = {"cidade": cidade} if cidade else {}
    return list(colecao_clima.find(filtro))

def atualizar_clima(cidade, nova_temp):
    colecao_clima.update_one({"cidade": cidade}, {"$set": {"temperatura": nova_temp}})
    print("Temperatura atualizada!")

def deletar_clima(cidade):
    colecao_clima.delete_one({"cidade": cidade})
    print("Registro deletado!")

# Testes
if __name__ == "__main__":
    inserir_clima("São Paulo", 22, 70)
    inserir_clima("Rio de Janeiro", 28, 80)

    print("\n📌 Climas cadastrados:")
    for c in listar_clima():
        print(c)

    atualizar_clima("São Paulo", 18)
    print("\n📌 Após atualização:")
    for c in listar_clima("São Paulo"):
        print(c)

    deletar_clima("Rio de Janeiro")
    print("\n📌 Após exclusão:")
    for c in listar_clima():
        print(c)

# Fechar conexão
cliente.close()
