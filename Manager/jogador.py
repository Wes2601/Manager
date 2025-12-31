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
        self.dias_lesao = 0

    @property
    def valor_mercado(self):
        valor = self.potencial * 10000

        idade = 2025 - self.data_nascimento.year
        if idade < 23:
            valor = valor * 1.5

        return int(valor)

    def processar_recuperacao_diaria(self, habilidade_medico):
        if not self.esta_lesionado:
            return None

        fator_cura = 1 + (habilidade_medico / 10)
        self.dias_lesao -= fator_cura

        if self.dias_lesao <= 0:
            self.dias_lesao = 0
            self.esta_lesionado = False
            return f"{self.nome} se recuperou da lesão!"

        return None