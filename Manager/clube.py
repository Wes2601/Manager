import random


class Time:
    def __init__(self, nome, id, nacionalidade, elenco=None):
        self.nome = nome
        self.id = id
        self.nacionalidade = nacionalidade
        self.elenco = elenco if elenco is not None else []

        self.saldo_em_caixa = 2000000
        self.capacidade_estadio = random.randint(20000, 60000)
        self.preco_ingresso = 50

    def adicionar_jogador(self, jogador):
        self.elenco.append(jogador)

    def __repr__(self):
        return self.nome

    def __str__(self):
        return self.nome

    @property
    def folha_salarial(self):
        if not self.elenco:
            return 0
        return sum(jogador.salario for jogador in self.elenco)

    @property
    def forca_ataque(self):
        atacantes = [j.potencial for j in self.elenco if "Atacante" in j.funcao or "Meio" in j.funcao]
        if not atacantes: return 50
        atacantes.sort(reverse=True)
        top_5 = atacantes[:5]
        return sum(top_5) / len(top_5)

    @property
    def forca_defesa(self):
        defensores = [j.potencial for j in self.elenco if "Defensor" in j.funcao or "Goleiro" in j.funcao]
        if not defensores: return 50
        defensores.sort(reverse=True)
        top_5 = defensores[:5]
        return sum(top_5) / len(top_5)

    def receber_bilheteria(self):
        ocupacao = random.uniform(0.50, 1.00)
        publico = int(self.capacidade_estadio * ocupacao)

        renda = publico * self.preco_ingresso
        self.saldo_em_caixa += renda

        return renda, publico