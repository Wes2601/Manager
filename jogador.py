import random
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

        self.moral = 70
        self.esta_lesionado = False
        self.dias_de_molho = 0
        self.convocado = False

        self.atributos = self.inicializar_atributos()

    def inicializar_atributos(self):
            atributos = {}
            atributos['Passe'] = 10
            atributos['Drible'] = 10
            atributos['Finalização'] = 10
            atributos['Desarme'] = 10
            atributos['Marcação'] = 10
            atributos['Cabeceio'] = 10
            atributos['Cruzamento'] = 10
            atributos['Determinação'] = 10
            atributos['Criatividade'] = 10
            atributos['Posicionamento'] = 10
            atributos['Velocidade'] = 10
            atributos['Força'] = 10
            atributos['Resistência'] = 10

            return atributos

    def get_idade(self):
            hoje = date.today()
            data_nasc = self.data_nascimento
            idade = hoje.year - data_nasc.year
            if (hoje.month, hoje.day) < (data_nasc.month, data_nasc.day):
                idade = idade - 1

                return idade

    def alterar_moral(self, valor):
            self.moral += valor
            if self.moral > 100:
                self.moral = 100
            if self.moral < 0:
                self.moral = 0

    def sofrer_lesao(self):
            if not self.esta_lesionado:
                self.tem_lesao = True
                gravidade = random.randint(1, 100)

                if gravidade <= 60:
                    self.dias_de_molho = random.randint(5, 15)
                elif gravidade <+ 90:
                    self.dias_de_molho = random.randint(20, 61)
                else:
                    self.dias_de_molho = random.randint(90, 241)

    def processar_recuperacao_diaria(self, habilidade_fisio):
            if self.esta_lesionado:
                self.dias_de_molho -= 1

            if random.randint (0,29) < habilidade_fisio:
                self.dias_de_molho -= 1

            if self.dias_de_molho <= 0:
                self.dias_de_molho = 0
                self.esta_lesionado = False

                return f"{self.nome} está recuperado da lesão"

            return None

    def processar_desenvolvimento_anual(self, habilidade_tecnico):
        idade = self.get_idade()
        if idade < 28:
            for chave, valor in self.atributos.items():
                if random.randint (0,399) <(self.potencial + habilidade_tecnico) and valor < 20:
                    self.atributos[chave] = valor + 1
        if idade > 30:
                atributos_fisicos = ["Velocidade", "Força", "Resistencia"]
                for atr in atributos_fisicos:
                    valor_atual = self.atributos[atr]

                    if random.randint (0,99) < (idade - 25) and valor_atual > 5:
                        self.atributos[atr] = valor_atual - 1
