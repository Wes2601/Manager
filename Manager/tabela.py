class Posicao:

    def __init__(self, time):
        self.time = time
        self.pontos = 0
        self.vitorias = 0
        self.empates = 0
        self.derrotas = 0
        self.gols_pro = 0
        self.gols_contra = 0

    def saldo_gols(self):
        return self.gols_pro - self.gols_contra


class Tabela:
    def __init__(self, times):

        self.posicoes = {}
        for time in times:
            self.posicoes[time] = Posicao(time)

    def atualizar(self, time, gols_feitos, gols_sofridos):
        posicao = self.posicoes[time]

        posicao.gols_pro += gols_feitos
        posicao.gols_contra += gols_sofridos

        if gols_feitos > gols_sofridos:
            posicao.pontos += 3
            posicao.vitorias += 1
        elif gols_feitos == gols_sofridos:
            posicao.pontos += 1
            posicao.empates += 1
        else:
            posicao.derrotas += 1