from model.Item import Item


class Carrinho:

    def __init__(self, terminal_id):

        self.terminal_id = terminal_id

        self.items = []

    # adicionar item
    def adicionar_item(self, item: Item):

        for i in self.items:

            if i.produto.codigo == item.produto.codigo:
                i.quantidade += item.quantidade

                return

        self.items.append(item)

    # remover item pelo código
    def remover_item(self, codigo_produto):

        self.items = [
            item for item in self.items
            if item.produto.codigo != codigo_produto
        ]

    # limpar carrinho
    def limpar(self):

        self.items.clear()

    # quantidade total de itens
    def quantidade_total_itens(self):

        return sum(item.quantidade for item in self.items)

    # total do carrinho
    def total(self):

        return sum(
            item.produto.preco * item.quantidade
            for item in self.items
        )

    # busca item
    def buscar_item(self, codigo_produto):

        for item in self.items:

            if item.produto.codigo == codigo_produto:
                return item

        return None

    # verifica se carrinho está vazio
    def vazio(self):

        return len(self.items) == 0

    # listar itens
    def listar_itens(self):

        return self.items

    # remover uma unidade
    def remover_quantidade_item(self, codigo_produto, quantidade=1):

        for item in self.items:

            if item.produto.codigo == codigo_produto:

                item.quantidade -= quantidade

                if item.quantidade <= 0:
                    self.remover_item(codigo_produto)

                return

    # total formatado
    def total_formatado(self):

        return f"R$ {self.total():.2f}"

    def to_dict(self):

        return {

            "terminalId": self.terminal_id,

            "items": [

                {
                    "productId": item.produto.id,

                    "quantity": item.quantidade,

                    "receivedWeight": item.received_weight
                }

                for item in self.items

            ]

        }

    def __str__(self):

        texto = "\n=== CARRINHO ===\n"

        for item in self.items:
            subtotal = item.produto.preco * item.quantidade

            texto += (
                f"{item.produto.nome} "
                f"x{item.quantidade} "
                f"- R$ {subtotal:.2f}\n"
            )

        texto += f"\nTOTAL: {self.total_formatado()}"

        return texto
