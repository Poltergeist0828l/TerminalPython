import requests
import json

class ApiService:

    def __init__(self):
        # Troque para sua URL Render se quiser usar online:
        # self.base_url = "https://app247.onrender.com"

        self.base_url = "http://localhost:8080"

    def buscar_produto(self, codigo_barras):

        try:
            response = requests.get(
                f"{self.base_url}/produtos/{codigo_barras}",
                timeout=3
            )

            if response.status_code == 200:
                return response.json()

            print("Produto não encontrado:", response.status_code)
            return None

        except Exception as e:
            print("Erro de conexão com Spring Boot:", e)
            return None

    def adicionar_produto(self, produto):

        try:

            files = {
                'data': (
                    None,
                    json.dumps(produto),
                    'application/json'
                )
            }

            response = requests.post(
                f"{self.base_url}/produtos",
                files=files,
                timeout=5
            )

            print("Resposta API:", response.text)

            return response.status_code in [200, 201]

        except Exception as e:
            print("Erro ao adicionar produto:", e)
            return False

    def registrar_venda(self, dados_venda):

        try:
            response = requests.post(
                f"{self.base_url}/vendas",
                json=dados_venda,
                timeout=3
            )

            return response.status_code in [200, 201]

        except Exception as e:
            print("Erro ao registrar venda:", e)
            return False
