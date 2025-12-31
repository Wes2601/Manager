import random
from calendario import Calendario
from tabela import Tabela
from datetime import date, timedelta


class Campeonato:
    def __init__(self, times, ano):
        self.times = times
        self.ano_atual = ano
        self.calendario = Calendario(times, ano)
        self.tabela = Tabela(times)
        self.data_atual = date(ano, 1, 1)
        self.time_do_usuario = times[0]

    def avancar_um_dia(self):
        self.simular_jogos_de_hoje()
        self.data_atual += timedelta(days=1)

    def get_jogos_de_hoje(self):
        return self.calendario.jogos_agendados.get(self.data_atual, [])

    def simular_jogos_de_hoje(self):
        jogos = self.get_jogos_de_hoje()

        for partida in jogos:
            forca_casa = partida.time_casa.forca_geral
            forca_visitante = partida.time_visitante.forca_geral

            vantagem = forca_casa - forca_visitante

            gols_casa = random.randint(0, 2)
            gols_visitante = random.randint(0, 2)

            if vantagem > 0:
                bonus = int(vantagem / 5)
                gols_casa += random.randint(0, bonus)
            elif vantagem < 0:
                bonus = int(abs(vantagem) / 5)
                gols_visitante += random.randint(0, bonus)

            gols_casa += random.choice([0, 1])

            partida.placar_casa = gols_casa
            partida.placar_visitante = gols_visitante
            partida.foi_jogado = True

            self.tabela.atualizar(partida.time_casa, gols_casa, gols_visitante)
            self.tabela.atualizar(partida.time_visitante, gols_visitante, gols_casa)

            print(f"JOGO: {partida.time_casa.nome} {gols_casa} x {gols_visitante} {partida.time_visitante.nome}")

        return jogos