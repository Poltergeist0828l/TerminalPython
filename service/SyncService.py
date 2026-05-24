from datetime import datetime

import requests

from database.DatabaseProdutos import DatabaseProdutos
from model.Produtos import Produtos


class SyncService:

    def __init__(self):

        self.db = DatabaseProdutos()

        self.API_URL = "http://localhost:8080/produtos/sync?lastSync="

    def get_last_sync(self):
        try:
            with open("database/last_sync.txt", "r") as file:
                return file.read()

        except:
            return "2000-01-01T00:00:00"

    def save_last_sync(self):

        with open("database/last_sync.txt", "w") as file:
            file.write(datetime.now().isoformat())

    # SINCRONIZAÇÃO
    def sincronizar_produtos(self):

        try:

            response = requests.get(self.API_URL + self.get_last_sync())

            if response.status_code == 200:

                produtos = response.json()

                for p in produtos:
                    produto = Produtos(
                        id=p.get("id"),
                        codigo=p.get("codigo"),
                        nome=p.get("nome"),
                        preco=p.get("preco"),
                        quantidade=p.get("quantidade"),
                        categoria=p.get("categoria"),
                        unidade_medida=p.get("unidadeMedida"),
                        descricao=p.get("descricao"),
                        foto=p.get("foto"),
                        peso=p.get("peso"),
                        peso_tolerancia=p.get("pesoTolerancia"),
                        create_at=p.get("createAt"),
                        update_at=p.get("updateAt"),
                        status=p.get("status")
                    )

                    # salva no SQLite
                    self.db.salvar_ou_atualizar(produto)

                # salva nova data de sync
                self.save_last_sync()

                print("Sincronização concluída!")

        except Exception as e:

            print("Erro no sync")
            print(e)
