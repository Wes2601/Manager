from datetime import date


class Jogador:
    def __init__(self, nome, id, nacionalidade, data_nascimento, funcao, potencial, contrato):
        self.nome = nome
        self.id = id
        self.nacionalidade = nacionalidade
        self.data_nascimento = data_nascimento
        self.funcao = funcao
        self.potencial = potencial
        self.contrato = contrato

        self.condicao_fisica = 100
        self.recuperacao = 0
        self.cartoes_amarelos = 0
        self.suspenso = False

    @property
    def esta_lesionado(self):
        return self.recuperacao > 0

    @property
    def salario(self):
        base = self.potencial * 500
        if self.potencial > 80:
            base = base * 3
        if self.potencial > 90:
            base = base * 2

        return int(base)

    @property
    def valor_mercado(self):
        idade = 2025 - self.data_nascimento.year

        valor = self.potencial * 10000

        if self.potencial > 80: valor *= 5
        if self.potencial > 90: valor *= 5

        if idade < 22: valor *= 1.5
        if idade > 32: valor *= 0.6

        return int(valor)

    def __repr__(self):
        return self.nome