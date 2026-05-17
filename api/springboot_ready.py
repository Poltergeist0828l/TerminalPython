import requests

class ApiService:
    def __init__(self):
        self.base_url = "http://localhost:8080"

    def buscar_produto(self, codigo_barras):
        try:
            response = requests.get(f"{self.base_url}/produtos/{codigo_barras}", timeout=2)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro de conexão com Spring Boot: {e}")
            return None

    def registrar_venda(self, dados_venda):
        try:
            response = requests.post(f"{self.base_url}/vendas", json=dados_venda, timeout=3)
            return response.status_code == 201
        except:
            return False
