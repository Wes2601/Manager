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

        self.esta_lesionado = False
        self.condicao_fisica = 100

    @property
    def salario(self):
        fator_salarial = (self.potencial ** 2) / 10
        return int(fator_salarial * 15)

    @property
    def valor_mercado(self):
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year

        fator_idade = 1.0
        if idade < 23:
            fator_idade = 1.5
        elif idade > 32:
            fator_idade = 0.6

        valor_base = (self.potencial ** 2) * 500
        return int(valor_base * fator_idade)